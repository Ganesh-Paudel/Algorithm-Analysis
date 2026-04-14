"""
Configuration management for algorithms and experiments.
Allows easy switching between algorithms and configuring their parameters.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class AlgorithmConfig:
    """Configuration for a specific algorithm."""

    name: str
    parameters: Dict[str, Any]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {"name": self.name, "parameters": self.parameters}


class ExperimentConfig:
    """Centralized configuration management for experiments."""

    # Default algorithm configurations
    DEFAULT_CONFIGS = {
        "astar": AlgorithmConfig(
            name="astar",
            parameters={},
        ),
        "genetic": AlgorithmConfig(
            name="genetic",
            parameters={
                "population_size": 50,
                "generations": 100,
                "mutation_rate": 0.2,
                "elite_ratio": 0.2,
            },
        ),
    }

    def __init__(self):
        """Initialize with default configurations."""
        self.configs: Dict[str, AlgorithmConfig] = {}
        self.active_algorithms: List[str] = []
        self._load_defaults()

    def _load_defaults(self):
        """Load default configurations."""
        self.configs = self.DEFAULT_CONFIGS.copy()

    def set_algorithm_config(self, algorithm_name: str, **kwargs):
        """
        Set or update configuration for an algorithm.

        Args:
            algorithm_name: Name of the algorithm
            **kwargs: Parameter overrides
        """
        algorithm_name = algorithm_name.lower()

        if algorithm_name not in self.configs:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")

        config = self.configs[algorithm_name]
        config.parameters.update(kwargs)

    def get_algorithm_config(self, algorithm_name: str) -> AlgorithmConfig:
        """Get configuration for an algorithm."""
        algorithm_name = algorithm_name.lower()
        if algorithm_name not in self.configs:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")
        return self.configs[algorithm_name]

    def get_algorithm_kwargs(self, algorithm_name: str) -> dict:
        """Get algorithm parameters as kwargs for factory."""
        config = self.get_algorithm_config(algorithm_name)
        return config.parameters.copy()

    def set_active_algorithms(self, *algorithm_names):
        """
        Set which algorithms should be tested.

        Args:
            *algorithm_names: Algorithm names to test
        """
        for algo in algorithm_names:
            if algo.lower() not in self.configs:
                raise ValueError(f"Unknown algorithm: {algo}")

        self.active_algorithms = [name.lower() for name in algorithm_names]

    def get_active_algorithms(self) -> List[str]:
        """Get list of active algorithms."""
        return self.active_algorithms.copy()

    def reset_to_defaults(self):
        """Reset all configurations to defaults."""
        self._load_defaults()
        self.active_algorithms = []

    def get_summary(self) -> str:
        """Get formatted summary of current configuration."""
        lines = ["=== Experiment Configuration ==="]

        if self.active_algorithms:
            lines.append(f"\nActive Algorithms: {', '.join(self.active_algorithms)}")

        for algo_name in sorted(self.configs.keys()):
            config = self.configs[algo_name]
            lines.append(f"\n{algo_name.upper()}:")
            if config.parameters:
                for key, value in config.parameters.items():
                    lines.append(f"  {key}: {value}")
            else:
                lines.append("  (no parameters)")

        return "\n".join(lines)


# Global configuration instance
_config = ExperimentConfig()


def get_config() -> ExperimentConfig:
    """Get the global configuration instance."""
    return _config


def reset_config():
    """Reset global configuration to defaults."""
    _config.reset_to_defaults()
