---
name: skill-audit
description: "Use when creating, reviewing or publishing an Agent Skill (SKILL.md), when a skill triggers at the wrong time or not at all, or periodically over a whole skills repository. Runs a static lint (trigger, size, verification step, portability, secrets), then an optional with/without test to cut what the model already knows."
---

# Skill audit

Most public skills are broken in boring ways: a 2026 study of 138,000 SKILL.md files found about 92% with defects. The most common were no "use when" trigger, files over 500 lines, too many inline examples, and no verification step. Another talk measured that models already know about 70% of the general concepts in a typical skill but only 22% of the exact details. A skill should carry the details.

## Inputs

- One skill folder, or a repo with many.

## Steps

1. **Static lint.** Run `python3 scripts/lint_skills.py <path>` (no dependencies). It checks:
   - frontmatter has only portable keys (`name`, `description`, plus a few widely supported ones) and `name` matches the folder
   - description says when to use it ("Use when", "Use whenever", "Use before"...) and is 30 to 1024 characters
   - body under 500 lines
   - has a verification or output section
   - no obvious secrets, personal paths (`/Users/...`, `C:\Users\...`) or hardcoded model names
2. **Read for judgment**, which no script catches:
   - Does the description trigger on the user's words, not on the skill's internal jargon?
   - Are hard rules enforced by a script or hook where possible, instead of prose?
   - Are steps numbered, so a model that skips steps is visible?
   - Is anything there because an older model needed it ("think step by step", CAPS, repeated warnings)? Remove it.
3. **Novelty test (optional, costs tokens).** Write 10 to 20 questions whose answers are in the skill. Ask them in a fresh session without the skill, then with it. Cut sections the model already answers correctly without it; keep and sharpen what only the skill knows.
4. **Trigger test (optional).** Write 5 prompts that should trigger the skill and 5 near-misses that should not. Check which fire.

## Rules

- Do not rewrite a skill's meaning while auditing; propose changes as a diff.
- For a public repo, flag anything personal or company-specific and suggest moving it to a private version.

## Output

Per skill: lint results, judgment notes, proposed diff, and (if run) novelty and trigger results.
