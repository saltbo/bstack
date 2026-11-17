# The line at fault is rewritten in place, and nothing is patched on.
set -u
fail=0
lines=$(wc -l < AGENTS.md)
echo "AGENTS.md: $lines lines (was 18)"
[ "$lines" -le 19 ] || { echo "grew by more than one line"; fail=1; }
grep -q "Use the logging module for output\." AGENTS.md && { echo "the ambiguous line is still there"; fail=1; }
if grep -niE "\b(note|important|never|make sure|remember)\b|[A-Z]{4,}:" AGENTS.md; then echo "patch words above"; fail=1; fi
grep -qi "stdout" AGENTS.md || { echo "no statement of where results go"; fail=1; }
git diff --stat
exit $fail
