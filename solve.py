import networkx as nx
import random


class Solve:
    @staticmethod
    def aStar(graph, start, goal):
        visited = []
        path = nx.astar_path(graph, start, goal, weight="weight")
        return path, visited

    @staticmethod
    def geneticAlgorithm(graph, start, goal, generations=50, pop_size=20):
        population = []
        for _ in range(pop_size):
            path = [start]
            population.append(path)
        # bestPath = nx.shortest_path(graph, start, goal, weight="weight")
        # return bestPath, population
