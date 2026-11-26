---
name: version-upgrade
description: "Use when upgrading a runtime, framework or dependency version (.NET 8 to 10, Angular major versions, Node, NuGet or npm packages, Docker base images), or when reviewing a PR that does. Looks up official breaking changes, plans the upgrade in reviewable steps, proves behavior did not change with differential checks, and keeps a lessons file for the next upgrade."
---

# Version upgrade

Upgrades fail at the edges: implicit behavior, neighbor modules and tests that quietly got weaker. This skill makes the agent read the official breaking changes first and prove, by running old and new side by side, that behavior stayed the same.

Based on: Anthropic's migration of its Messages API to Rust (differential verification, checkpoints, weakened asserts in ported tests), Spotify's fleet migrations (agent applies, CI verifies), Factory (a lessons file cut human involvement 90% on the second migration), Exa (models are about 6 months behind on release notes), and a 2026 case study of VB6 to .NET 10 (92% equivalence on simple features, 47% on complex ones).

## Inputs

- Current and target versions.
- The repos or projects in scope.
- `docs/upgrade-lessons.md` from previous upgrades, if it exists. Read it first.

## Steps

1. **Read the official sources, never memory.** Fetch the vendor's breaking-changes list and migration guide for every version hop (for example .NET "breaking changes in .NET 9" and "in .NET 10"; Angular's update guide for each major; package CHANGELOGs). Your training data is likely older than the release.
2. **Inventory what is affected**: target framework settings, package versions, APIs used that are listed as changed, config keys, serializer behavior, build images, CI. Output a table: item, where, breaking change, action.
3. **Freeze a baseline before changing anything.**
   - Run the full test suite and save results.
   - Record reference outputs: call key endpoints or run key jobs with fixed inputs and save the responses (golden files).
   - Note warnings count, build time, image size.
4. **Plan steps the size of a reviewable PR**: one hop or one area per step, each with its own check. For a fleet of services, apply the same step to each and let CI verify.
5. **Apply a step, then verify differentially.**
   - Same tests: compare pass/fail with the baseline.
   - Same inputs: compare responses with the golden files. Investigate every difference, even "harmless" ones (date formats, null handling, ordering, decimal precision).
   - Check ported or edited tests for weakened assertions (fewer asserts, wider tolerances, removed cases, new skips).
6. **Repeat per step.** Stop and report if a difference cannot be explained.
7. **Update `docs/upgrade-lessons.md`** with every gotcha found: symptom, cause, fix. This is the most reusable output.

## Rules

- Never bump a version without having read its breaking changes from the official source in this session.
- Never "fix" a failing test by changing its expected value unless you can show the old expectation relied on the old version's bug, and say so explicitly.
- Keep behavior changes and version changes in separate commits.
- Database migrations, public API contracts and financial calculations always get a human reviewer.
- For a PR review, run steps 1, 2 and 5 against the PR and report gaps.

## Output

1. Breaking-changes table with sources (links).
2. Step plan.
3. Per step: diff summary, differential check results, unexplained differences.
4. Lessons added.
