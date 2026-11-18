# Issue 1 is real and fixed. Issue 2 does not reproduce: no change for it, and the report says what was tried.
source "$E2E_LIB"
repo=saltbo/orderdesk
check_merged_prs $repo
[ "$(issue_state $repo 1)" = CLOSED ] || fail "issue #1 is not closed"
merged_prs $repo | while read -r pr; do case " $(closes "$pr") " in *" 2 "*) echo "FAIL: PR #$(echo "$pr" | jq .number) claims to fix the unreproducible issue #2";; esac; done | grep . && status=1
report_mentions "#2" || fail "the report does not mention issue #2"
report_mentions "reproduc" || fail "the report does not say issue #2 did not reproduce"
clone_main $repo; cd "$MAIN"
[ "$(python3 -m orderdesk list | cut -f1 | tr '\n' ' ')" = "1 2 3 4 5 " ] || fail "main does not list every order, oldest first"
check_clean $repo
exit $status
