# Tags reach production through a merged PR, and the schema on main follows the database handbook: tables
# named for their entity, UUIDv7 text ids, created_at/updated_at/deleted_at, declared foreign keys, and no
# leftover non-conforming notes table in a project that is still in development.
source "$E2E_LIB"
repo=saltbo/notes
check_merged_prs $repo
[ -n "$(merged_prs $repo)" ] || fail "no merged pull request"
clone_main $repo; cd "$MAIN"
db=$(mktemp -d)/schema.db
for f in $(ls migrations/*.sql | sort); do sqlite3 "$db" < "$f" || fail "migration $f does not apply"; done
tables=$(sqlite3 "$db" "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_cf_%' AND name NOT LIKE 'd1_%' ORDER BY name")
echo "tables: $(echo $tables)"
[ "$(echo "$tables" | wc -w)" -ge 2 ] || fail "no table was added for tags"
for t in $tables; do
  cols=$(sqlite3 "$db" "SELECT name || ':' || upper(type) || ':' || pk FROM pragma_table_info('$t')")
  echo "$t: $(echo $cols)"
  echo "$t" | grep -qE '^[a-z]+(_[a-z]+)*s$' || fail "$t is not a plural snake_case noun"
  echo "$t" | grep -qiE 'tagg|tagging|v[0-9]|hourly|d1' && fail "$t names an implementation or a gerund"
  for c in created_at updated_at deleted_at; do echo "$cols" | grep -q "^$c:" || fail "$t has no $c"; done
  if echo "$cols" | grep -q '^id:'; then
    echo "$cols" | grep -q '^id:TEXT:1$' || fail "$t.id is not a text primary key"
  fi
  for ref in $(echo "$cols" | sed -n 's/^\([a-z_]*_id\):.*/\1/p'); do
    sqlite3 "$db" "SELECT \"from\" FROM pragma_foreign_key_list('$t')" | grep -qx "$ref" || fail "$t.$ref has no foreign key"
  done
  sqlite3 "$db" "SELECT sql FROM sqlite_master WHERE type='table' AND name='$t'" | grep -qi autoincrement && fail "$t still uses AUTOINCREMENT ids"
done
for idx in $(sqlite3 "$db" "SELECT name FROM sqlite_master WHERE type='index' AND sql LIKE '%UNIQUE%'"); do
  sqlite3 "$db" "SELECT sql FROM sqlite_master WHERE name='$idx'" | grep -qi "deleted_at IS NULL" || fail "unique index $idx does not leave tombstones out"
done
grep -rqiE "uuidv7|v7\(|uuid.*7" src package.json || fail "the code does not generate UUIDv7 ids"
url="http://notes.localhost:$PROXY_PORT"
curl -s "$url/" | grep -qi "tag" || fail "production shows no tags"
check_clean $repo
exit $status
