"""
Unified comparison module for pathfinding algorithms.
Provides standardized testing, visualization, and comparison functionality.
"""

import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional
from pathlib import Path
import numpy as np

from traffic_environment import CityGraph
from algorithm_factory import AlgorithmFactory
from config import get_config
from results_aggregator import ResultsAggregator, ExperimentRound


class UnifiedComparison:
    """Unified comparison framework for pathfinding algorithms."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.aggregator = ResultsAggregator()
        self.environment = None

    def setup_environment(self, size: int = 20, obstacles: int = 50):
        """Setup the traffic environment for testing."""
        self.environment = CityGraph(size=size, num_obstacles=obstacles)
        return self.environment

    def run_algorithm_test(self, algorithm_name: str, start: tuple, goal: tuple,
                          max_time: float = 30.0) -> Dict[str, Any]:
        """
        Run a single algorithm test with standardized metrics.

        Args:
            algorithm_name: Name of the algorithm to test
            start: Starting position (x, y)
            goal: Goal position (x, y)
            max_time: Maximum time to allow for computation

        Returns:
            Dictionary with test results
        """
        if not self.environment:
            raise ValueError("Environment not set up. Call setup_environment() first.")

        # Create algorithm instance
        algorithm = AlgorithmFactory.create(algorithm_name)
        if not algorithm:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")

        # Initialize algorithm with environment
        algorithm.initialize(self.environment)

        # Time the execution
        start_time = time.time()
        try:
            path = algorithm.find_path(start, goal, max_time=max_time)
            execution_time = time.time() - start_time

            # Calculate metrics
            path_cost = self._calculate_path_cost(path) if path else float('inf')
            path_length = len(path) if path else 0
            success = path is not None and len(path) > 0

            return {
                'algorithm': algorithm_name,
                'success': success,
                'path': path,
                'path_length': path_length,
                'path_cost': path_cost,
                'execution_time': execution_time,
                'start': start,
                'goal': goal
            }

        except Exception as e:
            execution_time = time.time() - start_time
            return {
                'algorithm': algorithm_name,
                'success': False,
                'path': None,
                'path_length': 0,
                'path_cost': float('inf'),
                'execution_time': execution_time,
                'start': start,
                'goal': goal,
                'error': str(e)
            }

    def run_comparison_test(self, algorithms: List[str], start: tuple, goal: tuple,
                           num_runs: int = 5) -> pd.DataFrame:
        """
        Run comparison tests between multiple algorithms.

        Args:
            algorithms: List of algorithm names to compare
            start: Starting position
            goal: Goal position
            num_runs: Number of runs for each algorithm

        Returns:
            DataFrame with comparison results
        """
        results = []

        for algorithm in algorithms:
            print(f"Testing {algorithm}...")
            for run in range(num_runs):
                result = self.run_algorithm_test(algorithm, start, goal)
                result['run'] = run + 1
                results.append(result)

        return pd.DataFrame(results)

    def _calculate_path_cost(self, path: List[tuple]) -> float:
        """Calculate the total cost of a path."""
        if not path or len(path) < 2:
            return float('inf')

        total_cost = 0
        for i in range(len(path) - 1):
            current = path[i]
            next_pos = path[i + 1]
            # Calculate Euclidean distance as cost
            cost = np.sqrt((next_pos[0] - current[0])**2 + (next_pos[1] - current[1])**2)
            total_cost += cost

        return total_cost

    def visualize_path_comparison(self, results_df: pd.DataFrame,
                                 save_path: Optional[str] = None):
        """Create visualization comparing paths found by different algorithms."""
        if self.environment is None:
            raise ValueError("Environment not set up for visualization")

        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        # Plot 1: Environment with paths
        ax1 = axes[0]
        self._plot_environment(ax1)

        colors = ['blue', 'red', 'green', 'orange', 'purple']
        for i, (_, row) in enumerate(results_df.iterrows()):
            if row['success'] and row['path']:
                color = colors[i % len(colors)]
                path = row['path']
                ax1.plot([p[0] for p in path], [p[1] for p in path],
                        color=color, linewidth=2, alpha=0.7,
                        label=f"{row['algorithm']} (cost: {row['path_cost']:.2f})")

        ax1.legend()
        ax1.set_title("Path Comparison")
        ax1.grid(True, alpha=0.3)

        # Plot 2: Performance metrics
        ax2 = axes[1]
        successful_results = results_df[results_df['success']]

        if not successful_results.empty:
            # Execution time comparison
            time_data = successful_results.groupby('algorithm')['execution_time'].mean()
            time_data.plot(kind='bar', ax=ax2, position=0, width=0.3,
                          label='Avg Time (s)', alpha=0.7)

            # Path cost comparison
            cost_data = successful_results.groupby('algorithm')['path_cost'].mean()
            cost_data.plot(kind='bar', ax=ax2, position=1, width=0.3,
                          label='Avg Cost', alpha=0.7, color='orange')

            ax2.set_title("Performance Comparison")
            ax2.set_ylabel("Value")
            ax2.legend()
            ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to: {save_path}")

        plt.show()

    def visualize_comparison_charts(self, results_df: pd.DataFrame,
                                   save_dir: Optional[str] = None):
        """Create comprehensive comparison charts."""
        if save_dir:
            Path(save_dir).mkdir(parents=True, exist_ok=True)

        successful_results = results_df[results_df['success']]

        if successful_results.empty:
            print("No successful results to visualize")
            return

        # Create multiple comparison charts
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # 1. Execution Time Box Plot
        successful_results.boxplot(column='execution_time', by='algorithm', ax=axes[0,0])
        axes[0,0].set_title("Execution Time Distribution")
        axes[0,0].set_ylabel("Time (seconds)")

        # 2. Path Cost Box Plot
        successful_results.boxplot(column='path_cost', by='algorithm', ax=axes[0,1])
        axes[0,1].set_title("Path Cost Distribution")
        axes[0,1].set_ylabel("Cost")

        # 3. Success Rate
        success_rate = results_df.groupby('algorithm')['success'].mean() * 100
        success_rate.plot(kind='bar', ax=axes[1,0], color='green', alpha=0.7)
        axes[1,0].set_title("Success Rate (%)")
        axes[1,0].set_ylabel("Success Rate (%)")
        axes[1,0].grid(True, alpha=0.3)

        # 4. Path Length vs Cost Scatter
        for algorithm in successful_results['algorithm'].unique():
            data = successful_results[successful_results['algorithm'] == algorithm]
            axes[1,1].scatter(data['path_length'], data['path_cost'],
                            label=algorithm, alpha=0.6, s=50)
        axes[1,1].set_xlabel("Path Length")
        axes[1,1].set_ylabel("Path Cost")
        axes[1,1].set_title("Path Length vs Cost")
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)

        plt.suptitle("Algorithm Comparison Analysis", fontsize=16)
        plt.tight_layout()

        if save_dir:
            chart_path = Path(save_dir) / "comprehensive_comparison.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            print(f"Comprehensive comparison chart saved to: {chart_path}")

        plt.show()

    def _plot_environment(self, ax):
        """Plot the environment grid with obstacles."""
        size = self.environment.size
        ax.set_xlim(-1, size)
        ax.set_ylim(-1, size)

        # Plot obstacles
        for obstacle in self.environment.obstacles:
            ax.add_patch(plt.Rectangle((obstacle[0]-0.5, obstacle[1]-0.5), 1, 1,
                                     color='black', alpha=0.7))

        # Plot grid
        for i in range(size + 1):
            ax.axhline(i - 0.5, color='gray', alpha=0.3)
            ax.axvline(i - 0.5, color='gray', alpha=0.3)


# Convenience functions for easy access
def run_algorithm_test(algorithm_name: str, start: tuple, goal: tuple,
                      environment: CityGraph = None, max_time: float = 30.0) -> Dict[str, Any]:
    """Convenience function to run a single algorithm test."""
    comparator = UnifiedComparison()
    if environment:
        comparator.environment = environment
    else:
        comparator.setup_environment()
    return comparator.run_algorithm_test(algorithm_name, start, goal, max_time)


def visualize_path_comparison(results_df: pd.DataFrame, save_path: Optional[str] = None):
    """Convenience function for path visualization."""
    comparator = UnifiedComparison()
    comparator.setup_environment()  # Setup with default parameters
    comparator.visualize_path_comparison(results_df, save_path)


def visualize_comparison_charts(results_df: pd.DataFrame, save_dir: Optional[str] = None):
    """Convenience function for comparison charts."""
    comparator = UnifiedComparison()
    comparator.visualize_comparison_charts(results_df, save_dir)