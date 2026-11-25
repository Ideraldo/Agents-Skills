# Output formats

Field names and enum values are kept in Portuguese on purpose: the visualizer reads them as is. If you rename them, rename them in the visualizer too.

## mapa/servicos/<servico>.json

```json
{
  "servico": "",
  "tipo": "api|worker|front|lib",
  "descricao": "what the service does, in 2 to 4 sentences, without interpreting abbreviations",
  "consumidores": ["who calls or consumes this service"],
  "depende_de": ["services, queues and databases it uses"],
  "status_mapeamento": "raso|aprofundado|validado",
  "entradas": [ { "tipo": "http|fila|job", "nome": "", "evidencia": "" } ],
  "passos": [
    {
      "fluxo": "",
      "ordem": 1,
      "acao": "leitura|escrita|chamada_http|publica_evento|consome_evento",
      "alvo": "raw name of the table, queue or service",
      "campos": ["columns or payload fields"],
      "descricao_tecnica": "",
      "status": "confirmado|inferido",
      "evidencia": "file:line"
    }
  ],
  "saidas": [ { "tipo": "", "destino": "", "evidencia": "" } ]
}
```

`status_mapeamento`: `raso` = inventory only, `aprofundado` = read by a sub-agent, `validado` = checked by a human.

## mapa/fluxos/<fluxo>.json

```json
{
  "fluxo": "",
  "gatilho": "user action that starts it",
  "passos": [
    { "ordem": 1, "de": "", "para": "", "acao": "", "dados": [],
      "campos_escritos": [], "status": "", "evidencia": "" }
  ]
}
```

## mapa/glossario.json

Every abbreviation found. `significado` stays `null` until a person fills it in.

```json
[ { "sigla": "", "tipo": "tabela|coluna|servico|fila",
    "onde_aparece": [], "significado": null } ]
```

## mapa/duvidas.md

Everything that was inferred, has no known output, or that only someone on the team can answer: triggers, stored procedures, scheduled jobs and any logic that is not in the services' code.
