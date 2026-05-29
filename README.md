# businesslog-agent

PLATO domain agent for [businesslog.ai](https://businesslog.ai) — writes business metrics to PLATO, queries trends, and learns from patterns over time.

## What This Gives You

- **Metric tile writes** — record business events as PLATO tiles
- **Trend queries** — retrieve aggregated business data from PLATO
- **Fleet integration** — shares PLATO infrastructure with other domain agents

## Installation

```bash
pip install businesslog-agent
```

## Quick Start

```python
from businesslog_agent import write_tile, query_metrics

# Record a business event
write_tile({
    "type": "sale",
    "amount": 50000,
    "customer": "Enterprise Corp",
    "tier": "enterprise",
})

# Query recent metrics
metrics = query_metrics(room="businesslog", limit=50)
```

## Testing

```bash
pip install -e .
pytest
```

## How It Fits

Domain agent in the Cocapn Fleet. Part of the business logging pipeline alongside `businesslog-ai` (analysis engine) and `businesslog-app` (structured logging).

## License

MIT
