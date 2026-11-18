# Both features reached production through separate merged PRs, each with green CI and a preview, and every task is done.
set -u
repo=saltbo/notes
status=0
fail() { echo "FAIL: $*"; status=1; }
merged=$(jq --arg r "$repo" '[.repos[$r].prs[] | select(.state=="MERGED")] | length' "$STATE")
echo "merged PRs: $merged"
[ "$merged" -ge 2 ] || fail "fewer than two merged PRs"
for row in $(jq -r --arg r "$repo" '.repos[$r].prs[] | select(.state=="MERGED") | "\(.number):\(.head):\(.head_sha)"' "$STATE"); do
  n=${row%%:*}; rest=${row#*:}; branch=${rest%%:*}; sha=${rest#*:}
  ci=$(jq -r --arg r "$repo" --arg s "$sha" '[.repos[$r].runs[] | select(.sha==$s)] | map(.conclusion) | join(",")' "$STATE")
  pv=$(jq --arg r "$repo" --arg b "$branch" '[.repos[$r].deployments[] | select(.branch==$b and .target=="preview" and .ok)] | length' "$STATE")
  echo "PR #$n $branch: CI=$ci previews=$pv"
  [ "$ci" = "success" ] || fail "PR #$n merged without green CI on its head"
  [ "$pv" -ge 1 ] || fail "PR #$n never had a working preview"
done
main=$(git ls-remote "https://github.com/$repo.git" refs/heads/main | cut -f1)
[ "$(jq -r --arg r "$repo" '.repos[$r].production.sha' "$STATE")" = "$main" ] || fail "production does not run main"
dir=$(mktemp -d); trap 'rm -rf "$dir"' EXIT
git clone -q "https://github.com/$repo.git" "$dir/main"
grep -rqiE "tag|标签" "$dir/main/spec" || fail "no scenario covers tags"
grep -rqiE "search|搜索" "$dir/main/spec" || fail "no scenario covers search"
(cd "$dir/main" && cp -cR "$WORK/node_modules" node_modules && pnpm verify >/dev/null 2>&1) || fail "the gate fails on main"
url="http://notes.localhost:$PROXY_PORT"
curl -s "$url/" | grep -qiE "search|搜索" || fail "the production page has no search"
if [ -f "$DOCKET_DB" ]; then
  echo "docket tasks: $(sqlite3 "$DOCKET_DB" "select status || ' ' || count(*) from tasks group by status" | tr '\n' ' ')"
  undone=$(sqlite3 "$DOCKET_DB" "select count(*) from tasks where status not in ('done','cancelled')")
  [ "$undone" = 0 ] || fail "$undone docket task(s) not done"
else
  fail "no docket tasks were created"
fi
left=$(git ls-remote --heads "https://github.com/$repo.git" | grep -v refs/heads/main | wc -l | tr -d ' ')
[ "$left" = 0 ] || fail "$left branch(es) left on the remote"
exit $status
