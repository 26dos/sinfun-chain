from sinfun.lifecycle import classify_phase, Phase, LifecycleTracker


def test_pre_launch_when_no_liquidity():
    assert classify_phase({}) == Phase.PRE_LAUNCH


def test_bonding_overrides_age():
    s = {"liquidity_usd": 1000, "on_bonding_curve": True}
    assert classify_phase(s) == Phase.BONDING


def test_dead_when_no_volume_for_a_week():
    s = {"liquidity_usd": 100, "age_days": 30, "volume_24h_usd": 0}
    assert classify_phase(s) == Phase.DEAD


def test_tracker_collapses_repeats():
    t = LifecycleTracker()
    t.update(1, {"liquidity_usd": 100, "on_bonding_curve": True})
    t.update(2, {"liquidity_usd": 100, "on_bonding_curve": True})
    t.update(3, {"liquidity_usd": 100, "age_days": 0.5})
    assert len(t.transitions) == 2
    assert t.transitions[1][1] == Phase.GRADUATED
