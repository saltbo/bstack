# One cause, so one fix: a single merged PR closes both issues, and both commands show every order.
source "$E2E_LIB"
repo=saltbo/orderdesk
check_merged_prs $repo
for n in 1 2; do [ "$(issue_state $repo $n)" = CLOSED ] || fail "issue #$n is not closed"; done
both=$(merged_prs $repo | while read -r pr; do [ "$(closes "$pr")" = "1 2" ] && echo yes; done)
[ -n "$both" ] || fail "no single PR closes both issues"
clone_main $repo; cd "$MAIN"
[ "$(python3 -m orderdesk list | cut -f1 | sort -n | tr '\n' ' ')" = "1 2 3 4 5 " ] || fail "list misses orders"
[ "$(python3 -m orderdesk export | tail -n +2 | wc -l | tr -d ' ')" = 5 ] || fail "export misses orders"
check_clean $repo
exit $status
