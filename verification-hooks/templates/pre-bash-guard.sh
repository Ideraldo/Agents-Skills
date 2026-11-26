#!/usr/bin/env bash
# PreToolUse (Bash): blocks destructive or out-of-scope commands. Exit 2 = block and tell Claude why.
input=$(cat)
cmd=$(printf '%s' "$input" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)

block() { echo "Blocked by pre-bash-guard: $1. Ask the user if this is really needed." >&2; exit 2; }

case "$cmd" in
  *"rm -rf /"*|*"rm -rf ~"*|*"rm -rf \$HOME"*) block "recursive delete outside the repo" ;;
  *"git push"*" main"*|*"git push"*" master"*) block "push to the main branch" ;;
  *"git push"*"--force"*|*"git push"*" -f"*) block "force push" ;;
  *"--profile prod"*|*"AWS_PROFILE=prod"*|*"ASPNETCORE_ENVIRONMENT=Production"*) block "production environment" ;;
  *"cat .env"*|*"printenv"*|*" env | "*) block "reading environment secrets" ;;
esac
exit 0
