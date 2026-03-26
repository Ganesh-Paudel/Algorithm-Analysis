from Graph import Graph
from visualize import GraphVisualizer
from aStar import AStar

def main():
    graph = Graph('data/nodes.csv', 'data/edges.csv')
    solve = AStar(graph);
    source = '154751519'
    target = '13167613297'
    path = solve.solve(source, target)
    visual = GraphVisualizer(graph)
    # visual.animate_search(solve.visited_nodes, path, source, target)
    solve.print_performance();
    



if __name__ == "__main__":
    main()
