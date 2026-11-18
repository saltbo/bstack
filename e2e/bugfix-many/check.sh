# Four reported bugs, each fixed in a PR of its own. A fifth, unreported bug in `top` is a follow-up, not part of these fixes.
source "$E2E_LIB"
repo=saltbo/orderdesk
check_merged_prs $repo
for n in 1 2 3 4; do [ "$(issue_state $repo $n)" = CLOSED ] || fail "issue #$n is not closed"; done
count=$(merged_prs $repo | wc -l | tr -d ' ')
echo "merged PRs: $count, subagents are in result.json"
[ "$count" -ge 4 ] || fail "four bugs with four causes got $count PR(s)"
merged_prs $repo | while read -r pr; do n=$(closes "$pr" | wc -w | tr -d ' '); [ "$n" -le 1 ] || echo "FAIL: PR #$(echo "$pr" | jq .number) closes $n issues with different causes"; done | grep . && status=1
clone_main $repo; cd "$MAIN"
[ "$(python3 -m orderdesk list | cut -f1 | sort -n | tr '\n' ' ')" = "1 2 3 4 5 " ] || fail "list misses orders"
[ "$(python3 -m orderdesk revenue)" = 113 ] || fail "revenue is wrong"
[ "$(python3 -m orderdesk average)" = 22.6 ] || fail "average is $(python3 -m orderdesk average)"
[ "$(python3 -m orderdesk since 105 | cut -f1 | sort -n | tr '\n' ' ')" = "2 3 4 5 " ] || fail "since is wrong"
python3 -m unittest -q >/dev/null 2>&1 || fail "the gate fails on main"
filed=$(jq --arg r "$repo" '[.repos[$r].issues[] | select(.number > 4) | select((.title + .body) | test("top"; "i"))] | length' "$STATE")
{ [ "$filed" -ge 1 ] || report_mentions "top"; } || fail "the unreported bug in top was neither filed nor reported"
check_clean $repo
exit $status
