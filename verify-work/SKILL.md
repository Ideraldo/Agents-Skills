---
name: verify-work
description: "Use when an agent finishes a code change and before calling it done, opening a PR, or asking a human to review. Runs the real system (service, API, UI), checks each acceptance criterion and each thing that must NOT change, and returns an evidence table. Also use when the user asks 'prove it works' or 'did you test it?'."
---

# Verify work

Turn "I think it works" into evidence. The agent runs the thing it changed, checks every criterion, and shows the command and output for each one. No evidence, no "done".

Why this exists: across Anthropic's Claude Code team, Lauren Tan (SpaceXAI) and most 2026 agent talks, giving the agent a pass/fail check and asking for proof was the single most repeated tip. A plausible-looking answer is not a verified one.

## Inputs

- The change (diff, branch or list of files).
- Acceptance criteria: from the task, the spec, the ticket or the user. If there are none, write them first (3 to 7 lines) and confirm with the user.
- How to run the system. Look for `docs/feature-map.md`, `README`, `Makefile`, `package.json` scripts, `*.csproj`, `docker-compose.yml`. If nothing says how, ask once and save the answer to `docs/feature-map.md` (see below).

## Steps

1. **List the criteria in two columns.**
   - Positive: what must now be true ("POST /boletos rejects negative value with 400").
   - Negative: what must NOT change ("existing contracts unchanged", "no schema migration", "other products still load").
2. **Run the cheap checks first**, in this order, stopping to fix on the first failure: build, lint/format, type check, unit tests for the touched area.
3. **Start the system** the way a developer would (local service, dev server, test container). Wait for the health check instead of sleeping a fixed time.
4. **Exercise each criterion for real.**
   - API: call the endpoint with a reference payload (curl, `.http` file, integration test). Save request and response.
   - UI: open the page with Playwright or the browser tool, do the action, take a screenshot.
   - Async/messaging: publish the message or trigger the job, then read the consumer side (log line, DB row, topic).
5. **Fix and repeat.** If a check fails, fix the code and rerun from step 2. Max 3 rounds; after that, stop and report what is blocked.
6. **Write the evidence table** (format below). Every row needs the exact command or action and the observed output, trimmed to the relevant lines.

## Rules

- Never write "tests pass" without the command and its output in the same message.
- Never mark a criterion as passed by reading the code. Reading is analysis, not verification.
- An error must surface as an error. If a call returns "access denied", empty or zero where data was expected, that is a failure, not a pass.
- Never call paid or production APIs, never use production credentials, never write to shared environments. If a criterion needs them, mark it "needs human" and say why.
- Do not weaken, skip or delete a test to make the run green. If a test is wrong, say so and leave the decision to the human.
- Label each result: **measured** (ran it), **inferred** (followed from another check) or **not checked**.

## Feature map

Keep `docs/feature-map.md` in the repo so the next run does not rediscover everything: how to start each service, required env vars (names only, never values), test data, URLs and the shortest path to each feature. Update it whenever you learn something new about running the system.

## Output

```
## Verification

| # | Criterion | Type | How checked | Result | Evidence |
|---|-----------|------|-------------|--------|----------|
| 1 | Rejects negative value | positive | POST /boletos {"valor": -1} | PASS (measured) | 400 {"error":"valor must be > 0"} |
| 2 | Existing contracts unchanged | negative | diff of OpenAPI before/after | PASS (measured) | no changes in paths/schemas |

Not checked: <items and why>
Commands run: <list>
```

Close with one line: ready for review, or blocked on <what>.
