import networkx as nx
import matplotlib.pyplot as plt
import osmnx as os



class Graph:
    
    def __init__(self) -> None:
        self.G = nx.Graph()
        self.G_os = os.graph.graph_from_place("Huntington, West Virginia, USA", network_type="drive")

        


    def drawGraph(self, list):
        self.G.add_nodes_from(list)
        self.G.add_edges_from([(list[0], list[1]), (list[2], list[3])])
        nx.draw(self.G, with_labels=True)
        plt.show()
    def drawOs(self):
        fig,ax = os.plot.plot_graph(self.G_os)



def main():
    graph = Graph()
    nodes = ['1', '2', '3', '4']
    graph.drawOs()


if __name__ == "__main__":
    main()
