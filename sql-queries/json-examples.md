# JSON examples

One entry per column that stores JSON. Real structure, **fake values only**.

## DatabaseA.dbo.Orders.Metadata

```json
{
  "channel": "web",
  "coupon": { "code": "FAKE10", "percent": 10 },
  "tags": ["first-purchase", "promo"]
}
```

- Optional: `coupon`
- Arrays: `tags`
- Format history: `channel` exists only in rows created after the v2 release; older rows don't have it.
