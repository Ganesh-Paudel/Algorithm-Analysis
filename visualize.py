import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def savePathPlot(graph, path, title, fileName):
    fig, ax = plt.subplots(figsize=(15, 15), dpi=100)
    pos = {node: node for node in graph.nodes()}

    nx.draw_networkx_nodes(graph, pos, node_size=5, node_color="gray", alpha=0.1, ax=ax)
    nx.draw_networkx_edges(graph, pos, width=0.2, edge_color="gray", alpha=0.1, ax=ax)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(
            graph, pos, nodelist=path, node_size=15, node_color="blue", ax=ax
        )
        nx.draw_networkx_edges(
            graph, pos, edgelist=path_edges, edge_color="blue", width=2, ax=ax
        )

    plt.title(title)
    plt.savefig(f"./output/{fileName}.png")
    plt.close()


def saveComparisonPlot(graph, staticPath, reroutedPath, affectedEdges, fileName):
    fig, ax = plt.subplots(figsize=(12, 12), dpi=100)
    pos = {n: n for n in graph.nodes()}

    # nx.draw_networkx_nodes(graph, pos, node_size=5, node_color="gray", alpha=0.5, ax=ax)
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=affectedEdges,
        edge_color="red",
        width=2,
        alpha=0.5,
        label="Traffic High",
    )

    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=list(zip(staticPath, staticPath[1:])),
        edge_color="blue",
        width=3,
        style="dashed",
        label="Original path",
    )

    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=list(zip(reroutedPath, reroutedPath[1:])),
        edge_color="green",
        width=4,
        label="Reroutedpath",
        alpha=1,
    )
    plt.legend()
    plt.savefig(f"./output/{fileName}.png", bbox_inches="tight")
    plt.close()


def generateSummaryPlots(fileName):
    import pandas as pd

    df = pd.read_csv("./output/performanceResults.csv")

    plt.figure(figsize=(10, 6))
    plt.scatter(df["Size"], df["Efficiency_Gain"], color="green")
    plt.title("Algorithm Effectiveness in Dynamic Traffic")
    plt.xlabel("Grid Size")
    plt.ylabel("Percent Cost Saved by Rerouting")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(f"./output/{fileName}_efficiency.png")
    plt.close()

    indices = np.arange(len(df))
    width = 0.35

    plt.figure(figsize=(12, 6), dpi=100)
    plt.bar(
        indices - width / 2,
        df["StaticCost"],
        width,
        label="Original (Clear) Cost",
        color="#2ecc71",
    )
    plt.bar(
        indices + width / 2,
        df["ReroutedCost"],
        width,
        label="Rerouted (Congested) Cost",
        color="#f1c40f",
    )

    plt.xlabel("Experiment (Grid Size)")
    plt.ylabel("Total Path Cost")
    plt.title("Path Quality: Original Baseline vs. Rerouted Path Cost")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"./output/{fileName}_cost_comparison.png")
    plt.close()
