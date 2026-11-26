---
name: legacy-spec-extraction
description: "Use before changing, rewriting or migrating an existing service or module you don't fully understand, or when the user asks 'what does this service actually do?'. Extracts a language-agnostic functional spec (inputs, outputs, validations, events, business rules, implicit behavior) from the code, with file:line for each rule, and lists open questions for the team."
---

# Legacy spec extraction

Agents working on legacy code fail on the implicit: rules spread across modules, behavior in config or stored procedures, side effects nobody wrote down. Extracting the spec first, and having a human confirm it, is what helped most in 2026 modernization studies and talks (GEICO, Lucas Montano's "RFC first", the VB6 to .NET 10 study).

## Inputs

- The service, module or flow to document (repo path, entry point, or "from button X to table Y").
- Optional: tickets, old docs, people who know it.

## Steps

1. **Map the edges**: entry points (HTTP endpoints, consumers of queues/topics, scheduled jobs, UI actions) and exits (DB writes, published events, outgoing calls, files).
2. **For each entry point, trace the flow** and record:
   - inputs with types and constraints
   - validations and the exact error returned
   - business rules (each as one sentence)
   - state changes and side effects
   - outputs and events emitted
3. **Hunt the implicit**: defaults in config, feature flags, DB constraints and triggers, stored procedures, serializer settings, culture/timezone/decimal handling, retries and idempotency, ordering assumptions.
4. **Cite everything.** Each rule gets `file:line`. If a rule is inferred and not seen in code, mark it "inferred".
5. **List contradictions and dead code** found on the way.
6. **Write open questions** for the team: rules that look like bugs, behavior with no clear reason.

## Rules

- Describe behavior, not implementation. Someone should be able to reimplement it in another language from the spec.
- Never "clean up" a rule while documenting it. If it looks wrong, document it as is and add a question.
- Do not paste secrets, real customer data or internal hostnames into the spec.
- Prefer scripts (grep, AST tools) for inventory and the model for interpretation, to save tokens.

## Output: `docs/spec/<service>.md`

```
# <Service> functional spec
Scope: ...   Extracted from commit: <sha>

## Entry points
| Kind | Name | Input | Output | Source |

## Rules
- R1 <rule> (src/x.cs:120)
- R2 <rule> (inferred: ...)

## Side effects and events
## Implicit behavior
## Contradictions / suspected bugs
## Open questions
```
