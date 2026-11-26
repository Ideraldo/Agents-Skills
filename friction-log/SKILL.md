---
name: friction-log
description: "Use in any agent coding session to record what was broken, confusing or slow (missing docs, failing setup, unclear rules, permission walls), and weekly to triage the log into fixes: a doc line, a script, a check, a skill or a permission. Use when the user asks 'what keeps slowing the agent down?' or wants the harness to improve over time."
---

# Friction log

Agents hit the same walls over and over: the service that needs a magic env var, the test that only runs with a flag, the rule nobody wrote down. Cursor's team and the GrokBot team (2026) both run a version of this loop: the agent writes down friction as it happens, a human triages it, and fixes are validated before they land.

## Part 1: during any session

When something costs more than a couple of minutes or a retry, append one line to `docs/agent-friction.md`:

```
YYYY-MM-DD | <area> | <what happened, one sentence> | <what would have avoided it> | <type: setup / docs / permission / tooling / knowledge>
```

Keep going with the task afterwards. Do not stop to fix the friction unless it blocks the task.

## Part 2: weekly triage

1. Read the log since the last triage. Group lines with the same cause.
2. For each group, pick the cheapest durable fix:
   - knowledge missing: a line in CLAUDE.md or a `feature-map.md` entry
   - repeated steps: a script or a skill
   - repeated mistake: a check (see correction-to-check)
   - permission walls: adjust permissions, or document why they stay
   - setup pain: a dev container, a make target, a seed script
3. Propose the fixes as a list with effort (small, medium, large) and wait for approval.
4. After a fix lands, verify it by having a fresh session do the task that hit the friction. Only then mark the group as fixed in the log.

## Rules

- One line per friction; no essays.
- Never put secrets or values of env vars in the log, only their names.
- A fix is not done until a fresh session confirms it.

## Output

Part 1: the appended line. Part 2: grouped causes, proposed fixes with effort, and what was verified.
