import networkx as nx 
import random

class CityGraph:

    def __init__(self, girdSize = 50):
        self.gridSize = gridSize
        self.graph = nx.grid_2d_graph(self.gridSize, self.gridSize);
