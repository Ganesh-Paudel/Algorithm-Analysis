"""
Main entry point for Algorithm Analysis.
Modular architecture for comparing pathfinding algorithms.
Easy to switch algorithms and configure parameters.
"""

import pandas as pd
from src.environments.traffic import CityGraph
from src.utils.algorithm_factory import AlgorithmFactory
from src.utils.performance import recordPerformance
from config.config import get_config
from analysis.comparison import (
    run_algorithm_test,
    visualize_path_comparison,
    visualize_comparison_charts,
)
from analysis.results_aggregator import ExperimentRound, ResultsAggregator


def run_experiments():
    """Run comparison experiments with configured algorithms."""

    # Get configuration
    config = get_config()

    # Set which algorithms to test
    config.set_active_algorithms("astar", "genetic")

    # Optionally customize algorithm parameters
    config.set_algorithm_config("genetic", population_size=50, generations=100)

    print("\n" + "=" * 80)
    print("Algorithm Analysis - Modular Comparison")
    print("=" * 80)
    print(config.get_summary())
    print("=" * 80)

    # Load test configuration
    experiment_data = pd.read_csv("./data/inputTestData.csv")

    # Initialize results aggregator
    results_aggregator = ResultsAggregator()

    for index, row in experiment_data.iterrows():
        size = int(row["size"])
        start = (int(row["startX"]), int(row["startY"]))
        goal = (int(row["goalX"]), int(row["goalY"]))

        print(f"\n[Experiment {index + 1}] Grid Size: {size}x{size}")
        print(f"Start: {start}, Goal: {goal}\n")

        # Create city
        city = CityGraph(size=size)

        # Create experiment round
        round_result = ExperimentRound(
            round_number=index + 1,
            grid_size=size,
            start=start,
            goal=goal,
        )

        # Test each active algorithm
        for algo_name in config.get_active_algorithms():
            print(f"\nTesting: {algo_name}")
            print("-" * 40)

            # Create algorithm with configured parameters
            algo_kwargs = config.get_algorithm_kwargs(algo_name)
            algorithm = AlgorithmFactory.create(algo_name, **algo_kwargs)

            # Run test
            result = run_algorithm_test(city, start, goal, algorithm)

            if result.success:
                print(f"Static path cost: {result.static_cost:.2f}")
                print(f"Cost after traffic: {result.cost_after_traffic:.2f}")
                print(f"Rerouted path cost: {result.rerouted_cost:.2f}")
                print(f"Improvement: {result.improvement_percent:.1f}%")
                print(f"Nodes explored: {result.nodes_explored}")
                print(f"Static runtime: {result.static_runtime:.4f}s")
                print(f"Dynamic runtime: {result.dynamic_runtime:.4f}s")
            else:
                print(f"Failed: {result.error}")

            # Add result to round
            round_result.add_result(result)

            # Save performance results
            recordPerformance(size, result)

            # Visualize paths if successful
            if result.success:
                visualize_path_comparison(
                    city.graph,
                    result.static_path,
                    result.rerouted_path,
                    result.affected_edges,
                    f"{algo_name.lower()}_{size}x{size}",
                    title=f"{algorithm.name} - Size {size}x{size}",
                )

            # Reset traffic for next algorithm
            city.reset_traffic()

        # Add round to results
        results_aggregator.add_round(round_result)

        print("\n" + "=" * 80)

        # Uncomment to process only first experiment
        # break

    # Generate summary and charts
    results_aggregator.print_summary()
    visualize_comparison_charts(results_aggregator)

    print("\nAnalysis complete!")


if __name__ == "__main__":
    run_experiments()
