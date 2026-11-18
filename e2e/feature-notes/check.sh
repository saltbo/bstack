# Delete works in production, it got there through a PR that had green CI and a preview, and nothing is left behind.
set -u
repo=saltbo/notes
status=0
fail() { echo "FAIL: $*"; status=1; }
pr=$(jq -c --arg r "$repo" '.repos[$r].prs | to_entries | map(.value) | map(select(.state=="MERGED")) | first // empty' "$STATE")
[ -n "$pr" ] || { echo "FAIL: no merged pull request"; jq ".repos[\"$repo\"].prs" "$STATE"; exit 1; }
head=$(echo "$pr" | jq -r .head_sha); branch=$(echo "$pr" | jq -r .head)
echo "merged PR #$(echo "$pr" | jq .number) from $branch: $(echo "$pr" | jq -r .title)"
ci=$(jq -r --arg r "$repo" --arg s "$head" '[.repos[$r].runs[] | select(.sha==$s)] | map(.conclusion) | join(",")' "$STATE")
echo "CI on its head: $ci"
[ "$ci" = "success" ] || fail "CI on the merged head was not green"
previews=$(jq --arg r "$repo" --arg b "$branch" '[.repos[$r].deployments[] | select(.branch==$b and .target=="preview" and .ok)] | length' "$STATE")
echo "preview deployments of the branch: $previews"
[ "$previews" -ge 1 ] || fail "the branch never had a working preview"
prod=$(jq -r --arg r "$repo" '.repos[$r].production' "$STATE")
echo "production: $(echo "$prod" | jq -r '.sha[0:7] + " ok=" + (.ok|tostring)')"
main=$(git ls-remote "https://github.com/$repo.git" refs/heads/main | cut -f1)
[ "$(echo "$prod" | jq -r .sha)" = "$main" ] || fail "production does not run main"
url="http://notes.localhost:$PROXY_PORT"
created=$(curl -s -X POST "$url/api/notes" -H 'content-type: application/json' -d '{"body":"to be deleted"}')
id=$(echo "$created" | jq -r '.note.id // empty')
[ -n "$id" ] || fail "could not add a note in production: $created"
if [ -n "$id" ]; then
  code=$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$url/api/notes/$id")
  echo "DELETE /api/notes/$id -> $code"
  still=$(curl -s "$url/api/notes" | jq --argjson id "$id" '[.notes[] | select(.id==$id)] | length')
  [ "$still" = 0 ] || fail "the note is still listed after deleting it"
fi
shown=$(curl -s -X POST "$url/api/notes" -H 'content-type: application/json' -d '{"body":"shown on the page"}' | jq -r '.note.id // empty')
curl -s "$url/" | grep -qi "delete" || fail "a note on the page has no delete control"
dir=$(mktemp -d); trap 'rm -rf "$dir"' EXIT
git clone -q "https://github.com/$repo.git" "$dir/main"
grep -rqi "delete" "$dir/main/spec" || fail "no scenario in spec/ covers deleting"
left=$(git ls-remote --heads "https://github.com/$repo.git" | grep -v refs/heads/main | wc -l | tr -d ' ')
[ "$left" = 0 ] || fail "$left branch(es) left on the remote"
exit $status
