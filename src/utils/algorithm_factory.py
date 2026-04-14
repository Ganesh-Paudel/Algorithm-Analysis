"""
Algorithm factory for easy switching between pathfinding algorithms.
Provides factory methods and algorithm registry.
"""

from typing import Type, Dict, Optional
from ..algorithms.base import PathfindingAlgorithm
from ..algorithms.aStar import AStarPathfinder
from ..algorithms.geneticAlgo import GeneticPathfinder


class AlgorithmFactory:
    """Factory for creating and managing pathfinding algorithms."""

    _algorithms: Dict[str, Type[PathfindingAlgorithm]] = {
        "astar": AStarPathfinder,
        "genetic": GeneticPathfinder,
    }

    @classmethod
    def create(cls, algorithm_name: str, **kwargs) -> Optional[PathfindingAlgorithm]:
        """
        Create an algorithm instance by name.

        Args:
            algorithm_name: Name of the algorithm ('astar' or 'genetic')
            **kwargs: Additional arguments to pass to the algorithm constructor

        Returns:
            Algorithm instance, or None if algorithm not found
        """
        algorithm_name = algorithm_name.lower()

        if algorithm_name not in cls._algorithms:
            available = ", ".join(cls._algorithms.keys())
            raise ValueError(
                f"Unknown algorithm '{algorithm_name}'. Available: {available}"
            )

        algorithm_class = cls._algorithms[algorithm_name]
        return algorithm_class(**kwargs)

    @classmethod
    def register(
        cls, algorithm_name: str, algorithm_class: Type[PathfindingAlgorithm]
    ) -> None:
        """
        Register a new algorithm.

        Args:
            algorithm_name: Name to register the algorithm as
            algorithm_class: The algorithm class (must inherit from PathfindingAlgorithm)
        """
        if not issubclass(algorithm_class, PathfindingAlgorithm):
            raise TypeError(
                f"{algorithm_class.__name__} must inherit from PathfindingAlgorithm"
            )

        cls._algorithms[algorithm_name.lower()] = algorithm_class

    @classmethod
    def get_available(cls) -> list:
        """Get list of available algorithms."""
        return list(cls._algorithms.keys())

    @classmethod
    def get_algorithm_config(cls, algorithm_name: str) -> dict:
        """
        Get configuration options for an algorithm.

        Returns a dict with parameter names and suggested values.
        """
        config = {
            "astar": {
                "description": "A* algorithm - deterministic, optimal",
                "parameters": {},
            },
            "genetic": {
                "description": "Genetic algorithm - heuristic, parallelizable",
                "parameters": {
                    "population_size": {"default": 50, "range": (10, 200)},
                    "generations": {"default": 100, "range": (10, 500)},
                    "mutation_rate": {"default": 0.2, "range": (0.0, 1.0)},
                    "elite_ratio": {"default": 0.2, "range": (0.0, 1.0)},
                },
            },
        }

        return config.get(algorithm_name.lower(), {})
