"""
Traffic Environment: Simulates a city graph with dynamic traffic conditions.
"""

import networkx as nx
import random
from typing import Tuple, List, Set


class CityGraph:
    """Represents a city as a grid graph with weighted edges and dynamic traffic."""

    def __init__(self, size: int = 50, seed: int = None):
        """
        Initialize CityGraph.

        Args:
            size: Size of the grid (size x size)
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)

        self.size = size  # Expose size for unified_comparison
        self.grid_size = size  # Keep for backwards compatibility
        self.graph = nx.grid_2d_graph(size, size)

        # Initialize edge weights with distance, speed limit, and traffic
        for u, v in self.graph.edges():
            distance = random.choice([1, 5, 10])
            speed_limit = random.choice([20, 40, 80])
            self.graph[u][v]["distance"] = distance
            self.graph[u][v]["speed_limit"] = speed_limit
            self.graph[u][v]["traffic_index"] = 1.0
            self.update_edge_weight(u, v)

    def update_edge_weight(self, u: Tuple[int, int], v: Tuple[int, int]) -> None:
        """
        Update the total weight of an edge based on distance, speed, and traffic.

        Weight = (distance / speed_limit) * traffic_index

        Args:
            u: First node
            v: Second node
        """
        if not self.graph.has_edge(u, v):
            return

        edge = self.graph[u][v]
        edge["weight"] = (
            edge["distance"] / edge["speed_limit"]
        ) * edge["traffic_index"]

    def apply_traffic_scenario(
        self,
        center_node: Tuple[int, int],
        radius: int = 5,
        intensity: float = 20.0,
    ) -> List[Tuple]:
        """
        Apply a traffic event (congestion) centered at a node.

        Affects all edges in an ego graph around the center node.

        Args:
            center_node: Center of traffic event
            radius: Radius of affected area
            intensity: Traffic intensity multiplier (1.0 = normal)

        Returns:
            List of affected edges
        """
        # Get all nodes within radius
        affected_subgraph = nx.ego_graph(self.graph, center_node, radius=radius)
        affected_nodes = affected_subgraph.nodes()

        # Apply traffic to edges in the affected area
        affected_edges = []
        for u, v in self.graph.edges():
            if u in affected_nodes or v in affected_nodes:
                self.graph[u][v]["traffic_index"] = intensity
                self.update_edge_weight(u, v)
                affected_edges.append((u, v))

        return affected_edges

    def reset_traffic(self, edges: List[Tuple] = None) -> None:
        """
        Reset traffic conditions.

        Args:
            edges: Specific edges to reset. If None, reset all.
        """
        edges_to_reset = edges if edges is not None else self.graph.edges()

        for u, v in edges_to_reset:
            if self.graph.has_edge(u, v):
                self.graph[u][v]["traffic_index"] = 1.0
                self.update_edge_weight(u, v)

    def get_stats(self) -> dict:
        """Get statistics about the graph."""
        return {
            "grid_size": self.grid_size,
            "num_nodes": len(self.graph.nodes()),
            "num_edges": len(self.graph.edges()),
            "avg_degree": sum(dict(self.graph.degree()).values()) / len(self.graph),
        }
