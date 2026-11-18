# The fix reached main through a merged PR whose CI passed, every order is listed, and nothing is left behind.
set -u
repo=saltbo/orderdesk
fail() { echo "FAIL: $*"; status=1; }
status=0
pr=$(jq -c --arg r "$repo" '.repos[$r].prs | to_entries | map(.value) | map(select(.state=="MERGED")) | first // empty' "$STATE")
[ -n "$pr" ] || { echo "FAIL: no merged pull request"; jq ".repos[\"$repo\"].prs" "$STATE"; exit 1; }
number=$(echo "$pr" | jq .number); head=$(echo "$pr" | jq -r .head_sha); branch=$(echo "$pr" | jq -r .head)
echo "merged PR #$number from $branch: $(echo "$pr" | jq -r .title)"
ci=$(jq -r --arg r "$repo" --arg s "$head" '[.repos[$r].runs[] | select(.sha==$s)] | map(.conclusion) | join(",")' "$STATE")
echo "CI on its head: $ci"
[ "$ci" = "success" ] || fail "CI on the merged head was not a single success"
dir=$(mktemp -d); trap 'rm -rf "$dir"' EXIT
git clone -q "https://github.com/$repo.git" "$dir/main"
listed=$(cd "$dir/main" && python3 -m orderdesk list | cut -f1 | sort -n | tr '\n' ' ')
echo "main lists: $listed"
[ "$listed" = "1 2 3 4 5 " ] || fail "main does not list every order"
(cd "$dir/main" && python3 -m unittest -q >/dev/null 2>&1) || fail "the gate fails on main"
left=$(git ls-remote --heads "https://github.com/$repo.git" | grep -v refs/heads/main | wc -l | tr -d ' ')
[ "$left" = 0 ] || fail "$left branch(es) left on the remote"
open=$(jq --arg r "$repo" '[.repos[$r].prs[] | select(.state=="OPEN")] | length' "$STATE")
[ "$open" = 0 ] || fail "$open PR(s) still open"
exit $status
