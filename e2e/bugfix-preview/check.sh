# The fix went through a PR with green CI and a preview, and production lists the newest note first.
source "$E2E_LIB"
repo=saltbo/notes
check_merged_prs $repo
[ "$(issue_state $repo 1)" = CLOSED ] || fail "issue #1 is not closed"
branch=$(merged_prs $repo | head -1 | jq -r .head)
previews=$(jq --arg r "$repo" --arg b "$branch" '[.repos[$r].deployments[] | select(.branch==$b and .target=="preview" and .ok)] | length' "$STATE")
[ "$previews" -ge 1 ] || fail "the fix never had a working preview"
url="http://notes.localhost:$PROXY_PORT"
for body in "older e2e note" "newer e2e note"; do curl -s -X POST "$url/api/notes" -H 'content-type: application/json' -d "{\"body\":\"$body\"}" >/dev/null; sleep 1; done
first=$(curl -s "$url/api/notes" | jq -r '.notes[0].body')
echo "production lists first: $first"
[ "$first" = "newer e2e note" ] || fail "production does not list the newest note first"
check_clean $repo
exit $status
