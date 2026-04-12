import networkx as nx
from numpy.random import weibull
from solve import Solve
from trafficEnvironment import CityGraph
from performance import recordPerformance
import pandas as pd
from visualize import saveComparisonPlot, savePathPlot, generateSummaryPlots
from runner import comparisonRun


def run():
    experimentData = pd.read_csv("./inputTestData.csv")

    for index, row in experimentData.iterrows():
        size = int(row["size"])
        start = (int(row["startX"]), int(row["startY"]))
        target = (int(row["goalX"]), int(row["goalY"]))

        print(f"Running run no: {index + 1} : Size {size}*{size}")

        city = CityGraph(size=size)

        resAstar = comparisonRun(city, start, target, Solve.aStar, "A_Star")
        recordPerformance(size, resAstar)
        saveComparisonPlot(
            city.graph,
            resAstar["Paths"][0],
            resAstar["Paths"][1],
            resAstar["affectedEdges"],
            f"A* Reroute (Size {size})",
        )

    generateSummaryPlots("AStar_Time_Performance")


if __name__ == "__main__":
    run()
