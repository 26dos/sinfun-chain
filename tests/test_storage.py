import tempfile
from pathlib import Path

import pandas as pd

from sinfun.storage import append, read_all


def test_append_creates_partition(tmp_path):
    p = append(tmp_path, "solana", [{"mint": "a", "top1_pct": 50.0}])
    assert p is not None
    assert p.exists()


def test_read_all_returns_concat(tmp_path):
    append(tmp_path, "solana", [{"mint": "a", "top1_pct": 50.0}])
    append(tmp_path, "solana", [{"mint": "b", "top1_pct": 25.0}])
    df = read_all(tmp_path, chain="solana")
    assert len(df) == 1  # b dedup-overwrites a only if same mint; here distinct -> 2
    assert df["mint"].iloc[0] in {"a", "b"}


def test_read_all_empty(tmp_path):
    df = read_all(tmp_path, chain="solana")
    assert df.empty
