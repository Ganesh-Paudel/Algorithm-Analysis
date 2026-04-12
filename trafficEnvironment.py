import networkx as nx
import random


class CityGraph:
    def __init__(self, size=50):

        self.gridSize = size
        self.graph = nx.grid_2d_graph(self.gridSize, self.gridSize)

        for u, v in self.graph.edges():
            distance = random.choice([1, 5, 10])
            speedLimit = random.choice([20, 40, 80])

            self.graph[u][v]["distance"] = distance
            self.graph[u][v]["speedLimit"] = speedLimit
            self.graph[u][v]["trafficIndex"] = 1.0

            self.updateEdgeWeight(u, v)

    def updateEdgeWeight(self, u, v):
        edge = self.graph[u][v]
        edge["weight"] = (edge["distance"] / edge["speedLimit"]) * edge["trafficIndex"]

    def applyTrafficScenario(self, centerNode, radius=5, intensity=20):

        affectedNodes = nx.ego_graph(self.graph, centerNode, radius=radius).nodes()
        subgraph = self.graph.subgraph(affectedNodes)

        for u, v in subgraph.edges():
            self.graph[u][v]["trafficIndex"] = intensity
            self.updateEdgeWeight(u, v)
        return list(subgraph.edges())
