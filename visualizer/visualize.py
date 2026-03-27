import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class GraphVisualizer:
    def __init__(self, graph):
        self.graph = graph
        self.nx_graph = nx.DiGraph()
        for _, row in graph.edges_df.iterrows():
            self.nx_graph.add_edge(str(row['source']), str(row['target']), weight=row['weight'])
        
        self.pos = {node: (coords[0], coords[1]) for node, coords in graph.node_coords.items()}

    def animate_search(self, visited_nodes, final_path, start_node, target_node):
        plt.ion() # Turn on interactive mode
        fig, ax = plt.subplots(figsize=(12, 9))
        
        nx.draw_networkx_edges(self.nx_graph, self.pos, alpha=0.1, edge_color='gray', ax=ax)
        nx.draw_networkx_nodes(self.nx_graph, self.pos, node_size=5, node_color='lightgray', alpha=0.3, ax=ax)

        nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=[str(start_node)], 
                               node_color='blue', node_size=100, label='Source', ax=ax)
        nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=[str(target_node)], 
                               node_color='magenta', node_size=100, label='Target', ax=ax)
        
        ax.legend(scatterpoints=1, loc = 'upper left', bbox_to_anchor=(1,1))
        
        batch_size = 100 
        for i in range(0, len(visited_nodes), batch_size):
            batch = visited_nodes[i : i + batch_size]
            nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=batch, 
                                   node_color='orange', node_size=15, ax=ax)
            
            plt.title(f"Searching... Nodes Visited: {i + len(batch)}")
            plt.pause(0.001) 
        if final_path and len(final_path) > 1:
            edges = list(zip(final_path, final_path[1:]))
            nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=final_path, 
                                   node_color='green', node_size=40, ax=ax)
            nx.draw_networkx_edges(self.nx_graph, self.pos, edgelist=edges, 
                                   edge_color='red', width=3, ax=ax)
        
        plt.title("Pathfinding Complete!")
        plt.ioff() 
        plt.show(block=True) 
