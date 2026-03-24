import osmnx as ox
import matplotlib.pyplot as plt

class VisualizeGraph:

    def __init__(self, graph) -> None:
        self.graph = graph


    def plot_map(self):
        fig,ax = ox.plot_graph(
            self.graph,
            figsize=(19,19),
            node_size=30,
            edge_color='#444444',
            show=False,
            close = False
        )

        plt.subplots_adjust(left = 0, right=1, top=1, bottom=0.6, hspace=0,wspace=0)
        plt.show()
        
