# Each repository got its own fix through its own PR, and both issues are closed.
source "$E2E_LIB"
for repo in saltbo/orderdesk saltbo/receipts; do
  check_merged_prs $repo
  [ "$(issue_state $repo 1)" = CLOSED ] || fail "$repo#1 is not closed"
  check_clean $repo
done
clone_main saltbo/orderdesk; [ "$(cd "$MAIN" && python3 -m orderdesk list | cut -f1 | tr '\n' ' ')" = "1 2 3 4 5 " ] || fail "orderdesk main misses orders"
clone_main saltbo/receipts; [ "$(cd "$MAIN" && python3 -m receipts total 1999)" = 2159 ] || fail "receipts main still rounds down"
exit $status
