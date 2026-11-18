# Each issue was fixed by a merged PR of its own with green CI, the issues are closed, and nothing is left behind.
set -u
source "$E2E_LIB"
repo=saltbo/orderdesk
status=0
fail() { echo "FAIL: $*"; status=1; }
for n in 1 2; do
  state=$(jq -r --arg r "$repo" --arg n "$n" '.repos[$r].issues[$n].state' "$STATE")
  echo "issue #$n: $state"
  [ "$state" = "CLOSED" ] || fail "issue #$n is not closed"
done
merged=$(jq -c --arg r "$repo" '[.repos[$r].prs[] | select(.state=="MERGED")]' "$STATE")
echo "merged PRs: $(echo "$merged" | jq -r 'map("#\(.number) \(.head): \(.title)") | join("; ")')"
[ "$(echo "$merged" | jq length)" -ge 2 ] || fail "the two bugs did not get a PR each"
for row in $(echo "$merged" | jq -r '.[] | "\(.number):\(.head_sha)"'); do
  ci=$(jq -r --arg r "$repo" --arg s "${row#*:}" '[.repos[$r].runs[] | select(.sha==$s)] | map(.conclusion) | join(",")' "$STATE")
  [ "$ci" = "success" ] || fail "PR #${row%%:*} merged without green CI"
done
closes=$(echo "$merged" | jq -r '[.[].body | scan("(?i)(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?) #([12])") | .[0]] | unique | join(",")')
echo "PRs close issues: $closes"
[ "$closes" = "1,2" ] || fail "the PRs do not close both issues"
dir=$(mktemp -d); trap 'rm -rf "$dir"' EXIT
git clone -q "https://github.com/$repo.git" "$dir/main"
cd "$dir/main"
listed=$(python3 -m orderdesk list | cut -f1 | sort -n | tr '\n' ' ')
[ "$listed" = "1 2 3 4 5 " ] || fail "main lists $listed"
revenue=$(python3 -m orderdesk revenue)
[ "$revenue" = "113" ] || fail "main reports revenue $revenue"
python3 -m unittest -q >/dev/null 2>&1 || fail "the gate fails on main"
left=$(git ls-remote --heads origin | grep -v refs/heads/main | wc -l | tr -d ' ')
[ "$left" = 0 ] || fail "$left branch(es) left on the remote"
check_local_clean
[ "$status" = 0 ] || exit 1
exit $status
