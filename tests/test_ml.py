import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from sinfun.signals.rug_features import FEATURE_NAMES, featurize


def test_featurize_returns_all_names():
    rec = {
        "holders": [{"address": f"a{i}", "amount": 100, "percent_of_supply": 5.0}
                    for i in range(20)],
        "age_days": 3.0,
        "liquidity_usd": 50_000,
    }
    feats = featurize(rec)
    assert set(feats.keys()) == set(FEATURE_NAMES)


def test_featurize_handles_empty_holders():
    feats = featurize({"holders": []})
    assert feats["top1_pct"] == 0.0
    assert feats["gini"] == 0.0
