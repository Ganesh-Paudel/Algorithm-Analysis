"""
Quick testing script - demonstrates easy algorithm switching.
Useful for testing individual algorithms or quick experiments.
"""

import pandas as pd
from src.environments.traffic import CityGraph
from src.utils.algorithm_factory import AlgorithmFactory
from config.settings import get_config
from analysis.comparison import run_algorithm_test


def quick_test(algorithm_name: str = "astar", grid_size: int = 20):
    """
    Quick test of a single algorithm.

    Args:
        algorithm_name: "astar" or "genetic"
        grid_size: Size of grid to test
    """
    print("\n" + "=" * 60)
    print(f"Quick Test: {algorithm_name.upper()}")
    print("=" * 60)

    # Create city
    city = CityGraph(size=grid_size)

    # Simple start and goal
    start = (5, 5)
    goal = (grid_size - 5, grid_size - 5)

    # Configure if needed
    config = get_config()
    if algorithm_name == "genetic":
        config.set_algorithm_config(
            "genetic",
            population_size=50,
            generations=100,
            mutation_rate=0.2,
        )

    # Create algorithm
    algo_kwargs = config.get_algorithm_kwargs(algorithm_name)
    algorithm = AlgorithmFactory.create(algorithm_name, **algo_kwargs)

    print(f"\nAlgorithm: {algorithm.name}")
    print(f"Grid size: {grid_size}x{grid_size}")
    print(f"Start: {start}, Goal: {goal}\n")

    # Run test
    result = run_algorithm_test(city, start, goal, algorithm)

    if result.success:
        print(f"✓ Static path cost: {result.static_cost:.2f}")
        print(f"✓ Cost after traffic: {result.cost_after_traffic:.2f}")
        print(f"✓ Rerouted path cost: {result.rerouted_cost:.2f}")
        print(f"✓ Improvement: {result.improvement_percent:.1f}%")
        print(f"✓ Nodes explored: {result.nodes_explored}")
        print(f"✓ Static runtime: {result.static_runtime:.4f}s")
        print(f"✓ Dynamic runtime: {result.dynamic_runtime:.4f}s")
    else:
        print(f"✗ Failed: {result.error}")

    print("=" * 60 + "\n")

    return result


def compare_all_algorithms(grid_size: int = 20):
    """
    Compare all available algorithms with default settings.

    Args:
        grid_size: Size of grid to test
    """
    print("\n" + "=" * 60)
    print("Algorithm Comparison - All Available")
    print("=" * 60)

    config = get_config()
    available = AlgorithmFactory.get_available()

    results = {}
    for algo_name in available:
        result = quick_test(algo_name, grid_size)
        results[algo_name] = result

    # Summary comparison
    print("\nCOMPARISON SUMMARY:")
    print("-" * 60)

    for algo_name, result in results.items():
        if result.success:
            print(f"\n{algo_name.upper()}:")
            print(f"  Static Cost: {result.static_cost:.2f}")
            print(f"  Rerouted Cost: {result.rerouted_cost:.2f}")
            print(f"  Improvement: {result.improvement_percent:.1f}%")
            print(f"  Nodes Explored: {result.nodes_explored}")
            print(f"  Total Runtime: {result.static_runtime + result.dynamic_runtime:.4f}s")
        else:
            print(f"\n{algo_name.upper()}: FAILED - {result.error}")

    print("\n" + "=" * 60 + "\n")


def test_with_custom_parameters():
    """Test genetic algorithm with custom parameters."""
    print("\n" + "=" * 60)
    print("Custom Configuration Test")
    print("=" * 60)

    config = get_config()

    # Test different genetic algorithm configurations
    configs = [
        {"label": "Small Population", "population_size": 20, "generations": 50},
        {"label": "Large Population", "population_size": 100, "generations": 200},
        {"label": "High Mutation", "population_size": 50, "generations": 100, "mutation_rate": 0.5},
    ]

    for config_params in configs:
        label = config_params.pop("label")
        print(f"\nTesting: {label}")
        print(f"Parameters: {config_params}")

        config.set_algorithm_config("genetic", **config_params)
        result = quick_test("genetic", grid_size=15)


if __name__ == "__main__":
    # Example 1: Test A*
    quick_test("astar", grid_size=20)

    # Example 2: Test Genetic Algorithm
    quick_test("genetic", grid_size=20)

    # Example 3: Compare all algorithms
    compare_all_algorithms(grid_size=20)

    # Example 4: Custom parameters
    test_with_custom_parameters()
