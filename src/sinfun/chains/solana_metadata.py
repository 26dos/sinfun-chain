"""Fetch SPL token metadata (name, symbol, supply, mint authority).

We mostly care about: was the mint authority renounced? Whoever can mint
new supply controls the rug button.
"""
from solana.rpc.api import Client
from solders.pubkey import Pubkey


def get_mint_info(rpc_url: str, mint: str) -> dict:
    client = Client(rpc_url)
    pk = Pubkey.from_string(mint)
    resp = client.get_account_info_json_parsed(pk)
    val = resp.value
    if val is None:
        return {}
    info = val.data.parsed.get("info", {})
    return {
        "mint": mint,
        "supply": int(info.get("supply", 0)),
        "decimals": info.get("decimals"),
        "mint_authority": info.get("mintAuthority"),
        "freeze_authority": info.get("freezeAuthority"),
        "is_renounced": info.get("mintAuthority") is None,
    }
