# Viewer guidelines: keeping the map readable

`visualizer.md` says what the visualizer must contain. This file says how to organize it so people can actually read it. Follow it when building the visualizer for the first time, and use it as a checklist when the user says an existing one is confusing.

The examples use a fictional online store (services `storefront`, `orders-api`, `payments-api`, `shipping-worker`; flow "place order"). Replace them with whatever the mapped system contains.

## The failure mode to avoid

Once a map covers more than a handful of services, the natural result is too many views, several of them showing the same thing in different ways, and almost all of them opening with blocks of text. The user ends up liking only the animated flow and ignoring the rest.

The cause is never missing content. It is too many entry points and no hierarchy. Three principles fix it:

1. **One view per question.** If two views answer the same question, merge them.
2. **Visual first, text on demand.** A screen opens with a picture and at most one sentence. Everything else is one click away.
3. **Never show everything at once.** A graph with every node answers no question. Show a small set and let the user expand.

## Navigation

Aim for a short top menu, in this order:

`Home | Journeys and flows | Status | Events | Data | APIs | More`

`More` holds Explore, Glossary, Impact and Tour. Keep every view's state in the URL (view, flow, scenario, step) so a screen can be shared as a link.

Do not use a gallery of cards as the landing page. A gallery of ten cards with descriptions is ten blocks of text before the first diagram.

## Home

- Left: the application map (who talks to whom), at application level only. No tables, no queues, no topics. Keep the faded style for applications with status `raso`.
- Right: the list of journeys and flows available.
- Clicking an application opens its card in a side panel: description, who uses it, what it depends on, entry points, queues and tables. There is no separate "services catalog" view; the card is the catalog.
- If there are more than about 9 applications, group them into domains (for example Catalog, Checkout, Fulfilment) and show the domains first. The grouping is a business decision: ask the user for it, do not infer it.

## One page per flow

Do not split a flow across separate views such as "flow detail", "animation" and "simple summary". Build one flow page:

- **Top:** the animation, filling the available width and height. Fit the diagram to the space on load; never open it shrunk in a corner.
- **Toggle:** a "Plain summary" button that switches to a plain-language explanation of the flow without leaving the page.
- **Below, collapsed by default:** sequence diagram, code evidence and technical details.

### Animation

- One lane per service, with each table drawn inside the lane of the service that uses it.
- Start at the user action in the front end (for example the "Place order" button in `storefront`). If the front-end origin is not in the JSONs, show a first step labelled "origin not mapped" and record it in `mapa/duvidas.md`. Do not start silently at the back end.
- Follow asynchronous hops to the end: after a write to an outbox or a publish, continue to the topic and to each consumer when the JSONs have that data (for example `orders-api` publishes `order-placed`, `shipping-worker` consumes it).
- At each step show the current business status (for example "Order: awaiting payment") and, for writes, the columns written.
- Keep the controls from `visualizer.md`: play, pause, previous, next, speed, and the side list of steps.

## Journey as the index of flows

A journey is the business process end to end, made of several flows (for example: browse, add to cart, place order, pay, ship, deliver).

- Draw the journey as stages in a row, in the order they happen.
- A stage with a mapped flow links to that flow's page. A stage with no mapped flow appears faded and labelled "not mapped".
- Show a coverage indicator at the top: how many stages are mapped, inferred and not mapped. This doubles as the progress panel for the next extraction waves.

The stage list is a business decision too. Ask the user for it; mark it as inferred if you derived it from flow names.

## Status view

For each main entity (for example Order), show its state diagram: states, transitions, and what triggers each transition. Clicking a transition shows the flow and step where it happens. Keep the transition table below the diagram, not instead of it.

## Explore (the full graph)

- Lives under `More`, not in the main menu.
- Never opens with every node. It opens focused on one chosen application and its direct neighbours, with a control to expand one level at a time.
- Tables and topics appear only when the user expands toward them.

## Less text on open

- Every screen opens with at most one sentence of description.
- Gaps, points of attention and inferred steps become a badge with a counter (for example "2 gaps") that expands on click. They are never a paragraph above the diagram.
- Long descriptions sit behind "show more".
- Nothing is removed. Whatever leaves the main screen stays reachable by click.

## Abbreviation legend

- Next to every table, column, service or topic code, show the meaning from `mapa/glossario.json`. With no meaning filled in, show only the code with a discreet "to be defined" marker.
- Add a Glossary page under `More`: a searchable table with code, type, where it appears and meaning, plus a "no meaning yet" filter so the team sees what is left to fill in.
- Never invent a meaning. The rule from `SKILL.md` applies to the viewer as well.

## Catalogs are tables, not walls of cards

Events, Data and APIs are lookup views. Build them as searchable, sortable tables with filters.

- **Events:** topic, producers, consumers, publishing mechanism, flows where it appears. Filters for "no producer identified" and "orphan" (no consumer).
- **Data:** a matrix of services by tables, with R for read and W for write. It shows at a glance who owns each table and which tables are shared between services.
- **APIs:** endpoint, service, callers, flows where it appears.

Give every table column a sensible minimum width and allow horizontal scrolling. A column so narrow that text wraps letter by letter is a bug.

## Two views worth adding after the basics

- **Impact:** clicking a table, column or event lists and highlights every service and flow that reads, writes, publishes or consumes it. It answers "if I change this, what is affected?".
- **Guided tour:** a route of 5 to 7 steps for someone new to the team, reusing existing screens (home, one application card, one journey, one animated flow, the glossary).

## Look at the result before saying it is done

Reading the HTML is not enough to know a screen works. After building the visualizer, and after each stage of a reorganization, look at it.

- Open the visualizer in a browser with whatever browser or screenshot tool the session has, and take a screenshot of every screen you changed.
- Take them at two sizes: a large desktop window and a laptop-sized one (about 1366 by 768). Broken layouts usually show only at the smaller size.
- For an animated flow, capture the first step, one step in the middle and the last step.
- In each screenshot, check that:
  - the diagram fills the available space and nothing is cut off or overlapping;
  - no label is truncated to the point of being unreadable, and no table column wraps text letter by letter;
  - the screen opens with at most one sentence of text;
  - the checklist items for that stage are met.
- Fix what you find and take the screenshot again. Do not report a stage as done with a known visual defect.
- In the stage summary, show the screenshots or say what you saw in them.
- If the session has no way to open a browser or take a screenshot, say so plainly and ask the user to check the screen. Never claim a screen looks right without having seen it.

Screenshots of a real system show real service, table and column names. Keep them inside the project; do not attach them anywhere outside it.

## When reorganizing an existing visualizer

- Do not redo the extraction and do not reread service code. Work only on the visualizer and the JSONs that already exist.
- If a change needs data the JSONs do not have, do not invent it: list it in `mapa/duvidas.md`. That list becomes the scope of the next extraction wave.
- Redirect the URLs of removed views to the views that replaced them.
- Work in stages, in the order of this file's sections. After each stage, check the result on screen (see "Look at the result before saying it is done"), then stop, say what changed in at most 5 lines and wait for the user to confirm. The first two (one page per flow, and the home) remove most of the confusion, so the user can judge after them whether the rest is worth the tokens.
- At the end, update `mapa/README.md` with the new structure.

## Checklist

- [ ] Landing page is a map plus a list of flows, not a gallery of cards
- [ ] Each flow has exactly one page, with the animation on top at full size
- [ ] The full graph never opens with every node
- [ ] Journeys index the flows and show coverage
- [ ] No screen opens with more than one sentence of text
- [ ] Gaps and inferred steps are badges, not paragraphs
- [ ] Animations start at the user action and follow events to their consumers
- [ ] Every code shows its glossary meaning or a "to be defined" marker
- [ ] Events, Data and APIs are searchable tables
- [ ] No table column wraps text letter by letter
- [ ] Every changed screen was checked in a screenshot at two window sizes
