"""Abstract base class for per-chain data backends."""
from abc import ABC, abstractmethod


class ChainBackend(ABC):
    name: str

    @abstractmethod
    def top_holders(self, token: str, limit: int = 100) -> list[dict]:
        ...

    @abstractmethod
    def total_supply(self, token: str) -> int:
        ...
