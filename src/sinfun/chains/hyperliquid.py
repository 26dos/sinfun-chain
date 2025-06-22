"""Hyperliquid perp data — useful for tracking forced-liquidation cascades.

Hyperliquid exposes the orderbook + recent trades over a public REST API.
We don't need archive data here; we sample at intervals.
"""
import requests


HL_API = "https://api.hyperliquid.xyz/info"


def get_open_interest(coin: str) -> dict:
    r = requests.post(HL_API, json={"type": "metaAndAssetCtxs"}, timeout=15)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, list) or len(data) < 2:
        return {}
    universe = data[0].get("universe", [])
    asset_ctxs = data[1]
    for i, u in enumerate(universe):
        if u.get("name") == coin and i < len(asset_ctxs):
            ctx = asset_ctxs[i]
            return {
                "coin": coin,
                "open_interest": float(ctx.get("openInterest", 0)),
                "funding": float(ctx.get("funding", 0)),
                "mark_price": float(ctx.get("markPx", 0)),
                "premium": float(ctx.get("premium", 0)),
            }
    return {}
