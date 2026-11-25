# Schema index

One line per table the team uses most (10 to 20 is plenty). The DDL of each table lives in `schema/<Database>/`.

| Database | Table | What it's for | JSON columns |
|---|---|---|---|
| DatabaseA | dbo.Orders | One row per customer order, created at checkout | `Metadata` |
| DatabaseA | dbo.OrderItems | Items of each order, joined by `OrderId` | none |
