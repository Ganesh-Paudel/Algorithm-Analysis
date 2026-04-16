"""
A* Pathfinding Algorithm implementation.
Inherits from PathfindingAlgorithm base class.
"""

import heapq
from typing import Tuple, Set, Optional, Any, TYPE_CHECKING
from .base import PathfindingAlgorithm

if TYPE_CHECKING:
    from src.utils.animation_data import AnimationDataCollector, AnimationNode


class AStarPathfinder(PathfindingAlgorithm):
    """A* algorithm for pathfinding on weighted graphs."""

    def __init__(self):
        """Initialize A* pathfinder."""
        self.name = "A*"

    def find_path(
        self, graph: Any, start: Tuple[int, int], goal: Tuple[int, int],
        animation_collector: Optional["AnimationDataCollector"] = None
    ) -> Tuple[Optional[list], float, Set]:
        """
        Find shortest path using A* algorithm.

        Args:
            graph: NetworkX graph representing the environment
            start: Starting node tuple (x, y)
            goal: Goal node tuple (x, y)
            animation_collector: Optional animation data collector

        Returns:
            Tuple of (path, cost, visited_nodes)
        """

        def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
            """Manhattan distance heuristic."""
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}  # actual cost from start
        f_score = {start: heuristic(start, goal)}
        visited = set()
        step_counter = 0

        while open_set:
            _, current = heapq.heappop(open_set)

            if current in visited:
                continue

            visited.add(current)

            # Collect animation data
            if animation_collector:
                from src.utils.animation_data import AnimationNode
                explored_node = AnimationNode(
                    step=step_counter,
                    node=current,
                    status="visited",
                    metadata={
                        "g_score": float(g_score[current]),
                        "f_score": float(f_score[current]),
                        "heuristic": float(heuristic(current, goal))
                    }
                )
                animation_collector.add_step(
                    nodes_explored=[explored_node],
                    current_node=current,
                    open_set=[n for _, n in open_set],
                    closed_set=list(visited)
                )
                step_counter += 1

            if current == goal:
                # Reconstruct path
                path = []
                total_cost = g_score[current]
                node = current

                while node in came_from:
                    path.append(node)
                    node = came_from[node]

                path.append(start)
                return path[::-1], total_cost, visited

            for neighbor in graph.neighbors(current):
                if neighbor in visited:
                    continue

                weight = graph[current][neighbor].get("weight", 1)
                tentative_g = g_score[current] + weight

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    f_score[neighbor] = f
                    heapq.heappush(open_set, (f, neighbor))

        # Goal not found
        return None, float("inf"), visited
