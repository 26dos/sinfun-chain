"""Aggregate a feature vector used to estimate rug probability.

Not a model — just the inputs to one. The actual classifier is fit
externally; this module is the contract between data extraction and ml.
"""
from .concentration import concentration_features
from .dev_wallet import dev_dump_score


FEATURE_NAMES = [
    "top1_pct",
    "top10_pct",
    "gini",
    "n_holders",
    "dev_dump_score",
    "is_mint_renounced",
    "n_bundled_buy_clusters",
    "exit_liquidity_events",
    "age_days",
    "liquidity_usd",
]


def featurize(token_record: dict) -> dict:
    holders = token_record.get("holders", [])
    conc = concentration_features(holders)
    dev = dev_dump_score(token_record.get("dev_balance_history", []),
                         token_record.get("launch_ts", 0))
    return {
        "top1_pct": conc["top1_pct"],
        "top10_pct": conc["top10_pct"],
        "gini": conc["gini"],
        "n_holders": conc["n_holders"],
        "dev_dump_score": dev["score"],
        "is_mint_renounced": int(bool(token_record.get("is_mint_renounced", False))),
        "n_bundled_buy_clusters": len(token_record.get("bundled_buy_clusters", [])),
        "exit_liquidity_events": len(token_record.get("exit_liquidity_events", [])),
        "age_days": float(token_record.get("age_days", 0)),
        "liquidity_usd": float(token_record.get("liquidity_usd", 0)),
    }
