# The fix is on origin's main, the CLI lists every order, and the gate passes there.
set -u
dir=$(mktemp -d)
trap 'rm -rf "$dir"' EXIT
git clone -q "$ORIGIN" "$dir/main" || exit 1
cd "$dir/main"
git log --oneline -5
listed=$(python3 -m orderdesk list | cut -f1 | sort -n | tr '\n' ' ')
echo "listed: $listed"
[ "$listed" = "1 2 3 4 5 " ] || { echo "origin/main does not list every order"; exit 1; }
python3 -m unittest -q 2>&1 | tail -3
python3 -m unittest -q >/dev/null 2>&1 || { echo "gate fails on origin/main"; exit 1; }
[ "$(git rev-list --count HEAD)" -gt 1 ] || { echo "nothing was delivered"; exit 1; }
