"""Hyperliquid perp data."""
import requests


HL_API = "https://api.hyperliquid.xyz/info"


def _f(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def get_open_interest(coin: str) -> dict:
    r = requests.post(HL_API, json={"type": "metaAndAssetCtxs"}, timeout=15)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, list) or len(data) < 2:
        return {}
    universe = (data[0] or {}).get("universe") or []
    asset_ctxs = data[1] or []
    for i, u in enumerate(universe):
        if u.get("name") != coin:
            continue
        if i >= len(asset_ctxs):
            return {}
        ctx = asset_ctxs[i] or {}
        return {
            "coin": coin,
            "open_interest": _f(ctx.get("openInterest")),
            "funding": _f(ctx.get("funding")),
            "mark_price": _f(ctx.get("markPx")),
            "premium": _f(ctx.get("premium")),
        }
    return {}


def get_recent_funding(coin: str, n: int = 24) -> list[dict]:
    r = requests.post(HL_API, json={"type": "fundingHistory", "coin": coin}, timeout=15)
    r.raise_for_status()
    data = r.json()
    return data[-n:] if isinstance(data, list) else []
