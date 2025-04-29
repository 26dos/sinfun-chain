"""Detect dev wallet activity that's incompatible with a "trustworthy" token.

Heuristics:
  - dev wallet sells a large % of its holdings shortly after launch
  - dev wallet adds liquidity then removes shortly after
  - dev wallet receives buybacks from other LP fees
"""


def dev_dump_score(
    dev_balance_history: list[dict],
    launch_ts: int,
) -> dict:
    """Return a score [0, 1] indicating how aggressive the dev's selling has been.

    `dev_balance_history` items: {timestamp, balance}
    """
    if not dev_balance_history:
        return {"score": 0.0, "max_dump_pct": 0.0}
    sorted_h = sorted(dev_balance_history, key=lambda h: h["timestamp"])
    initial = sorted_h[0]["balance"] or 1
    minimum = min(h["balance"] for h in sorted_h)
    max_dump_pct = (1 - minimum / initial) * 100
    score = min(max_dump_pct / 100, 1.0)
    return {"score": score, "max_dump_pct": max_dump_pct}
