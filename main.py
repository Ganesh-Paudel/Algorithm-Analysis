from maps import LoadMap
from visualize import VisualizeGraph

def main():
    graph = LoadMap("data/graph.graphml").getGraph()
    VisualizeGraph(graph).plot_map()

if __name__ == "__main__":
    main()
