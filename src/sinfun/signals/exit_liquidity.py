"""Detect liquidity-removal events that look like exit-liq attacks.

An exit-liquidity event:
  - Single tx removes a large fraction of pool liquidity
  - The remover had been the LP (or close associate)
  - Price impact on the small remaining liquidity is severe afterwards
"""


def is_likely_exit(
    pre_liquidity_usd: float,
    post_liquidity_usd: float,
    remover_lp_share: float,
    threshold_pct: float = 50.0,
) -> dict:
    """Heuristic: was this withdrawal probably an exit?"""
    if pre_liquidity_usd <= 0:
        return {"is_exit": False, "reason": "no liquidity to begin with"}
    removed_pct = (1 - post_liquidity_usd / pre_liquidity_usd) * 100
    if removed_pct < threshold_pct:
        return {"is_exit": False, "removed_pct": removed_pct}
    if remover_lp_share < 0.5:
        # if the remover wasn't a major LP, this isn't exit-style
        return {"is_exit": False, "removed_pct": removed_pct,
                "reason": "remover was not a major LP"}
    return {
        "is_exit": True,
        "removed_pct": removed_pct,
        "remover_lp_share": remover_lp_share,
    }
