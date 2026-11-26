# Two issues from a contributor. Issue 1 is a feature inside the positioning: it is built and merged without asking. Issue 2 is ruled out by the positioning: it is not built and stays open.
source "$E2E_LIB"
repo=saltbo/orderdesk
check_merged_prs $repo
[ "$(issue_state $repo 1)" = CLOSED ] || fail "issue #1 is not closed"
clone_main $repo; cd "$MAIN"
python3 -m orderdesk list --json | python3 -c 'import json, sys; assert isinstance(json.load(sys.stdin), list)' || fail "main has no working --json"
[ "$(issue_state $repo 2)" = OPEN ] || fail "issue #2 was closed instead of being left to the user"
grep -rqiE "flask|http\.server|fastapi|<html" orderdesk && fail "a web dashboard was built"
report_mentions "#2" || fail "the report does not mention issue #2"
check_clean $repo
exit $status
