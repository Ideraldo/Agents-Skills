#!/usr/bin/env bash
# PostToolUse (Edit/Write): format and lint only the changed file. Exit 2 = send lint errors back to Claude.
input=$(cat)
file=$(printf '%s' "$input" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null)
[ -z "$file" ] && exit 0
cd "$CLAUDE_PROJECT_DIR" || exit 0

case "$file" in
  *.cs)
    proj=$(dirname "$file"); while [ "$proj" != "/" ] && ! ls "$proj"/*.csproj >/dev/null 2>&1; do proj=$(dirname "$proj"); done
    [ "$proj" = "/" ] && exit 0
    dotnet format "$proj" --include "$file" >/dev/null 2>&1   # auto-fix what it can
    out=$(dotnet format "$proj" --include "$file" --verify-no-changes --severity warn 2>&1) || {
      echo "dotnet format/analyzer issues left in $file:" >&2; echo "$out" | tail -20 >&2; exit 2; } ;;
  *.ts|*.js|*.html)
    [ -x node_modules/.bin/eslint ] || exit 0
    out=$(node_modules/.bin/eslint --fix "$file" 2>&1) || { echo "eslint errors in $file:" >&2; echo "$out" | tail -20 >&2; exit 2; } ;;
esac
exit 0
