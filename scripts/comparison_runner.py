"""
Comparison runner for benchmarking pathfinding algorithms.
Handles static path finding, traffic scenarios, and dynamic rerouting.
"""

import time
import random
from typing import Dict, Any, Tuple
from ..src.algorithms.base import PathfindingAlgorithm


def run_comparison(
    city: Any,
    start: Tuple[int, int],
    goal: Tuple[int, int],
    algorithm: PathfindingAlgorithm,
) -> Dict[str, Any]:
    """
    Run comparison test for an algorithm.

    Compares:
    1. Static path cost before traffic event
    2. Path cost after traffic event (on same path)
    3. Rerouted path after dynamic replanning

    Args:
        city: TrafficEnvironment (CityGraph instance)
        start: Starting node (x, y)
        goal: Goal node (x, y)
        algorithm: PathfindingAlgorithm instance to test

    Returns:
        Dict with comparison results
    """

    # Step 1: Find static path
    static_start_time = time.time()
    static_path, static_cost, static_visited = algorithm.find_path(
        city.graph, start, goal
    )
    static_end_time = time.time()
    static_runtime = static_end_time - static_start_time

    if static_path is None:
        print(f"[{algorithm.name}] Failed to find initial path")
        return {
            "algorithm": algorithm.name,
            "success": False,
            "error": "No path found",
        }

    print(f"[{algorithm.name}] Static path found with cost {static_cost:.2f}")

    # Step 2: Apply traffic scenario to middle of the path
    middle_idx = len(static_path) // 2
    middle_node = static_path[middle_idx]

    affected_edges = city.apply_traffic_scenario(
        center_node=middle_node,
        radius=random.choice([3, 5, 8]),
        intensity=random.choice([15, 20, 30, 40]),
    )

    # Calculate cost of original path under traffic
    cost_after_traffic = algorithm.calculate_path_cost(city.graph, static_path)

    print(
        f"[{algorithm.name}] Cost after traffic: {cost_after_traffic:.2f} "
        f"(original: {static_cost:.2f})"
    )

    # Step 3: Find rerouted path (dynamic replanning)
    dynamic_start_time = time.time()
    rerouted_path, rerouted_cost, dynamic_visited = algorithm.find_path(
        city.graph, start, goal
    )
    dynamic_end_time = time.time()
    dynamic_runtime = dynamic_end_time - dynamic_start_time

    if rerouted_path is None:
        rerouted_cost = float("inf")

    print(f"[{algorithm.name}] Rerouted path cost: {rerouted_cost:.2f}")

    # Combine visited nodes from both runs
    all_visited = static_visited | dynamic_visited

    return {
        "algorithm": algorithm.name,
        "success": True,
        "static_runtime": static_runtime,
        "dynamic_runtime": dynamic_runtime,
        "static_cost": static_cost,
        "cost_after_traffic": cost_after_traffic,
        "rerouted_cost": rerouted_cost,
        "improvement": cost_after_traffic - rerouted_cost if rerouted_path else 0,
        "improvement_percent": (
            ((cost_after_traffic - rerouted_cost) / cost_after_traffic * 100)
            if rerouted_path and cost_after_traffic > 0
            else 0
        ),
        "static_path": static_path,
        "rerouted_path": rerouted_path,
        "affected_edges": affected_edges,
        "nodes_explored": len(all_visited),
    }
