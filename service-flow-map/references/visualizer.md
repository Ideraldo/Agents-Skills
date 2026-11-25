# Phase 5: the visualizer

Build only after the pilot is validated.

This file lists what the visualizer must contain. Read `viewer-guidelines.md` before building: it says how to organize the views so the result stays readable as the map grows.

Build `mapa/visualizador/index.html`: a single page, no build step, that reads the JSONs in `mapa/`. No external CDN dependencies (plain JavaScript, CSS and SVG, or libraries already approved by the organization). The visualizer is generic: swapping the JSONs swaps the content.

## Three zoom levels

1. **Overview map:** every repository in the inventory as linked nodes, grouped by type (front end, APIs, workers, queues, databases). Nodes with status `raso` appear faded, so coverage is visible.
2. **Service card:** clicking a node opens a panel with the description, who uses it, what it depends on, entry points, queues and tables, with the columns read and written.
3. **Animated flow:** pick a flow, click the trigger (for example the button on the screen) and the animation shows the data moving through the nodes step by step. When it reaches a table, the table is highlighted showing the columns written in that step. Controls: play, pause, previous step, next step and speed. A side list shows the steps and highlights the current one.

## Cross-cutting features

- **Abbreviation legend:** every abbreviation shows its glossary meaning on hover. With no meaning filled in, it shows "to be defined".
- **Confirmed vs inferred:** solid line for `confirmado`, dashed line for `inferido`, with a filter to show only one of them.
- **Evidence:** every step shows its source file and line.
- **Search** by service, table, column or queue name, highlighting where it appears on the map.
- **Reverse view:** clicking a table shows every service that reads or writes it.
