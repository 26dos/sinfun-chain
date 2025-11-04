"""Aggregate a feature vector used to estimate rug probability."""
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


def _safe_get(d, k, default):
    v = d.get(k)
    return default if v is None else v


def featurize(token_record: dict) -> dict:
    holders = _safe_get(token_record, "holders", [])
    conc = concentration_features(holders)
    dev = dev_dump_score(_safe_get(token_record, "dev_balance_history", []),
                         _safe_get(token_record, "launch_ts", 0))
    return {
        "top1_pct": conc["top1_pct"],
        "top10_pct": conc["top10_pct"],
        "gini": conc["gini"],
        "n_holders": conc["n_holders"],
        "dev_dump_score": dev["score"],
        "is_mint_renounced": int(bool(_safe_get(token_record, "is_mint_renounced", False))),
        "n_bundled_buy_clusters": len(_safe_get(token_record, "bundled_buy_clusters", [])),
        "exit_liquidity_events": len(_safe_get(token_record, "exit_liquidity_events", [])),
        "age_days": float(_safe_get(token_record, "age_days", 0)),
        "liquidity_usd": float(_safe_get(token_record, "liquidity_usd", 0)),
    }
