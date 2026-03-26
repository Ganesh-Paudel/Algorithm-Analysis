from maps import LoadMap,GenerateMap
from visualize import VisualizeGraph
from Nodes import ExtractNodeAndEdges


def main():
    data = ExtractNodeAndEdges("data/graph.graphml")
    data.saveToCSV()

if __name__ == "__main__":
    main()
