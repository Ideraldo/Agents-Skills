---
name: sql-queries
description: Refines the request first, then writes or explains T-SQL queries (SELECT and UPDATE) for a SQL Server database, including columns that store JSON. Use whenever a request involves fetching, changing or understanding data in the project's database.
---

# Project SQL queries

Always work in two stages: first WHAT to fetch, then HOW. Do not write SQL before stage 1 is approved.

This skill assumes SQL Server (T-SQL). For Postgres or MySQL the JSON functions and the schema script change; see `references/setup.md`.

## Stage 1: what to fetch

1. Read `schema/INDEX.md` and find the candidate tables.
2. Open in `schema/` only the files for those tables and, if any column stores JSON, read `json-examples.md`.
3. If the table is not there, look for its ORM entity and migrations in the repository (for example EF Core entities and migrations).
4. Reply with your understanding of the request, without SQL:
   - Goal in one sentence, in business language.
   - Tables and columns you plan to use, and why.
   - Granularity: what each result row represents.
   - Filters: period, status, what's in and what's out.
   - How the tables join (which keys).
   - JSON fields involved and the path to each one.
   - One example row of the expected result. For an UPDATE, a before and after example.
   - Doubts and ambiguities, as numbered questions.
5. Stop and wait for approval or answers.

If a column, type or JSON format is missing, ask. Never invent a column name or a JSON field.

Skip stage 1 only if the request says "direct" or already brings the tables, columns and filters.

## Stage 2: how to fetch

Do not try to connect to the database or run the query unless you were explicitly given read access. Deliver the script for a human to run.

### General rules

- Dialect: T-SQL (SQL Server).
- Prefer the simplest form that works. JOIN before subquery. CTE only when it makes reading clearer.
- No cursors, temp tables, procedures or dynamic SQL unless the request requires them.
- No `SELECT *`. List the columns.
- Qualify columns with the table alias.
- If the query crosses databases, use the full name `Database.schema.Table`.

### JSON columns

- Scalar value: `JSON_VALUE`.
- Object or array: `JSON_QUERY`.
- Expand an array into rows: `CROSS APPLY OPENJSON ... WITH`.
- Guard with `ISJSON(column) = 1` when a row might hold invalid content.
- Handle optional fields: `JSON_VALUE` returns NULL when the path doesn't exist.
- Warn when a filter on JSON will scan the whole table.

### SELECT

- Build large queries in stages: base table, then JOINs, then JSON extraction, then filters.
- Use `TOP` in exploratory queries.

### UPDATE and DELETE

- A single statement with JOIN whenever possible.
- Every UPDATE and DELETE needs a WHERE.
- Wrap in `BEGIN TRAN` and leave `COMMIT` and `ROLLBACK` commented out for the human to choose.
- Include a check SELECT before and another after, with the same WHERE.
- Show `@@ROWCOUNT` and say how many rows are expected.
- Also deliver a script to roll the data back.
- To change a field inside JSON, use `JSON_MODIFY`.

### Response format

1. The query, with a comment on each line or block saying what it does and why.
2. A 3 to 5 sentence summary of the data path: which table it starts from, what it passes through and what it returns or changes.
3. Risks: what might be slow and what might touch more rows than expected.
4. Assumptions: everything you assumed that was not in the schema.

## When asked to explain an existing query

Explain it line by line, say what each JOIN brings and what each JSON extraction returns, and show an example input row and output row. Do not rewrite the query unless asked.
