"""
Unified comparison and visualization module.
Works with any algorithm through the PathfindingAlgorithm interface.
"""

import os
import time
import random
from typing import Dict, Any, Tuple, Optional, List
import networkx as nx
import matplotlib.pyplot as plt

from src.algorithms.base import PathfindingAlgorithm
from .results_aggregator import AlgorithmResult, ExperimentRound, ResultsAggregator


def _get_project_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _get_comparison_charts_dir() -> str:
    output_dir = os.path.join(
        _get_project_root(), "results", "charts", "ComparisonCharts"
    )
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def _resolve_output_dir(output_dir: Optional[str]) -> str:
    if output_dir is None:
        return _get_comparison_charts_dir()

    if not os.path.isabs(output_dir):
        output_dir = os.path.join(_get_project_root(), output_dir)

    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def run_algorithm_test(
    city: Any,
    start: Tuple[int, int],
    goal: Tuple[int, int],
    algorithm: PathfindingAlgorithm,
) -> AlgorithmResult:
    """
    Test an algorithm with traffic scenario.

    Tests:
    1. Static path (optimal path without traffic)
    2. Cost of static path under traffic
    3. Rerouted path (dynamic replanning after traffic)

    Args:
        city: TrafficEnvironment (CityGraph instance)
        start: Starting node (x, y)
        goal: Goal node (x, y)
        algorithm: PathfindingAlgorithm instance

    Returns:
        AlgorithmResult with all metrics
    """

    # Step 1: Find static path
    static_start_time = time.time()
    static_path, static_cost, static_visited = algorithm.find_path(
        city.graph, start, goal
    )
    static_end_time = time.time()
    static_runtime = static_end_time - static_start_time

    if static_path is None:
        return AlgorithmResult(
            algorithm=algorithm.name,
            grid_size=city.size,
            success=False,
            error="No path found in initial search",
        )

    # Step 2: Apply traffic scenario to middle of path
    middle_idx = len(static_path) // 2
    middle_node = static_path[middle_idx]

    affected_edges = city.apply_traffic_scenario(
        center_node=middle_node,
        radius=random.choice([3, 5, 8]),
        intensity=random.choice([15, 20, 30, 40]),
    )

    # Calculate cost of original path under traffic
    cost_after_traffic = algorithm.calculate_path_cost(city.graph, static_path)

    # Step 3: Find rerouted path (dynamic replanning)
    dynamic_start_time = time.time()
    rerouted_path, rerouted_cost, dynamic_visited = algorithm.find_path(
        city.graph, start, goal
    )
    dynamic_end_time = time.time()
    dynamic_runtime = dynamic_end_time - dynamic_start_time

    if rerouted_path is None:
        rerouted_cost = float("inf")
        improvement = 0
        improvement_percent = 0
    else:
        improvement = cost_after_traffic - rerouted_cost
        improvement_percent = (
            (improvement / cost_after_traffic * 100) if cost_after_traffic > 0 else 0
        )

    # Combine visited nodes from both runs
    all_visited = static_visited | dynamic_visited

    return AlgorithmResult(
        algorithm=algorithm.name,
        grid_size=city.size,
        success=True,
        static_cost=static_cost,
        cost_after_traffic=cost_after_traffic,
        rerouted_cost=rerouted_cost,
        improvement=improvement,
        improvement_percent=improvement_percent,
        nodes_explored=len(all_visited),
        static_runtime=static_runtime,
        dynamic_runtime=dynamic_runtime,
        static_path=static_path,
        rerouted_path=rerouted_path,
        affected_edges=affected_edges,
    )


def visualize_path_comparison(
    graph: nx.Graph,
    static_path: Optional[List],
    rerouted_path: Optional[List],
    affected_edges: List[Tuple],
    algorithm_name: str,
    title: str = "",
    output_path: Optional[str] = None,
) -> None:
    """
    Visualize static and rerouted paths on the graph.

    Args:
        graph: NetworkX graph
        static_path: Original path before traffic
        rerouted_path: New path after rerouting
        affected_edges: Edges affected by traffic
        algorithm_name: Name of algorithm for file naming
        title: Title for the plot
        output_path: Optional path to save the figure
    """
    if static_path is None and rerouted_path is None:
        print(f"Warning: No valid paths to visualize for {title}")
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Draw static path only, without nodes
    pos = {node: node for node in graph.nodes()}

    # Left plot: Static path
    ax1.set_title(f"Static Path - {title}", fontsize=12, fontweight="bold")

    if static_path:
        path_edges = list(zip(static_path, static_path[1:]))
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=path_edges,
            edge_color="green",
            width=2.5,
            ax=ax1,
            label="Original Path",
        )

    if affected_edges:
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=affected_edges,
            edge_color="red",
            width=2,
            alpha=0.7,
            ax=ax1,
            style="dashed",
            label="Traffic Affected",
        )

    ax1.legend(loc="upper left", fontsize=10)
    ax1.axis("off")

    # Right plot: Rerouted path
    ax2.set_title(f"Rerouted Path - {title}", fontsize=12, fontweight="bold")

    if rerouted_path:
        path_edges = list(zip(rerouted_path, rerouted_path[1:]))
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=path_edges,
            edge_color="blue",
            width=2.5,
            ax=ax2,
            label="Rerouted Path",
        )

    if affected_edges:
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=affected_edges,
            edge_color="red",
            width=2,
            alpha=0.7,
            ax=ax2,
            style="dashed",
            label="Traffic Affected",
        )

    ax2.legend(loc="upper left", fontsize=10)
    ax2.axis("off")

    plt.tight_layout()

    if output_path is None:
        output_path = os.path.join(
            _get_comparison_charts_dir(), f"{algorithm_name}_path.png"
        )
    else:
        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

    try:
        plt.savefig(output_path, dpi=100, bbox_inches="tight")
        print("saved")
        print(f"Saved visualization to {output_path}")
    except Exception as e:
        print("error")
        print(f"Error saving visualization: {e}")
    finally:
        plt.close()


def visualize_comparison_charts(
    results_aggregator: ResultsAggregator,
    output_dir: Optional[str] = None,
) -> None:
    """
    Generate comparison charts from aggregated results.

    Creates:
    1. Success rate comparison
    2. Cost comparison (static vs rerouted)
    3. Improvement percentage
    4. Runtime comparison
    5. Nodes explored comparison

    Args:
        results_aggregator: ResultsAggregator with all results
        output_dir: Directory to save charts
    """
    output_dir = _resolve_output_dir(output_dir)

    comparison_data = results_aggregator.get_comparison_table()

    if not comparison_data:
        print("No data to visualize")
        return

    # Extract algorithms and grid sizes
    algorithms = list(comparison_data.keys())
    grid_sizes = set()

    for algo_results in comparison_data.values():
        for result in algo_results:
            grid_sizes.add(result["size"])

    grid_sizes = sorted(grid_sizes)

    # Create comparison visualizations
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Algorithm Comparison - Key Metrics", fontsize=16, fontweight="bold")

    # 1. Success Rate
    ax = axes[0, 0]
    success_rates = {}
    for algo in algorithms:
        results = comparison_data[algo]
        successful = sum(1 for r in results if r["success"])
        success_rates[algo] = (successful / len(results) * 100) if results else 0

    ax.bar(algorithms, success_rates.values(), color=["#1f77b4", "#ff7f0e", "#2ca02c"])
    ax.set_ylabel("Success Rate (%)")
    ax.set_title("Success Rate")
    ax.set_ylim([0, 105])
    for i, v in enumerate(success_rates.values()):
        ax.text(i, v + 2, f"{v:.1f}%", ha="center", va="bottom")

    # 2. Average Static Cost by Grid Size
    ax = axes[0, 1]
    for algo in algorithms:
        costs_by_size = {}
        for result in comparison_data[algo]:
            if result["success"] and result["static_cost"] is not None:
                size = result["size"]
                if size not in costs_by_size:
                    costs_by_size[size] = []
                costs_by_size[size].append(result["static_cost"])

        avg_costs = [
            sum(costs_by_size[size]) / len(costs_by_size[size])
            for size in sorted(costs_by_size.keys())
        ]
        ax.plot(sorted(costs_by_size.keys()), avg_costs, marker="o", label=algo)

    ax.set_xlabel("Grid Size")
    ax.set_ylabel("Average Cost")
    ax.set_title("Static Path Cost by Grid Size")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 3. Average Rerouted Cost by Grid Size
    ax = axes[0, 2]
    for algo in algorithms:
        costs_by_size = {}
        for result in comparison_data[algo]:
            if result["success"] and result["rerouted_cost"] is not None:
                size = result["size"]
                if size not in costs_by_size:
                    costs_by_size[size] = []
                costs_by_size[size].append(result["rerouted_cost"])

        avg_costs = [
            sum(costs_by_size[size]) / len(costs_by_size[size])
            for size in sorted(costs_by_size.keys())
        ]
        ax.plot(sorted(costs_by_size.keys()), avg_costs, marker="s", label=algo)

    ax.set_xlabel("Grid Size")
    ax.set_ylabel("Average Cost")
    ax.set_title("Rerouted Path Cost by Grid Size")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 4. Average Improvement Percentage
    ax = axes[1, 0]
    for algo in algorithms:
        improvements_by_size = {}
        for result in comparison_data[algo]:
            if result["success"] and result["improvement_percent"] is not None:
                size = result["size"]
                if size not in improvements_by_size:
                    improvements_by_size[size] = []
                improvements_by_size[size].append(result["improvement_percent"])

        avg_improvements = [
            sum(improvements_by_size[size]) / len(improvements_by_size[size])
            for size in sorted(improvements_by_size.keys())
        ]
        ax.plot(
            sorted(improvements_by_size.keys()),
            avg_improvements,
            marker="^",
            label=algo,
        )

    ax.set_xlabel("Grid Size")
    ax.set_ylabel("Improvement (%)")
    ax.set_title("Average Improvement Percentage")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 5. Average Nodes Explored
    ax = axes[1, 1]
    for algo in algorithms:
        nodes_by_size = {}
        for result in comparison_data[algo]:
            if result["success"]:
                size = result["size"]
                if size not in nodes_by_size:
                    nodes_by_size[size] = []
                nodes_by_size[size].append(result["nodes_explored"])

        avg_nodes = [
            sum(nodes_by_size[size]) / len(nodes_by_size[size])
            for size in sorted(nodes_by_size.keys())
        ]
        ax.plot(sorted(nodes_by_size.keys()), avg_nodes, marker="d", label=algo)

    ax.set_xlabel("Grid Size")
    ax.set_ylabel("Average Nodes Explored")
    ax.set_title("Search Space Exploration")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 6. Runtime Comparison
    ax = axes[1, 2]
    total_runtimes = {}
    for algo in algorithms:
        results = comparison_data[algo]
        total_runtime = sum(
            r["static_runtime"] + r["dynamic_runtime"] for r in results if r["success"]
        )
        total_runtimes[algo] = total_runtime

    ax.bar(algorithms, total_runtimes.values(), color=["#1f77b4", "#ff7f0e", "#2ca02c"])
    ax.set_ylabel("Total Runtime (seconds)")
    ax.set_title("Total Runtime Across All Experiments")
    for i, v in enumerate(total_runtimes.values()):
        ax.text(i, v + 0.01, f"{v:.3f}s", ha="center", va="bottom")

    plt.tight_layout()
    output_path = f"{output_dir}/comparison_metrics.png"

    try:
        plt.savefig(output_path, dpi=100, bbox_inches="tight")
        print(f"Saved comparison chart to {output_path}")
    except Exception as e:
        print(f"Error saving chart: {e}")
    finally:
        plt.close()
