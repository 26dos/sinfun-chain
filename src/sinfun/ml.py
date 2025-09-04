"""Train a rug-or-not classifier from labeled token records."""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report

from .signals.rug_features import FEATURE_NAMES


def fit(dataset_path: str, model_out: str = "models/rug.joblib") -> None:
    df = pd.read_parquet(dataset_path)
    X = df[FEATURE_NAMES].to_numpy(dtype=np.float64)
    y = df["is_rug"].to_numpy(dtype=int)
    clf = GradientBoostingClassifier(n_estimators=300, max_depth=4)
    clf.fit(X, y)
    Path(model_out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, model_out)
    Path(model_out).with_suffix(".json").write_text(json.dumps({
        "feature_names": FEATURE_NAMES, "n_samples": len(X),
        "rug_rate": float(y.mean()),
    }))
    print(classification_report(y, clf.predict(X)))


def predict_rug_prob(model_path: str, record: dict) -> float:
    clf = joblib.load(model_path)
    from .signals.rug_features import featurize
    feats = featurize(record)
    x = np.array([[feats[k] for k in FEATURE_NAMES]], dtype=np.float64)
    return float(clf.predict_proba(x)[0, 1])
