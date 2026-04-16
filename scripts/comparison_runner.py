"""
Comparison runner for benchmarking pathfinding algorithms.
Handles static path finding, traffic scenarios, and dynamic rerouting.
"""

import os
import time
import random
from typing import Dict, Any, Tuple
from src.algorithms.base import PathfindingAlgorithm
from src.utils.animation_data import AnimationDataCollector


def run_comparison(
    city: Any,
    start: Tuple[int, int],
    goal: Tuple[int, int],
    algorithm: PathfindingAlgorithm,
    save_animation: bool = False
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
        save_animation: Whether to save animation data to JSON

    Returns:
        Dict with comparison results
    """

    # Create animation collector if requested
    collector = None
    if save_animation:
        collector = AnimationDataCollector(
            algorithm_name=algorithm.name,
            grid_size=city.size,
            start=start,
            goal=goal
        )

    # Step 1: Find static path
    static_start_time = time.time()
    static_path, static_cost, static_visited = algorithm.find_path(
        city.graph, start, goal, animation_collector=collector
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

    # Step 2: Apply traffic scenario at multiple points along static path
    num_points = 5 if city.size > 100 else 1
    affected_edges = city.apply_traffic_scenario(
        path=static_path,
        num_points=num_points,
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

    # Save animation data if requested
    animation_file = None
    if save_animation and collector:
        edges = [(u, v, city.graph[u][v]['weight']) for u, v in city.graph.edges()]
        collector.set_graph_data(edges)
        collector.set_traffic_affected_edges(affected_edges)
        collector.set_result(static_path, static_cost, static_runtime)
        
        output_dir = os.path.join(os.path.dirname(__file__), "..", "results", "animation_data")
        os.makedirs(output_dir, exist_ok=True)
        animation_file = f"{output_dir}/{algorithm.name.replace(' ', '_')}_{start}_{goal}_{int(time.time() * 1000)}.json"
        collector.get_data().save(animation_file)
        print(f"[{algorithm.name}] Animation data saved to {animation_file}")

    return {
        "algorithm": algorithm.name,
        "success": True,
        "static_runtime": static_runtime,
        "dynamic_runtime": dynamic_runtime,
        "static_cost": static_cost,
        "cost_after_traffic": cost_after_traffic,
        "rerouted_cost": rerouted_cost,
        "improvement": cost_after_traffic - rerouted_cost
        if rerouted_path
        else 0,
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
