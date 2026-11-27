# Agent harness best practices

Distilled from ~150 talks and videos (Anthropic and the Claude Code team, AI Engineer 2026, Lauren Tan, Matt Palmer, ThePrimeTime, Lucas Montano and others), 25 papers and Anthropic's own writing, June to November 2026. Model names and numbers reflect that period; re-check them when new models ship.

The one idea behind almost everything here: **generating code is cheap; what limits results is how well the agent can verify its own work, and whether each correction becomes an automatic check.**

---

## 1. Principles

1. **Mechanisms over instructions.** A rule the agent must remember will be forgotten. A hook, a lint rule, a test or a permission is not.
2. **Verification is the bottleneck.** Give the agent a way to run the system and a pass/fail signal, and ask for evidence. The Claude Code team estimates this alone gives 2 to 3 times better results.
3. **Less context, better context.** Short instruction files, small skills with clear triggers, curated memory. Irrelevant context makes tasks that used to work fail.
4. **Deterministic where possible, model where needed.** Use scripts to collect, filter and validate; use the model to understand, decide and write.
5. **Re-check on every model change.** What helped an older model can hurt a newer one. Re-run your baseline and prune.

---

## 2. Instruction files (CLAUDE.md, AGENTS.md, copilot-instructions)

- Keep only what the agent cannot learn by reading the repo: decisions and their reasons, traps that bit before, environment quirks, who owns what. Build commands visible in `package.json` or a `.csproj` do not need repeating.
- Start nearly empty and add a line only when the same correction was needed more than once.
- Target under ~100 lines. A 2026 study found larger AGENTS.md files did not improve task success.
- Put area-specific rules in scoped files (`.claude/rules/<area>.md` with `paths`) instead of one long file.
- Remove old-model scaffolding: ALL CAPS, stacks of IMPORTANT/NEVER, "think step by step", ritual verification steps. Newer models over-apply them and get overly cautious.
- When a rule mentions a cost or a "never", give both sides of the trade-off ("prefer X because Y; Z is fine when W").
- Multiple tools on one team: keep one source file in plain markdown and point the others to it.
- Audit at each model release (agent-config-review skill).

## 3. Skills

- A skill is a procedure loaded only when relevant: the agent sees every skill's name and description at session start and loads the body when a request matches. The **description decides triggering**: write it as "Use when..." in the user's words.
- Keep the body under 500 lines; move examples, references and scripts into side files. In a study of 138,000 SKILL.md files, about 92% had defects; the most common were no trigger guidance, oversized files and too many inline examples.
- Put the details the model does not know. Models already know most general concepts in a typical skill but only a minority of the exact details; test with and without the skill and cut what it already knows.
- Prefer a script inside the skill for anything that must be exact. Instructions that come from a script's output are followed more reliably than rules in prose.
- Number the steps so skipped steps are visible, and end with an output or verification section.
- Version skills in git; use the open SKILL.md standard so Claude Code, Copilot and Devin can share them (`~/.claude/skills`, `~/.agents/skills`, `.github/skills`, `.agents/skills`).
- Third-party skills are dependencies: read their scripts and hooks before installing (agent-instructions-audit).
- Let skills grow from real work: when a hard task succeeds, distill the procedure; when a skill fails in use, update it with a reviewed diff. Lint them regularly (skill-audit).

## 4. Subagents

Use a subagent for one of three reasons, not for "a better answer":
1. **Clean context**: a reviewer or verifier that must not see the author's reasoning.
2. **Parallelism**: independent tasks fanned out, ideally each in its own worktree.
3. **Noise isolation or cost**: searching, reading logs, exploring a big codebase on a cheaper model, returning only conclusions.

Give read-only subagents read-only tools. Keep their output short (conclusions plus file:line). A strong model planning or orchestrating with cheaper models executing is a common, cost-effective split.

## 5. Hooks and permissions

- **Exit code 2 blocks** and sends stderr back to the agent so it fixes the issue. Exit code 1 is a non-blocking error: the task can still be marked done. Check this in every verification hook.
- Typical set:
  - after edits: format and lint only the changed file
  - before finishing (Stop): run tests for the touched area
  - before shell commands: block destructive or out-of-scope commands
- Deny rules for anything irreversible (pushing to main, production profiles, reading `.env`, applying DB migrations). They are evaluated before auto-approval modes.
- Commit shared hooks and settings to the repo so the team gets them; keep personal tweaks in local, uncommitted settings.
- Keep hooks fast and scoped, or people disable them.
- Hooks are a safety net, not a sandbox. Untrusted code runs in a sandbox with restricted network.
- See the verification-hooks skill for templates.

## 6. MCP servers and connections

- Add an MCP server when it gives the agent something a CLI or a plain file cannot, or when several clients must share the same tool. If a good CLI exists, a skill that calls the CLI usually costs less context.
- Tool output should be lean: deduplicated, markdown, only needed fields. One team cut tokens by 66% to 77% with better accuracy just by trimming tool output.
- Fewer, well-designed tools beat large catalogs. Reducto, for one, deleted its MCP server and rebuilt it around tasks instead of mirroring every API endpoint.
- Treat third-party MCP servers like any dependency: pin versions, review what they can reach, prefer official sources.
- Least privilege: read-only tokens by default, short-lived credentials, secrets referenced by name and never shown to the model.
- In companies, route agents through a gateway with central auth, a reviewed tool list, human approval for writes, audit logs and filtering of sensitive data (patterns shown by Monzo and Credit Karma in 2026).

## 7. Models, effort and cost

- Change effort before changing model. With Claude Opus 5.5 the Claude Code team recommends medium as the default; benchmarks showed little gain above high. Raise it for cross-cutting changes, hard bugs in unfamiliar code and schema changes.
- A strong model at low effort often beats a weak model at high effort, and can cost less.
- Do not switch effort or model mid-way through a long conversation: it invalidates the prompt cache. Watch cache hit rate; fixing cache use alone saved up to 72% for one team.
- Keep system prompts and instruction files stable so they stay cached.
- When results are poor, change things in this order: better verification, one step more effort, a bigger model.
- Measure cost per task, not per token, on a small golden set of your own tasks before switching providers or models.

## 8. Verification

- Every task gets acceptance criteria, including **what must not change**.
- The agent runs the real thing (service, endpoint, UI via a browser tool, job) and shows command and output per criterion (verify-work skill).
- Keep a `docs/feature-map.md`: how to start each service, test data, the path to each feature.
- Errors must surface as errors: "access denied", empty or zero where data was expected is a failure.
- Never let tests call paid or production services.
- Test quality matters more than count: most agent-written tests in one study did not assert on output values. Assert on outputs, use property tests for rules that are laws, and check tests fail when behavior breaks (mutation).
- In CI, a quality ratchet (no metric may get worse) lets you accept agent PRs without line-by-line reading of everything (quality-ratchet skill).

## 9. Code review

- Review in a clean context, ideally with a different model than the author; the same model shares its blind spots.
- Several independent passes, keep the findings that survive, ignore the commit message as evidence (an LLM reviewer approved vulnerable code with an innocent message 88% of the time in one test, humans 35%).
- Human review quality drops above about 400 changed lines: plan work in phases the size of a reviewable PR.
- Always human: database migrations, public contracts, financial calculations, auth.
- Turn repeated review comments into checks; the review shrinks over time.
- Ask the agent to explain every business rule it added, with file:line, so the human can review intent instead of every line.

## 10. Specs and requirements

- Let the agent interview you with multiple-choice questions until acceptance criteria are testable (spec-interview skill).
- Value is in human-approved acceptance criteria tied to tests; long specs cost 40% to 130% more tokens and are rarely read.
- Look for spec bugs before coding: conflicting rules, states with no rule, ambiguous terms.
- Implement in a fresh session starting from the spec.

## 11. Long-running and autonomous work

Before letting an agent run unattended, answer five questions: what is "done", how does it check itself, what can it access, what are the limits (turns, budget, time), and who approves at the end.

- Give an explicit stop rule ("stop only if blocked or before anything destructive").
- Keep progress in a `TASKS.md` so it survives context compaction.
- Agents with strong goals take shortcuts that only a repo rule forbids. Put constraints in checks and permissions, and keep a "do not" list with shortcuts already tried.
- More parallel agents is not automatically better: several practitioners reported they stopped reviewing properly. Scale parallelism only as fast as verification.

## 12. Memory

- Write memory quickly during work, then consolidate periodically outside the session: deduplicate, remove stale items, mark confirmed ones, review the diff ("dreaming").
- Irrelevant memory makes previously working tasks fail; curation beats volume.
- Keep a friction log (what slowed the agent down) and a corrections log; triage them weekly into docs, scripts, checks or skills.
- Rules that are critical do not live in memory notes; they become code with state, idempotency and audit.

## 13. Security

- Instruction files (CLAUDE.md, AGENTS.md), skills, MCP servers and code comments are an attack surface. Real attacks in 2026 used malicious CLAUDE.md files, skills and MCP servers, and an AGENTS.md from one project leaked into a PR for another.
- "Run the tests" in an untrusted repo is one of the riskiest tasks: test and install scripts run arbitrary code. Audit before running (agent-instructions-audit) and use a sandbox.
- Security rules in the prompt raise warnings but do not stop attacks. Enforcement goes in permissions, sandboxing and network limits.
- AI-found vulnerabilities need human triage; many "confirmed" findings do not hold up.
- Keep git clean before risky operations so everything can be reverted.

## 14. Legacy code and upgrades

- Extract the functional spec before changing legacy code, including implicit behavior in config, database and neighbor modules (legacy-spec-extraction).
- Backfill characterization tests before refactoring (legacy-test-backfill).
- For version upgrades, read official breaking changes first, freeze a baseline, verify differentially (same inputs, old vs new), and keep a lessons file for the next upgrade (version-upgrade).
- Map who consumes an API before changing it (api-change-impact).

## 15. Teams and adoption

- Start where risk is low and value is visible: questions about legacy code, git archaeology, test backfill, explainers.
- Make skeptics and senior engineers owners of where AI is and is not allowed.
- PR descriptions keep a human-written part at the top.
- Measure human touches until the agent gets it right; it is a number managers understand.
- Retros discuss failures of the system (missing check, missing context), not of people.

---

## Setup checklist

Repo level:
- [ ] Short instruction file with only what the code does not say
- [ ] `docs/feature-map.md` explaining how to run and reach each feature
- [ ] Test and lint commands the agent can run locally
- [ ] Hooks: format after edit, tests before finishing, guard on shell commands (exit code 2)
- [ ] Deny rules for irreversible actions
- [ ] Review step in a clean context before human review
- [ ] Quality ratchet or equivalent gates in CI
- [ ] Shared settings and hooks committed

Machine level:
- [ ] Global rules file (see `templates/global-rules.md`)
- [ ] Skills installed where every tool you use can find them
- [ ] Subagents for review, verification and exploration
- [ ] MCP servers reviewed, pinned and least-privilege
- [ ] Periodic memory consolidation and skill lint

---

## Sources

- Anthropic: [Migrating the Messages API to Rust](https://www.anthropic.com/research/migrating-api-to-rust), [Components of agent memory](https://www.anthropic.com/research/components-of-agent-memory), [How the Claude Code team thinks about verification](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/), [Solving code review at Anthropic](https://claude.dev/blog/solving-code-review-at-anthropic/), [Getting the most out of Opus 5.5](https://claude.dev/blog/getting-the-most-out-of-opus-5-5), [Claude Code best practices](https://code.claude.com/docs/en/best-practices), [How we use skills](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills)
- Talks (YouTube): [Rethinking Claude Code Best Practices, Lydia Hallie](https://youtu.be/vlfCjWuv4es), [All Code Is Slop (Except Mine), Lauren Tan](https://youtu.be/O_zcc6Xl12g), [The Dark Arts of Skill Engineering, Paul Bakaus](https://youtu.be/SQMCtZX3trg), [Building verification loops in Claude Code](https://youtu.be/mQZB0l-rhxE), [Tool, skill, or subagent?](https://youtu.be/mWvtOHlZM-I), [A Bank Built Its Own Coding Agent, Monzo](https://youtu.be/adfw3xJBx1o), [225,000 Lines of Tests, Duolingo](https://youtu.be/D_4Rn6uLdQM)
- Papers: [Harness design for coding agents](https://huggingface.co/papers/2609.20804), [138K SKILL.md files](https://arxiv.org/pdf/2608.08453), [Oracle signals in agent-written tests](https://arxiv.org/html/2606.18168v1), [Contract-grounded test generation](https://arxiv.org/pdf/2608.17177), [Agentic code review in the wild](https://arxiv.org/abs/2607.03316), [Legacy modernization with coding agents](https://arxiv.org/pdf/2608.28972)
