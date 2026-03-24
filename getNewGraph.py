import osmnx as os

class GetNewGraph:

    def __init__(self, CityName):
        self.graph = os.graph.graph_from_place(CityName, network_type="drive")

    def visualizeGraph(self):
        fig,ax = os.plot.plot_graph(self.graph)

    def saveGraph(self, name = None):
        if name != None:
            os.save_graphml(self.graph,name)
        else:
            os.save_graphml(self.graph)



