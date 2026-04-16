"""
Example: Generate animation data for Manim visualization

This script shows how to:
1. Run algorithms with animation data collection
2. Save the data as JSON for independent animation generation
3. Load the saved data later without re-running algorithms
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.environments.traffic import CityGraph
from src.algorithms.aStar import AStarPathfinder
from src.algorithms.geneticAlgo import GeneticPathfinder
from src.utils.animation_data import AnimationDataCollector


def generate_animation_data():
    """
    Run algorithms with animation data collection.
    Saves JSON files that can be used to generate Manim animations independently.
    """

    print("=" * 60)
    print("Generating Animation Data for Manim Visualization")
    print("=" * 60)

    # Create a small city graph for testing
    print("\n1. Creating city graph (20x20 grid)...")
    city = CityGraph(size=100, seed=42)
    start = (0, 10)
    goal = (91, 89)

    print(f"   Start: {start}, Goal: {goal}")

    # Test A* algorithm with animation collection
    print("\n2. Running A* algorithm with animation collection...")
    astar = AStarPathfinder()

    # Create animation collector
    collector_astar = AnimationDataCollector(
        algorithm_name="A*", grid_size=city.size, start=start, goal=goal
    )

    # Run algorithm with animation collection
    import time

    start_time = time.time()
    path, cost, visited = astar.find_path(
        city.graph, start, goal, animation_collector=collector_astar
    )
    exec_time = time.time() - start_time

    print(f"   ✓ Path found with cost: {cost:.2f}")
    print(f"   ✓ Nodes explored: {len(visited)}")
    print(f"   ✓ Execution time: {exec_time:.4f}s")
    print(f"   ✓ Animation steps recorded: {len(collector_astar.data.steps)}")

    # Save animation data
    print("\n3. Saving animation data to JSON...")
    output_dir = os.path.join(
        os.path.dirname(__file__), "..", "results", "animation_data"
    )
    os.makedirs(output_dir, exist_ok=True)

    astar_file = os.path.join(output_dir, "astar_example.json")
    collector_astar.set_result(path, cost, exec_time)
    edges = [(u, v, city.graph[u][v]["weight"]) for u, v in city.graph.edges()]
    collector_astar.set_graph_data(edges)
    collector_astar.get_data().save(astar_file)
    print(f"   ✓ Saved to: {astar_file}")

    # Test Genetic Algorithm with animation collection
    print("\n4. Running Genetic Algorithm with animation collection...")
    ga = GeneticPathfinder(population_size=10, generations=15)

    collector_ga = AnimationDataCollector(
        algorithm_name="Genetic Algorithm", grid_size=city.size, start=start, goal=goal
    )

    start_time = time.time()
    path_ga, cost_ga, visited_ga = ga.find_path(
        city.graph, start, goal, animation_collector=collector_ga
    )
    exec_time_ga = time.time() - start_time

    print(f"   ✓ Path found with cost: {cost_ga:.2f}")
    print(f"   ✓ Nodes explored: {len(visited_ga)}")
    print(f"   ✓ Execution time: {exec_time_ga:.4f}s")
    print(f"   ✓ Animation steps recorded: {len(collector_ga.data.steps)}")

    # Save GA animation data
    ga_file = os.path.join(output_dir, "genetic_algo_example.json")
    collector_ga.set_result(path_ga, cost_ga, exec_time_ga)
    collector_ga.set_graph_data(edges)
    collector_ga.get_data().save(ga_file)
    print(f"   ✓ Saved to: {ga_file}")

    # Example: Load animation data later (without re-running algorithms)
    print("\n5. Loading animation data from JSON (demonstrating reuse)...")
    from src.utils.animation_data import AlgorithmAnimationData

    loaded_data = AlgorithmAnimationData.from_json(astar_file)
    print(f"   ✓ Loaded A* animation data:")
    print(f"      - Algorithm: {loaded_data.algorithm_name}")
    print(f"      - Grid size: {loaded_data.grid_size}x{loaded_data.grid_size}")
    print(f"      - Total steps: {len(loaded_data.steps)}")
    print(f"      - Final path cost: {loaded_data.path_cost:.2f}")

    print("\n" + "=" * 60)
    print("✓ Animation data generation complete!")
    print("\nYou can now:")
    print("  1. Load these JSON files in Manim to generate animations")
    print("  2. Iterate on animation visuals without re-running algorithms")
    print("  3. Share JSON files with colleagues for collaborative animation work")
    print("=" * 60)


if __name__ == "__main__":
    generate_animation_data()
