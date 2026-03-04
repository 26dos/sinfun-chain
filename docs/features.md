# Feature dictionary

| Feature                      | Range  | Notes |
|------------------------------|--------|-------|
| `top1_pct`                   | 0-100  | largest holder's % of supply |
| `top10_pct`                  | 0-100  | sum of top-10 holders' % |
| `gini`                       | 0-1    | gini coefficient over holder distribution |
| `n_holders`                  | int    | unique holders with non-zero balance |
| `dev_dump_score`             | 0-1    | how much of dev's initial balance has been sold |
| `is_mint_renounced`          | 0/1    | true if mint authority is `null` |
| `n_bundled_buy_clusters`     | int    | number of suspected bundled-buy clusters at launch |
| `exit_liquidity_events`      | int    | number of liquidity-removal events meeting heuristic |
| `age_days`                   | float  | days since launch (or token creation if no launch) |
| `liquidity_usd`              | float  | current pool depth (sum across DEXes) |

## When the value is missing

If we couldn't fetch the holder list, `top1_pct` / `top10_pct` / `gini` are
all 0. The classifier should treat 0s as missing if you're using these
features for a real prediction (the default sklearn classifier doesn't —
keep that in mind).



## gini implementation note

The Gini implementation in `concentration.py` operates on a count vector
(holder amounts). For very small holder lists (n < 10), the Gini estimate is
noisy; consider using a different summary statistic in that regime.
