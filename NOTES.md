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
