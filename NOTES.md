# notes

the speculative side of defi — memecoins, prediction markets, leveraged perps,
"casino-flavored" protocols — is what most people actually trade on, and what
generates most of the chaos. it's also the side where data is hardest to
study because:

  - most of it lives on chains other than ethereum (solana, base, hyperliquid)
  - tokens turn over fast (a memecoin's lifecycle is days, not months)
  - wallet behavior is highly bimodal (whales vs. dust)
  - rugs and exit-liq events are common but rarely labeled

what i want from this:
  - one tool that pulls memecoin lifecycle data across chains
  - features per token: peak mc, time-to-peak, top-holder concentration,
    bundled buys, dev wallet behavior
  - signals for "this looks like an exit liq pattern starting"
  - eventually a small classifier for rug probability

what i'm not trying to do:
  - this isn't a trading bot. zero financial advice.
  - it's a *research* toolkit. accuracy > speed. labels > predictions.



## naming

"sinfun" because the protocols this thing tracks are speculative as hell —
memecoins, casino DeFi, prediction markets on whether the casino will rug.
the academic/serious framing is "high-volatility on-chain instruments" but
nobody calls it that.



## end of 2025

state of the world:
  - 14k Solana mints in the dataset, ~2k Base, ~500 Hyperliquid coins
  - heuristics are stable; classifier on top is somewhere around 0.84 ROC-AUC
    on a hand-labeled rug subset (n=200)

next year:
  - cross-chain wallet linkage — probably the biggest unsolved piece
  - automated pull of pump.fun graduates daily
  - notebook tour of "interesting deaths" — case studies of tokens that
    rugged spectacularly

## solana

helius free tier is enough for ~100 tokens/day. for more, paid is fine.

## bundled buys

false positive rate is high. need a manual review of detected clusters.
