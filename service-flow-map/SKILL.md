---
name: service-flow-map
description: Maps a distributed system (microservices, front end, workers, queues, databases) into versioned JSON and an interactive visual that animates a data flow from a UI click to the last database write. Use when the user wants to document or understand how services connect across many repositories.
---

# Interactive map of a distributed system

The goal is documentation that is as visual as possible: an interactive diagram showing what each part does, who uses each service and where the data goes, including an animation of the path a piece of data takes from a click on screen to its last write in a database.

It works in phases, starts with the repositories the user knows best and expands in waves. It is built for codebases where table, column, service and queue names are cryptic abbreviations, and for teams that need to save tokens.

## Before starting, ask the user

1. Which folder holds the cloned repositories.
2. Which two repositories to start with (ideally a back-end service and the front end they know best).
3. The first flow to animate and its entry point (screen, button or endpoint).
4. Which documentation skills are available in this session and what each one produces (see "Documentation skills").
5. Whether supporting files already exist: database schema dump, a distributed trace of a real run, list of queues and topics.
6. Which models can be used for sub-agents.

Do not read service code before the user answers.

## Rules for everything

- **Never translate or interpret abbreviations.** Table, column, service and queue names stay exactly as they appear in code. Their meaning gets filled in later by people on the team, in a glossary.
- **Only record what was seen in code.** Every item carries `evidencia` (file and line). Anything deduced carries `"status": "inferido"`.
- Everything you produce goes to files under `mapa/`. In chat, only short summaries.
- **Token economy is a requirement.** Prefer scripts and grep over reading code with a model whenever the result is the same.

## Phase 1: inventory without AI

Write and run a script (no model reading code) that walks every cloned repository and generates `mapa/inventario.json` with:

- One node per repository: name, language, type (`api`, `worker`, `front`, `lib`), entry points (controllers, consumers, scheduled jobs).
- Links found by text search: queue and topic names (who publishes, who consumes), URLs or clients of other services, table names in ORM mappings (DbContext, entity configurations, models), raw queries and connection strings.

At the end, show a summary: how many nodes, how many links, and what could not be detected by script.

## Phase 2: pilot on the first back-end service

You are the orchestrator. You don't read service code: you delegate, read summaries and consolidate.

- Create ONE sub-agent for the first back-end repository. It follows only the chosen flow from its entry point, without exploring the rest.
- Limit of 40 files read per sub-agent. If it needs more, it stops and reports why.
- No sub-agents inside sub-agents.
- If you can pick models, use a mid-tier or cheaper model for sub-agents (their job is reading and extraction) and the strongest model only for the orchestrator.
- The sub-agent writes `mapa/servicos/<servico>.json` and returns at most 10 lines: steps found, outputs to other services, and doubts.

**MANDATORY STOP:** when the pilot is done, show the summary, the tokens or credits used so far and the estimate for the next services. Continue only after the user confirms.

## Phase 3: front end and first animated flow

- One sub-agent for the front end: from the screen and button to the HTTP call, with the fields sent.
- Consolidate front end and the first service into `mapa/fluxos/<fluxo>.json`, with steps in global order.

## Phase 4: expansion in waves

- The reported outputs (published events, HTTP calls) and the inventory links define the next wave of services.
- One sub-agent per service, at most 3 in parallel.
- No sub-agent for a service that never appeared in a flow. Those stay at the shallow inventory level.
- Before each wave, say how many services it includes and ask for confirmation.

## Documentation skills

If documentation-generating skills are available, before Phase 2:

- List them, say what each produces (markdown, README, Mermaid or C4 diagram, other) and propose how they fit the plan.
- Preferred: a single pass. The same sub-agent that reads the code uses the skill to write the text documentation AND writes the structured JSON, so the same code is never read twice.
- Fallback, if the skill can't be combined: run the skill as is, then a light sub-agent that reads only the generated markdown (not the code) and extracts the JSON.
- If a skill generates a diagram, use it to cross-check the map and list the differences.

The text documentation feeds the description of each service in the visual.

## Output formats and the visualizer

- JSON formats for services, flows, glossary and doubts: `references/output-formats.md`
- Visualizer specification (Phase 5, after the pilot is validated): `references/visualizer.md`

## Validation and maintenance

- List in `mapa/duvidas.md` everything that needs human checking. The user validates by diffing the tables in a development environment (before and after running the flow) and against a real trace, then changes steps to `"confirmado"` and the service to `"validado"`.
- The JSONs are versioned. At the end, write `mapa/README.md` explaining how to add a new service or flow and how to update the glossary.

## Definition of done for the first delivery

Inventory of every repository in the overview map, the first back-end service and the front end mapped in depth, one end-to-end animated flow, the glossary generated and the list of doubts.
