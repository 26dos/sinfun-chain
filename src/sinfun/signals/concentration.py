"""Top-N holder concentration as a rug-risk signal.

A token where the top 10 holders own > X% of supply is, in expectation,
fragile against a coordinated dump. We track:

  - top1_pct: the single largest holder's share
  - top10_pct: top 10
  - gini: gini coefficient over the holder distribution
"""
from typing import Iterable


def gini_coefficient(amounts: Iterable[float]) -> float:
    sorted_amounts = sorted(a for a in amounts if a > 0)
    if not sorted_amounts:
        return 0.0
    n = len(sorted_amounts)
    cumulative = 0.0
    weighted = 0.0
    for i, a in enumerate(sorted_amounts, 1):
        cumulative += a
        weighted += i * a
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
