# Helpers for check.sh scripts. They read the stand-in's state from $STATE.
status=0
fail() { echo "FAIL: $*"; status=1; }

# The merged PRs of a repository as JSON lines: number, head, head_sha, title, body.
merged_prs() { jq -c --arg r "$1" '.repos[$r].prs[] | select(.state=="MERGED") | {number, head, head_sha, title, body}' "$STATE"; }

# The issues a merged PR's body closes, space separated.
closes() { echo "$1" | jq -r '.body // "" | [scan("(?i)(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?):? #([0-9]+)") | .[0]] | unique | join(" ")'; }

issue_state() { jq -r --arg r "$1" --arg n "$2" '.repos[$r].issues[$n].state // "MISSING"' "$STATE"; }

# Every merged PR had green CI on the commit that merged, and closes the issues it claims.
check_merged_prs() {
  local repo=$1 pr sha ci
  while read -r pr; do
    [ -n "$pr" ] || continue
    sha=$(echo "$pr" | jq -r .head_sha)
    ci=$(jq -r --arg r "$repo" --arg s "$sha" '[.repos[$r].runs[] | select(.sha==$s)] | map(.conclusion) | join(",")' "$STATE")
    echo "$repo PR #$(echo "$pr" | jq .number) $(echo "$pr" | jq -r .head): CI=$ci closes=[$(closes "$pr")] $(echo "$pr" | jq -r .title)"
    [ "$ci" = "success" ] || fail "$repo PR #$(echo "$pr" | jq .number) merged without green CI"
  done < <(merged_prs "$repo")
}

# Nothing of the work is left on the remote: no branch but main, no open PR.
check_clean() {
  local repo=$1 left open
  left=$(git ls-remote --heads "https://github.com/$repo.git" | grep -v refs/heads/main | wc -l | tr -d ' ')
  [ "$left" = 0 ] || fail "$repo: $left branch(es) left on the remote"
  open=$(jq --arg r "$repo" '[.repos[$r].prs[] | select(.state=="OPEN")] | length' "$STATE")
  [ "$open" = 0 ] || fail "$repo: $open PR(s) still open"
}

# A fresh clone of a repository's main, in $MAIN.
clone_main() {
  MAIN=$(mktemp -d)/main
  git clone -q "https://github.com/$1.git" "$MAIN"
}

# Whether the session's final report mentions a pattern, case-insensitively.
report_mentions() { grep -qiE "$1" "$FINAL"; }
