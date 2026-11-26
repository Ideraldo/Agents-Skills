---
name: explain-in-html
description: "Use when someone needs to understand one complex piece of code fast (a module, a request flow, a tricky class) before changing or reviewing it, or asks for an explainer, walkthrough or onboarding page. Produces one self-contained HTML page with a flow diagram, 3 to 5 annotated code excerpts and a 'gotchas' section. For mapping a whole multi-repo system, use service-flow-map instead."
---

# Explain in HTML

A single page that explains one thing well. The Claude Code team and several 2026 creators use HTML explainers instead of long markdown because a diagram plus annotated excerpts is read; a wall of text is not.

## Inputs

- What to explain: file, class, endpoint, or "what happens when the user clicks X".
- Who will read it: new team member, reviewer, the user themselves.

## Steps

1. **Trace the flow** in the code. Keep a list of steps with `file:line`.
2. **Pick 3 to 5 excerpts** that carry the logic (not boilerplate). Max about 25 lines each.
3. **Write the page** with these sections, in order:
   1. One-paragraph summary: what it does and why it exists.
   2. Flow diagram: inline SVG or Mermaid (rendered via the Mermaid CDN script) showing the steps and where data goes.
   3. Annotated excerpts: each excerpt with numbered callouts explaining the non-obvious lines.
   4. Gotchas: implicit behavior, ordering assumptions, things that broke before (check `git log`), config that changes behavior.
   5. Where to look next: related files with paths.
4. **Check it renders**: open it in a browser or screenshot it if a browser tool is available, and fix layout issues.

## Rules

- One file, no build step, no external assets except a pinned CDN script for Mermaid if used.
- Every claim about behavior points to `file:line`.
- No secrets, real customer data or internal hostnames in the page.
- Plain, readable styling: system font, max width about 900px, code in monospace with line numbers.
- Keep prompts and notes for agents in markdown; HTML is for humans.

## Output

`docs/explainers/<topic>.html` and a one-line summary of what it covers.
