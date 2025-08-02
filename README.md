# sinfun-chain

## The Problem

Most DeFi research focuses on the well-behaved end of the spectrum — money
markets, blue-chip DEXes, lending protocols with formal verification audits.
Meanwhile, the *vast majority* of trading volume on chains like Solana and
Base is happening in memecoins, leveraged perps, and prediction markets —
the speculative end of DeFi.

This is the side where rugs happen, where wash trading is endemic, where
exit-liquidity events wipe out retail in seconds. It's also the side where
data is hardest to study, because tokens turn over in days, infrastructure
is fragmented across chains, and very little gets labeled.

This repo is a research toolkit for studying that side.

## Our Approach

`sinfun-chain` pulls token-level data from multiple chains, computes
rug-risk features (top-N holder concentration, dev-wallet behavior,
bundled-buy clusters, mint authority status), and stores everything as
append-only parquet partitioned by chain and day.

The point isn't to predict the next rug in real time — that's a different
problem with much faster latency requirements. The point is to build a
clean, queryable dataset that researchers can use for offline analysis:
which signals were predictive of rugs in the past? How does dev-wallet
behavior on Solana compare to Base? How do exit-liquidity events cluster
in time?

## Show Me

```python
from sinfun.signals.rug_features import featurize
from sinfun.chains.solana import HeliusClient

client = HeliusClient(api_key="...")
holders = client.top_holders("WHATEVER_MINT_YOU_CARE_ABOUT")
print(featurize({"mint": "...", "holders": holders, "age_days": 3}))
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

# pull a small starter set of mints (e.g. recent pump.fun graduates) into mints.txt
sinfun backfill --mints-file mints.txt --chain solana --out data/
```

## How It Works

```
┌─────────────────┐     ┌────────────────┐     ┌───────────────┐
│  chain backends │────▶│ rug features   │────▶│  parquet store │
│  (sol, base, hl)│     │  (per-token)   │     │ (chain=, day=) │
└─────────────────┘     └────────────────┘     └───────────────┘
                                                        │
                                                        ▼
                                                 ┌──────────────┐
                                                 │ research /    │
                                                 │ classifier   │
                                                 └──────────────┘
```

## License

MIT.
