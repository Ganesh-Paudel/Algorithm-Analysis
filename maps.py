import osmnx as ox 

class GenerateMap:

    @staticmethod
    def fetchMapAndSave(placeName, outFileName = "map.graphml"):
        print(f"Fetching Map")
        graph = ox.graph.graph_from_place(placeName, network_type="drive")
        ox.save_graphml(graph, outFileName)
        print(f"Map Fetch Successful!!")
        return graph
    

    @staticmethod
    def saveToCSV(graphMlFile, outFileName = "graph"):
        print(f"Transforming graphml to normal CSV")

        G = ox.load_graphml(graphMlFile)
        nodes,edges = ox.graph_to_gdfs(G)
        edge_list = edges[['u','v','length']].copy()
        edge_list.columns = ['node_x', 'node_y', 'weight']
        outputFile = outFileName + ".csv"
        edge_list.to_csv(outFileName, index = False)

        print(f"Successful")

class LoadMap:

    def __init__(self, filePath) -> None:
        self.filePath = filePath
        self.graph = ox.load_graphml(filePath)

    def getGraph(self):
        return self.graph

     


