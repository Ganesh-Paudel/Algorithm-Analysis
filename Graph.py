import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue
import math
import time

class Graph:
    def __init__(self, nodes_csv, edges_csv):
        self.nodes_df = pd.read_csv(nodes_csv, dtype = {'node_id':str})
        self.edges_df = pd.read_csv(edges_csv ,dtype = {'source' : str, 'target': str})
        
        self.node_coords = {
            str(row['node_id']): (row['x'], row['y']) 
            for _, row in self.nodes_df.iterrows()
        }
        
        self.adj = {}
        for _, row in self.edges_df.iterrows():
            u, v, w = str(row['source']), str(row['target']), float(row['weight'])
            if u not in self.adj: self.adj[u] = []
            self.adj[u].append((v, w))
            
            if str(row['oneway']).lower() == 'false':
                if v not in self.adj: self.adj[v] = []
                self.adj[v].append((u, w))

    def get_heuristic(self, u, v):
        x1, y1 = self.node_coords[u]
        x2, y2 = self.node_coords[v]
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
