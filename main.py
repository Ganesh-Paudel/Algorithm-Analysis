import networkx as nx
import matplotlib.pyplot as plt
import osmnx as os
from getNewGraph import GetNewGraph

class LoadGraph:
    
    def __init__(self, path) -> None:
        self.graph = os.load_graphml(path)

    def visualizeGraph(self):
        os.plot_graph(self.graph)
        

def main():
    graph = LoadGraph("data/graph.graphml")
    graph.visualizeGraph()



if __name__ == "__main__":
    main()
