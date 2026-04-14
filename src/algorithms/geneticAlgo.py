"""
Genetic Algorithm implementation for pathfinding.
Inherits from PathfindingAlgorithm base class.
"""

import random
from typing import Tuple, Set, Optional, Any, List
from .base import PathfindingAlgorithm


class GeneticPathfinder(PathfindingAlgorithm):
    """Genetic algorithm for pathfinding on weighted graphs."""

    def __init__(
        self,
        population_size: int = 20,  # Reduced from 50
        generations: int = 30,  # Reduced from 100
        mutation_rate: float = 0.15,  # Reduced from 0.2
        elite_ratio: float = 0.3,  # Increased from 0.2
    ):
        """
        Initialize Genetic Algorithm pathfinder.

        Args:
            population_size: Number of paths in each generation
            generations: Number of generations to evolve
            mutation_rate: Probability of mutation (0.0 to 1.0)
            elite_ratio: Ratio of best paths to preserve
        """
        self.name = "Genetic Algorithm"
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_ratio = elite_ratio
        self.elite_count = max(1, int(population_size * elite_ratio))

    def find_path(
        self, graph: Any, start: Tuple[int, int], goal: Tuple[int, int]
    ) -> Tuple[Optional[list], float, Set]:
        """
        Find path using genetic algorithm.

        Args:
            graph: NetworkX graph representing the environment
            start: Starting node tuple (x, y)
            goal: Goal node tuple (x, y)

        Returns:
            Tuple of (path, cost, visited_nodes)
        """

        def generate_random_path() -> Optional[List]:
            """Generate a random valid path from start to goal using simplified approach."""
            path = [start]
            current = start
            visited = set([start])
            max_steps = min(200, len(graph.nodes()) // 2)  # Limit path length

            for _ in range(max_steps):
                if current == goal:
                    return path

                # Get unvisited neighbors
                neighbors = [n for n in graph.neighbors(current) if n not in visited]

                if not neighbors:
                    # Backtrack if stuck
                    if len(path) > 1:
                        visited.remove(current)
                        path.pop()
                        current = path[-1]
                        continue
                    else:
                        return None

                # Simple heuristic: prefer nodes closer to goal
                if random.random() < 0.8:  # 80% use heuristic
                    next_node = min(
                        neighbors,
                        key=lambda n: abs(n[0] - goal[0]) + abs(n[1] - goal[1]),
                    )
                else:  # 20% random exploration
                    next_node = random.choice(neighbors)

                path.append(next_node)
                visited.add(next_node)
                current = next_node

            return path if current == goal else None

        def crossover(parent1: List, parent2: List) -> List:
            """
            Simple crossover: take prefix from one parent, suffix from other.
            """
            if not parent1 or not parent2:
                return parent1.copy() if parent1 else parent2.copy()

            # Find common nodes
            common = set(parent1) & set(parent2)
            if not common or goal not in common:
                # No common path to goal, return shorter parent
                return (
                    parent1.copy() if len(parent1) <= len(parent2) else parent2.copy()
                )

            # Choose crossover point
            cross_points = [node for node in common if node != start and node != goal]
            if not cross_points:
                return parent1.copy()

            cross_node = random.choice(cross_points)

            # Create child
            idx1 = parent1.index(cross_node)
            idx2 = parent2.index(cross_node)

            child = parent1[: idx1 + 1] + parent2[idx2 + 1 :]

            # Validate child
            if self.validate_path(graph, child):
                return child

            # If invalid, return better parent
            return parent1.copy() if len(parent1) <= len(parent2) else parent2.copy()

        def mutate(path: List) -> List:
            """
            Simple mutation: randomly replace one intermediate node with a neighbor.
            """
            if random.random() > self.mutation_rate or len(path) < 3:
                return path.copy()

            # Choose random intermediate node
            idx = random.randint(1, len(path) - 2)
            current_node = path[idx]

            # Get neighbors
            neighbors = list(graph.neighbors(current_node))
            if not neighbors:
                return path.copy()

            # Replace with random neighbor
            new_node = random.choice(neighbors)

            # Avoid creating cycles
            if new_node in path:
                return path.copy()

            new_path = path.copy()
            new_path[idx] = new_node

            # Validate the mutated path
            return new_path if self.validate_path(graph, new_path) else path.copy()

        # Initialize population with valid paths
        population = []
        max_init_attempts = self.population_size * 3  # Reduced attempts

        attempts = 0
        while len(population) < self.population_size and attempts < max_init_attempts:
            candidate = generate_random_path()
            if candidate and self.validate_path(graph, candidate):
                population.append(candidate)
            attempts += 1

        if not population:
            return None, float("inf"), set()

        visited_all = set()
        cost_cache = {}  # Cache path costs

        def get_cost(path):
            """Get cached cost or calculate and cache it."""
            path_tuple = tuple(path)
            if path_tuple not in cost_cache:
                cost_cache[path_tuple] = self.calculate_path_cost(graph, path)
            return cost_cache[path_tuple]

        # Evolution loop
        best_path = None
        best_cost = float("inf")
        stagnation_count = 0
        max_stagnation = 5  # Reduced stagnation limit

        for generation in range(self.generations):
            # Calculate fitness for population
            population_with_costs = [(get_cost(p), p) for p in population]
            population_with_costs.sort(key=lambda x: x[0])  # Sort by cost

            # Update best solution
            current_best_cost, current_best_path = population_with_costs[0]
            if current_best_cost < best_cost:
                best_cost = current_best_cost
                best_path = current_best_path.copy()
                stagnation_count = 0
            else:
                stagnation_count += 1

            # Early termination
            if stagnation_count >= max_stagnation:
                break

            # Track visited nodes
            for _, path in population_with_costs:
                visited_all.update(path)

            # Selection: keep elite
            elite = [path for _, path in population_with_costs[: self.elite_count]]

            # Create new generation
            new_population = elite.copy()

            # Generate offspring
            while len(new_population) < self.population_size:
                # Simple random selection from elite
                parent1 = random.choice(elite)
                parent2 = random.choice(elite)

                # Crossover and mutate
                child = crossover(parent1, parent2)
                child = mutate(child)

                if child and self.validate_path(graph, child):
                    new_population.append(child)

            population = new_population[: self.population_size]

        return best_path, best_cost, visited_all
