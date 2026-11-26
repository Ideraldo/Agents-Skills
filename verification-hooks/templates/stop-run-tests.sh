#!/usr/bin/env bash
# Stop: run tests before Claude is allowed to finish. Exit 2 = keep working, with the failures as feedback.
input=$(cat)
active=$(printf '%s' "$input" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("stop_hook_active",False))' 2>/dev/null)
[ "$active" = "True" ] && exit 0   # avoid an endless loop: only one forced retry per stop
cd "$CLAUDE_PROJECT_DIR" || exit 0

changed=$(git diff --name-only HEAD 2>/dev/null; git ls-files --others --exclude-standard 2>/dev/null)
[ -z "$changed" ] && exit 0

if echo "$changed" | grep -q '\.cs$'; then
  out=$(dotnet test --nologo --verbosity quiet 2>&1) || { echo "dotnet test failed. Fix before finishing:" >&2; echo "$out" | grep -E "Failed|error" | head -30 >&2; exit 2; }
fi
if echo "$changed" | grep -qE '\.(ts|js)$' && [ -f package.json ]; then
  out=$(CI=true npm test --silent 2>&1) || { echo "npm test failed. Fix before finishing:" >&2; echo "$out" | tail -30 >&2; exit 2; }
fi
exit 0
