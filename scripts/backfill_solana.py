"""Backfill the dataset with recent Solana memecoin data."""
import argparse
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sinfun.chains.solana import HeliusClient
from sinfun.signals.rug_features import featurize
from sinfun.storage import append as storage_append


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mints-file", required=True, help="newline-delimited mint addresses")
    ap.add_argument("--out", default="data/")
    args = ap.parse_args()

    client = HeliusClient()
    mints = [m.strip() for m in Path(args.mints_file).read_text().splitlines() if m.strip()]
    records = []
    for i, mint in enumerate(mints):
        try:
            holders = client.top_holders(mint)
        except Exception as e:
            print(f"  {mint}: holders fetch failed ({e})")
            continue
        rec = {
            "mint": mint,
            "holders": holders,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }
        rec.update(featurize(rec))
        records.append(rec)
        if (i + 1) % 50 == 0:
            print(f"  fetched {i + 1}")
            storage_append(args.out, "solana", records)
            records = []
            time.sleep(1)
    storage_append(args.out, "solana", records)


if __name__ == "__main__":
    main()
