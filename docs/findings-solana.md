# Findings — Solana memecoins (Aug-Oct 2025 sample)

This is a rolling note. Numbers are from a backfill of ~14k Solana
memecoins fetched between 2025-08 and 2025-10.

## Holder concentration

  - Median top-1 holder share: 24.8%
  - Median top-10: 71.2%
  - 38% of tokens have a single holder owning > 50% of supply

For comparison, the 2024 baseline (from a smaller sample): top-1 median
17.4%, top-10 median 65.0%. Concentration appears to be drifting up.

## Mint authority

  - 71% of tokens have mint authority renounced at fetch time
  - Renouncement timing is bimodal: most tokens either renounce in the
    first hour or never. Tokens renouncing later than 24h post-launch are
    rare (~3% of sample).

## Bundled buys

  - Of tokens with > 100 holders, 19% have at least one bundled-buy cluster
    detected at launch.
  - The sniper bundles tend to be small (median 4 wallets) but a long
    tail goes up to 60+ wallets sharing a single funder.

## Caveat

These are heuristic rates, not ground-truth labels. The "bundled-buy
detector" is a rule, not a classifier — it has false positives (e.g. a
single funding wallet that legitimately disburses to many trader wallets).
