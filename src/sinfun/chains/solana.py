"""Pull memecoin-related data from Solana.

We talk to the Helius RPC (or any compatible endpoint that exposes the
expanded transaction format) plus the Jupiter and Raydium APIs for prices.
"""
import os
from typing import Any

import requests


HELIUS_BASE = "https://api.helius.xyz/v0"


class HeliusClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("HELIUS_API_KEY", "")

    def _get(self, path: str, params: dict = None):
        params = dict(params or {})
        params["api-key"] = self.api_key
        r = requests.get(f"{HELIUS_BASE}{path}", params=params, timeout=20)
        r.raise_for_status()
        return r.json()

    def get_token_holders(self, mint: str, limit: int = 100):
        return self._get(f"/token-metadata", {"mint": mint, "limit": limit})

    def get_address_transactions(self, address: str, limit: int = 100, before: str = None):
        params = {"limit": limit}
        if before:
            params["before"] = before
        return self._get(f"/addresses/{address}/transactions", params)



    def top_holders(self, mint: str, limit: int = 25):
        """Returns list of {address, amount, percent_of_supply} sorted desc."""
        data = self._get(f"/token-holders", {"mint": mint, "limit": limit})
        total = sum(h.get("amount", 0) for h in data)
        if total == 0:
            return []
        return [
            {
                "address": h["address"],
                "amount": h["amount"],
                "percent_of_supply": h["amount"] / total * 100,
            }
            for h in data
        ]
