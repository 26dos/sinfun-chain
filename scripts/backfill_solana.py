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


# Known mints that consistently produce errors on Helius (deactivated tokens, etc.)
SKIP = set()


def load_skip_file(p: str):
    if not p or not Path(p).exists():
        return
    SKIP.update(line.strip() for line in Path(p).read_text().splitlines() if line.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mints-file", required=True)
    ap.add_argument("--out", default="data/")
    ap.add_argument("--skip-file", default="data/known_bad_mints.txt")
    args = ap.parse_args()

    load_skip_file(args.skip_file)
    client = HeliusClient()
    mints = [m.strip() for m in Path(args.mints_file).read_text().splitlines()
             if m.strip() and m.strip() not in SKIP]
    records = []
    for i, mint in enumerate(mints):
        try:
            holders = client.top_holders(mint)
        except Exception as e:
            print(f"  {mint}: holders fetch failed ({e})")
            SKIP.add(mint)
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
    Path(args.skip_file).parent.mkdir(parents=True, exist_ok=True)
    Path(args.skip_file).write_text("\n".join(sorted(SKIP)))


if __name__ == "__main__":
    main()
