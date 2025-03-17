"""Top-N holder concentration as a rug-risk signal."""
from typing import Iterable


def gini_coefficient(amounts: Iterable[float]) -> float:
    sorted_amounts = sorted(a for a in amounts if a > 0)
    if not sorted_amounts:
        return 0.0
    n = len(sorted_amounts)
    cumulative = sum(sorted_amounts)
    if cumulative == 0:
        return 0.0
    weighted = sum(i * a for i, a in enumerate(sorted_amounts, 1))
    return (2 * weighted) / (n * cumulative) - (n + 1) / n


def concentration_features(holders: list[dict]) -> dict:
    if not holders:
        return {"top1_pct": 0.0, "top10_pct": 0.0, "gini": 0.0, "n_holders": 0}
    sorted_h = sorted(holders, key=lambda h: -h["percent_of_supply"])
    top1 = sorted_h[0]["percent_of_supply"]
    top10 = sum(h["percent_of_supply"] for h in sorted_h[:10])
    g = gini_coefficient(h["amount"] for h in holders)
    return {
        "top1_pct": top1,
        "top10_pct": top10,
        "gini": g,
        "n_holders": len(holders),
    }
