---
type: regex
target: {source: file, path: AGENTS.md}
pattern: '\b(note|important|never|make sure|remember)\b'
flags: i
match: not_contains
---
