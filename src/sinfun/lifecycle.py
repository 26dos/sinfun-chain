"""Track a token's lifecycle through coarse-grained phases.

Phases (in order):
  1. PRE_LAUNCH   — mint exists, no liquidity yet
  2. BONDING       — bonding curve / launchpad still active
  3. GRADUATED     — moved to AMM (e.g. Raydium for pump.fun graduates)
  4. ESTABLISHED   — > 24h post-graduation, > $X market cap
  5. DECLINING     — dropping volume, price below threshold
  6. DEAD          — no trading for > N days

We don't model cross-chain migration or wrapped tokens.
"""
from enum import Enum


class Phase(str, Enum):
    PRE_LAUNCH = "pre_launch"
    BONDING = "bonding"
    GRADUATED = "graduated"
    ESTABLISHED = "established"
    DECLINING = "declining"
    DEAD = "dead"


def classify_phase(token_state: dict) -> Phase:
    """Heuristic classifier given a current snapshot of a token's state."""
    if not token_state.get("liquidity_usd"):
        return Phase.PRE_LAUNCH
    if token_state.get("on_bonding_curve"):
        return Phase.BONDING
    age_days = token_state.get("age_days", 0)
    mcap = token_state.get("market_cap_usd", 0)
    vol_24h = token_state.get("volume_24h_usd", 0)
    if age_days < 1:
        return Phase.GRADUATED
    if vol_24h < 100 and age_days > 7:
        return Phase.DEAD
    if vol_24h < mcap * 0.005:
        return Phase.DECLINING
    return Phase.ESTABLISHED



class LifecycleTracker:
    """Replay a token's history into phase transitions."""

    def __init__(self):
        self._history: list[tuple[int, Phase]] = []

    def update(self, timestamp: int, state: dict) -> Phase:
        phase = classify_phase(state)
        if not self._history or self._history[-1][1] != phase:
            self._history.append((timestamp, phase))
        return phase

    @property
    def transitions(self):
        return list(self._history)

    def time_in_phase(self, phase: Phase) -> int:
        total = 0
        for i, (ts, p) in enumerate(self._history):
            if p != phase:
                continue
            end = self._history[i + 1][0] if i + 1 < len(self._history) else ts
            total += end - ts
        return total
