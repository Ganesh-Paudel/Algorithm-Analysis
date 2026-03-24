import osmnx as ox 

class GenerateMap:

    @staticmethod
    def fetchMapAndSave(placeName, outFileName = "map.graphml"):
        print(f"Fetching Map")
        graph = ox.graph.graph_from_place(placeName, network_type="drive")
        ox.save_graphml(graph, outFileName)
        print(f"Map Fetch Successful!!")
        return graph

class LoadMap:

    def __init__(self, filePath) -> None:
        self.filePath = filePath
        self.graph = ox.load_graphml(filePath)

    def getGraph(self):
        return self.graph

     


