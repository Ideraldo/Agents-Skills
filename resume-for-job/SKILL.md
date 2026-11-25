---
name: resume-for-job
description: "Use when the user pastes a job posting and wants to know which of their resume versions to send, how to tailor it for that role, or what gaps to expect before applying."
---

# Pick and tailor a resume for a job posting

The user keeps several ready-made resume versions (for example: a generic one, one per stack, one per language). Your job is to read the posting, say which version to send, suggest only the edits worth making, and flag gaps before they spend an application on it.

Everything you are allowed to claim about the user lives in two files next to this one. Read both before answering:

- `references/variants.md`: the resume versions they have, where each file lives, and the routing rules for choosing between them
- `references/fact-inventory.md`: the audited list of facts, by role and project. **Nothing goes on a resume unless it is in this file.**

If either file still contains only the template, stop and help the user fill it in first. A resume tailored without an inventory is a resume full of plausible guesses.

## How to decide

Read the posting and extract: the main required stack, seniority, business domain, the language of the posting, and the keywords that repeat.

Then apply the routing rules in `references/variants.md` in order, first match wins. When two versions tie, pick the one that matches the **first** requirements section of the posting, not the sum of all of them. That first section is what recruiters screen on.

If the posting's seniority or location does not match what the user is looking for, say so before anything else.

## What tailoring may change

Tailor only when the role matters to the user or the posting uses vocabulary the chosen version does not mirror. Real tailoring is cheap and touches five things:

- the headline under the name
- the summary (mostly its first sentence)
- the **order** of bullets within a role, and which one drops when space runs out
- the **order** and emphasis of the skills lines
- which personal projects appear

That's it. Do not write new bullets, do not rewrite achievements, do not swap verbs to sound stronger.

## Rules that never break

- **Never add a technology that is not in the inventory.** Say it's missing instead of squeezing the keyword in.
- **Never invent or round a metric.** If the inventory says a number was a perception and not a measurement, it never becomes a number.
- **Verbs only claim what the user did.** "Designed" or "architected" only where they took part in the decisions and their design was adopted. Not where they implemented someone else's design, and not where they proposed and lost.
- **A prototype stays a prototype.** A side project with no users is never a "product" or a "SaaS with customers".
- **One page, always** (unless the user's inventory says otherwise). If something goes in, something comes out, and you tell them what came out.
- **When in doubt about a technical detail, ask before writing.** The recurring failure is filling a gap with plausible vocabulary. The test: only keep on the resume what the user can defend for two minutes under questioning.

## Known gaps

`references/fact-inventory.md` has a "Known gaps" section. When the posting asks for one of them, say it plainly and say whether applying is still worth it.

## What to answer

1. Which file to send, with its full path
2. Why that version, in one or two sentences tied to what the posting asks for
3. Edits worth making, if any, with the new text ready to paste
4. Gaps: what the posting asks for that the user doesn't have, and whether to apply anyway
5. If seniority or location don't match, say it before they apply

If the user asks you to produce the tailored file, edit the source (document or generator script), regenerate it, confirm it still fits on one page, and save it where `references/variants.md` says tailored versions go.
