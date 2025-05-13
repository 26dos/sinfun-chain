"""Append-only parquet store for token records, partitioned by chain & day."""
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def append(root: str | Path, chain: str, records: list[dict]) -> Path:
    if not records:
        return None
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = Path(root) / f"chain={chain}" / f"day={day}" / "records.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(records)
    if out.exists():
        existing = pd.read_parquet(out)
        df = pd.concat([existing, df], ignore_index=True)
        # dedupe by token mint, last write wins
        if "mint" in df.columns:
            df = df.drop_duplicates(subset=["mint"], keep="last")
    df.to_parquet(out, index=False)
    return out



def read_all(root: str | Path, chain: str = None) -> pd.DataFrame:
    pattern = f"chain={chain}/**/records.parquet" if chain else "chain=*/**/records.parquet"
    paths = sorted(Path(root).glob(pattern))
    if not paths:
        return pd.DataFrame()
    return pd.concat([pd.read_parquet(p) for p in paths], ignore_index=True)
