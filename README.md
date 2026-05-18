# token-risk-feature-store

Multi-source feature pipeline for token-level risk signals and offline ML
analysis.

This project ingests fragmented market and holder data, computes risk-oriented
features, and stores append-only parquet datasets partitioned by source and
day. The current domain is speculative token markets, but the core pattern is
general: turn noisy, fast-changing public data into a clean feature store that
can support research, labeling, and model training.

## What It Builds

- **Source adapters** for Solana, Base/EVM-style RPCs, and Hyperliquid-style
  market data.
- **Feature modules** for holder concentration, developer-wallet behavior,
  bundled-buy clusters, exit-liquidity events, and lifecycle metadata.
- **Append-only parquet storage** that keeps historical snapshots queryable.
- **CLI workflows** for inspecting one asset or backfilling many assets.
- **Notebook-ready datasets** for offline analysis and classifier experiments.

## Pipeline

```
source APIs / RPCs
      |
      v
chain-specific adapters
      |
      v
normalization + validation
      |
      v
risk feature modules
      |
      v
partitioned parquet store
      |
      v
research notebooks / ML classifiers
```

## Example

```python
from sinfun.signals.rug_features import featurize
from sinfun.chains.solana import HeliusClient

client = HeliusClient(api_key="...")
holders = client.top_holders("MINT_ADDRESS")

print(featurize({"mint": "MINT_ADDRESS", "holders": holders, "age_days": 3}))
# {
#   "top1_pct": 47.2,
#   "top10_pct": 81.4,
#   "gini": 0.94,
#   "n_holders": 1812,
#   ...
# }
```

CLI:

```bash
sinfun inspect <mint> --chain solana
sinfun backfill --mints-file mints.txt --chain solana --out data/
```

## Getting Started

```bash
pip install -e ".[solana]"

export HELIUS_API_KEY=...
export BASE_RPC_URL=...

sinfun backfill --mints-file mints.txt --chain solana --out data/
```

## Repository Layout

```
src/sinfun/
  chains/       source adapters and chain-specific clients
  signals/      feature modules
  storage.py    parquet persistence
  lifecycle.py  asset lifecycle helpers
  ml.py         modeling utilities
  report.py     summaries for analysis
  cli.py        command-line workflows

docs/           design notes, features, findings
notebooks/      exploratory analysis
tests/          storage, feature, lifecycle, and ML tests
```

## Why This Framing Matters

Speculative markets are useful stress tests for data engineering: assets appear
and disappear quickly, labels are sparse, APIs are inconsistent, and the most
interesting signals are often behavioral rather than neatly tabular. This repo
focuses on the pipeline required before modeling is possible:

- normalize heterogeneous sources
- compute repeatable features
- preserve historical snapshots
- support offline labeling and analysis
- keep domain assumptions isolated in small modules

## License

MIT.
