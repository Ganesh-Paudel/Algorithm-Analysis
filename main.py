from Graph.graph import Graph
from visualizer.visualize import GraphVisualizer
from algorithms.aStar import AStar
import pandas as pd

def main():
    graph = Graph('data/nodes.csv', 'data/edges.csv')
    test = getTestData();
    for source,target in zip(test[0],test[1]):
        solve = AStar(graph);
        path = solve.solve(source, target)
    # visual = GraphVisualizer(graph)
    # visual.animate_search(solve.visited_nodes, path, source, target)
        solve.print_performance();
        solve.save_performance("performance.csv");

def getTestData():
    data = pd.read_csv("data/testCases.csv", names = ['source', 'target'], dtype = {'source':str, 'target':str})
    source = data['source'].tolist();
    target = data['target'].tolist();
    return [source,target]


if __name__ == "__main__":
    main()
