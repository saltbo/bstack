# Issue 1 is a bug and is fixed. Issue 2 asks for a new feature: the session leaves it to the user, who says not now.
source "$E2E_LIB"
repo=saltbo/orderdesk
check_merged_prs $repo
[ "$(issue_state $repo 1)" = CLOSED ] || fail "issue #1 is not closed"
clone_main $repo; cd "$MAIN"
grep -rq -- "--json" orderdesk && fail "a --json flag was built under bugfix"
[ "$(python3 -m orderdesk list | cut -f1 | tr '\n' ' ')" = "1 2 3 4 5 " ] || fail "main does not list every order"
report_mentions "#2" || fail "the report does not mention issue #2"
[ "$(issue_state $repo 2)" = OPEN ] || fail "issue #2 was closed, though the user wanted it left for later"
check_clean $repo
exit $status
