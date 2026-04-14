import networkx as nx
import random
from aStar import AStar


class Solve:
    @staticmethod
    def aStar(graph, start, goal):
        # path = nx.astar_path(graph, start, goal, weight="weight")
        return AStar(graph, start, goal)

    @staticmethod
    def geneticAlgorithm(graph, start, goal, generations=50, pop_size=20):
        population = []
        for _ in range(pop_size):
            path = [start]
            population.append(path)
        # bestPath = nx.shortest_path(graph, start, goal, weight="weight")
        # return bestPath, population
