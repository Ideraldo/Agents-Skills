---
name: api-change-impact
description: "Use before changing an API endpoint, message/event schema, DTO or shared contract in a microservice system, or when reviewing a PR that does. Finds every consumer across repos, the payloads they actually send or expect, and classifies the change as safe, risky or breaking, with a rollout suggestion."
---

# API change impact

Most changes in a microservice system touch an API surface (Postman reported about 75% of PRs do). The risk is rarely in the service you are editing; it is in consumers you did not know about. This skill finds them before the change ships.

## Inputs

- The contract that will change: endpoint, DTO, event/topic schema, gRPC proto, shared library type.
- The proposed change (diff or description).
- Where consumers may live: list of repos or a workspace folder with them cloned.

## Steps

1. **Describe the change precisely**: fields added, removed, renamed, type or nullability changed, validation tightened, default changed, status codes, ordering.
2. **Find consumers** with search, not memory:
   - route strings and client calls (HttpClient, typed clients, Refit, Angular services, fetch/axios)
   - topic or queue names and consumer classes (Kafka, RabbitMQ, SQS)
   - shared DTO packages and their versions per repo
   - config files and gateways that reference the route
   If `service-flow-map` JSON exists, start from it.
3. **For each consumer, record** what it reads and sends: fields used, assumptions (non-null, ordering, enum values), and the code location.
4. **Get real payloads** if possible: test fixtures, contract tests, logged samples from non-production. Never pull production data with personal or financial details.
5. **Classify**:
   - safe: additive and optional, no consumer depends on what changes
   - risky: behavior change that consumers might notice (validation, defaults, precision, timing)
   - breaking: removal, rename, type change, required field added
6. **Propose the rollout**: versioning, expand-and-contract (add new, migrate consumers, remove old), feature flag, consumer PRs needed, contract tests to add.

## Rules

- A consumer you could not check is listed as "unknown", not assumed safe.
- Every consumer line points to repo and file:line.

## Output

| Consumer (repo) | Uses | Location | Impact | Action needed |

Then: classification, rollout plan, and tests to add.
