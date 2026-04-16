"""
Base class for all pathfinding algorithms.
Provides a common interface for A*, Genetic Algorithm, and other algorithms.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Set, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.utils.animation_data import AnimationDataCollector


class PathfindingAlgorithm(ABC):
    """Abstract base class for pathfinding algorithms."""

    @abstractmethod
    def find_path(
        self, graph: Any, start: Tuple[int, int], goal: Tuple[int, int],
        animation_collector: Optional["AnimationDataCollector"] = None
    ) -> Tuple[Optional[list], float, Set]:
        """
        Find a path from start to goal.

        Args:
            graph: NetworkX graph representing the environment
            start: Starting node tuple (x, y)
            goal: Goal node tuple (x, y)
            animation_collector: Optional animation data collector for step-by-step visualization

        Returns:
            Tuple of (path, cost, visited_nodes)
            - path: List of nodes from start to goal, or None if not found
            - cost: Total cost of the path
            - visited_nodes: Set of all nodes explored during search
        """
        pass

    @staticmethod
    def calculate_path_cost(graph: Any, path: list, weight: str = "weight") -> float:
        """
        Calculate the total cost of a path.

        Args:
            graph: NetworkX graph
            path: List of nodes representing the path
            weight: Edge weight attribute name

        Returns:
            Total cost of the path, or infinity if path is invalid
        """
        if path is None or len(path) == 0:
            return float("inf")

        total_cost = 0.0
        try:
            for u, v in zip(path, path[1:]):
                if not graph.has_edge(u, v):
                    return float("inf")
                edge_data = graph[u][v]
                total_cost += edge_data.get(weight, 1.0)
        except (KeyError, TypeError):
            return float("inf")

        return total_cost

    @staticmethod
    def validate_path(graph: Any, path: list) -> bool:
        """
        Validate that a path is valid in the graph.

        Args:
            graph: NetworkX graph
            path: List of nodes

        Returns:
            True if path is valid, False otherwise
        """
        if not path or len(path) < 2:
            return False

        for u, v in zip(path, path[1:]):
            if not graph.has_edge(u, v):
                return False

        return True
