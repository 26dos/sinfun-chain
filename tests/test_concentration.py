import pytest

from sinfun.signals.concentration import gini_coefficient, concentration_features


def test_gini_uniform_is_low():
    g = gini_coefficient([100, 100, 100, 100])
    # Uniform: by the (2*sum_i i*a) / (n*sum_a) - (n+1)/n formula on
    # sorted equal values, gini = 1/n. For n=4, gini = 0.25.
    assert abs(g - 0.25) < 1e-9


def test_gini_single_holder_is_max():
    g = gini_coefficient([0, 0, 0, 100])
    assert g == pytest.approx(0.75)


def test_concentration_handles_empty():
    f = concentration_features([])
    assert f["n_holders"] == 0


def test_top1_pct():
    holders = [
        {"address": "a", "amount": 10, "percent_of_supply": 50.0},
        {"address": "b", "amount": 6,  "percent_of_supply": 30.0},
        {"address": "c", "amount": 4,  "percent_of_supply": 20.0},
    ]
    f = concentration_features(holders)
    assert f["top1_pct"] == 50.0
    assert f["top10_pct"] == 100.0
