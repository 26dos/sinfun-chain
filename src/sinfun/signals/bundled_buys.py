"""Detect bundled buys at launch — a known sniper / dev pattern.

The pattern:
  - Token launches at block T with liquidity provision
  - In block T or T+1, multiple buys occur from addresses that share a
    funding source (one wallet drained ETH/SOL into all of them right
    before launch)

We don't pretend to do full clustering here — just a quick heuristic to flag
suspicious clusters for downstream review.
"""


def detect_bundled_buys(
    launch_block: int,
    buys: list[dict],
    funding_lookback_blocks: int = 50,
) -> list[dict]:
    """Identify buyers that were funded shortly before launch.

    `buys` items: {block, buyer, amount_in, funding_history}
        funding_history items: {from, block}

    Returns: a list of detected clusters (wallets sharing a funder).
    """
    early_buyers = [b for b in buys if launch_block <= b["block"] <= launch_block + 1]
    by_funder: dict[str, list[dict]] = {}
    for b in early_buyers:
        recent_funders = {
            h["from"] for h in (b.get("funding_history") or [])
            if launch_block - funding_lookback_blocks <= h.get("block", -1) < launch_block
        }
        for f in recent_funders:
            by_funder.setdefault(f, []).append(b)
    clusters = [
        {"funder": f, "buyers": [b["buyer"] for b in bs], "size": len(bs)}
        for f, bs in by_funder.items()
        if len(bs) >= 2
    ]
    return clusters
