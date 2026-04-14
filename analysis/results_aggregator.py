"""
Results aggregator and analyzer for algorithm comparisons.
Collects and organizes comparison results for visualization and analysis.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
import json


@dataclass
class AlgorithmResult:
    """Result from running a single algorithm."""

    algorithm: str
    grid_size: int
    success: bool
    static_cost: Optional[float] = None
    cost_after_traffic: Optional[float] = None
    rerouted_cost: Optional[float] = None
    improvement: Optional[float] = None
    improvement_percent: Optional[float] = None
    nodes_explored: int = 0
    static_runtime: float = 0.0
    dynamic_runtime: float = 0.0
    error: Optional[str] = None
    static_path: Optional[List] = None
    rerouted_path: Optional[List] = None
    affected_edges: Optional[List] = None


@dataclass
class ExperimentRound:
    """Complete results from testing all algorithms on one test case."""

    round_number: int
    grid_size: int
    start: tuple
    goal: tuple
    results: Dict[str, AlgorithmResult] = field(default_factory=dict)

    def add_result(self, result: AlgorithmResult):
        """Add a result from an algorithm."""
        self.results[result.algorithm] = result

    def get_successful_algorithms(self) -> List[str]:
        """Get list of algorithms that found a path."""
        return [
            algo for algo, result in self.results.items() if result.success
        ]

    def get_best_static_cost(self) -> Optional[float]:
        """Get best static path cost among successful algorithms."""
        successful = [
            r.static_cost for r in self.results.values()
            if r.success and r.static_cost is not None
        ]
        return min(successful) if successful else None

    def get_best_rerouted_cost(self) -> Optional[float]:
        """Get best rerouted path cost among successful algorithms."""
        successful = [
            r.rerouted_cost for r in self.results.values()
            if r.success and r.rerouted_cost is not None
        ]
        return min(successful) if successful else None

    def get_best_improvement(self) -> Optional[float]:
        """Get best improvement percentage."""
        improvements = [
            r.improvement_percent for r in self.results.values()
            if r.success and r.improvement_percent is not None
        ]
        return max(improvements) if improvements else None


class ResultsAggregator:
    """Aggregates and analyzes results from multiple experiments."""

    def __init__(self):
        """Initialize results aggregator."""
        self.rounds: List[ExperimentRound] = []

    def add_round(self, round_result: ExperimentRound):
        """Add a completed experiment round."""
        self.rounds.append(round_result)

    def get_round(self, round_number: int) -> Optional[ExperimentRound]:
        """Get results from a specific round."""
        for round_result in self.rounds:
            if round_result.round_number == round_number:
                return round_result
        return None

    def get_all_rounds(self) -> List[ExperimentRound]:
        """Get all experiment rounds."""
        return self.rounds.copy()

    def get_summary_by_algorithm(self, algorithm: str) -> Dict[str, Any]:
        """Get aggregated statistics for a specific algorithm across all rounds."""
        results = [
            r.results[algorithm]
            for r in self.rounds
            if algorithm in r.results
        ]

        successful = [r for r in results if r.success]

        if not successful:
            return {
                "algorithm": algorithm,
                "total_runs": len(results),
                "successful": 0,
                "success_rate": 0.0,
            }

        return {
            "algorithm": algorithm,
            "total_runs": len(results),
            "successful": len(successful),
            "success_rate": len(successful) / len(results) * 100,
            "avg_static_cost": sum(r.static_cost for r in successful) / len(successful),
            "avg_rerouted_cost": sum(r.rerouted_cost for r in successful) / len(successful),
            "avg_improvement": sum(r.improvement for r in successful) / len(successful),
            "avg_improvement_percent": sum(r.improvement_percent for r in successful) / len(successful),
            "avg_nodes_explored": sum(r.nodes_explored for r in successful) / len(successful),
            "avg_static_runtime": sum(r.static_runtime for r in successful) / len(successful),
            "avg_dynamic_runtime": sum(r.dynamic_runtime for r in successful) / len(successful),
        }

    def get_comparison_table(self) -> Dict[str, List[Any]]:
        """Get comparison data suitable for visualization."""
        algorithms = set()
        for round_result in self.rounds:
            algorithms.update(round_result.results.keys())

        comparison = {algo: [] for algo in algorithms}

        for round_result in self.rounds:
            for algo in algorithms:
                if algo in round_result.results:
                    result = round_result.results[algo]
                    comparison[algo].append({
                        "round": round_result.round_number,
                        "size": round_result.grid_size,
                        "success": result.success,
                        "static_cost": result.static_cost,
                        "rerouted_cost": result.rerouted_cost,
                        "improvement_percent": result.improvement_percent,
                        "nodes_explored": result.nodes_explored,
                        "static_runtime": result.static_runtime,
                        "dynamic_runtime": result.dynamic_runtime,
                    })

        return comparison

    def to_json(self) -> str:
        """Serialize results to JSON."""
        data = []
        for round_result in self.rounds:
            round_data = {
                "round": round_result.round_number,
                "grid_size": round_result.grid_size,
                "start": round_result.start,
                "goal": round_result.goal,
                "results": {
                    algo: asdict(result)
                    for algo, result in round_result.results.items()
                }
            }
            data.append(round_data)

        return json.dumps(data, indent=2, default=str)

    def print_summary(self):
        """Print a formatted summary of all results."""
        print("\n" + "=" * 80)
        print("EXPERIMENT SUMMARY")
        print("=" * 80)

        algorithms = set()
        for round_result in self.rounds:
            algorithms.update(round_result.results.keys())

        for algo in sorted(algorithms):
            summary = self.get_summary_by_algorithm(algo)
            print(f"\n{algo.upper()}")
            print("-" * 40)
            print(f"  Total Runs: {summary['total_runs']}")
            print(f"  Successful: {summary['successful']} ({summary['success_rate']:.1f}%)")

            if summary['successful'] > 0:
                print(f"  Avg Static Cost: {summary['avg_static_cost']:.2f}")
                print(f"  Avg Rerouted Cost: {summary['avg_rerouted_cost']:.2f}")
                print(f"  Avg Improvement: {summary['avg_improvement_percent']:.1f}%")
                print(f"  Avg Nodes Explored: {summary['avg_nodes_explored']:.0f}")
                print(f"  Avg Static Runtime: {summary['avg_static_runtime']:.4f}s")
                print(f"  Avg Dynamic Runtime: {summary['avg_dynamic_runtime']:.4f}s")
