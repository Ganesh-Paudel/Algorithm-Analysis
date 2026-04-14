"""Traffic simulation environments package."""

# Manual imports only: expose the canonical environment implementation.
from .traffic import CityGraph

__all__ = ["CityGraph"]
