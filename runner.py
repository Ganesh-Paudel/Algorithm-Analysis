import time
import networkx as nx
import random


def comparisonRun(city, start, goal, algoFunc, algoName):

    staticStartTime = time.time()
    staticPath, staticCost, _ = algoFunc.runAlgo(city.graph, start, goal)
    print(f"Static path: {staticPath} with cost {staticCost}")
    staticEndtime = time.time()
    # staticCost = nx.path_weight(city.graph, staticPath, weight="weight")

    middleNode = staticPath[len(staticPath) // 2]
    affectedEdges = city.applyTrafficScenario(
        centerNode=middleNode,
        radius=random.choice([3, 5, 8]),
        intensity=random.choice([15, 20, 30, 40]),
    )
    costStaticAfterAffect = algoFunc.calculatePathCost(
        city.graph, start, weight="weight"
    )
    print(f"Cost after traffic change: {costStaticAfterAffect}")

    dynamicStartTime = time.time()
    reroutedPath, reroutedCost, _ = algoFunc.runAlgo(city.graph, start, goal)
    dynamicEndTime = time.time()
    print(f"Static path: {reroutedPath} with cost {reroutedCost}")
    # reroutedCost = nx.path_weight(city.graph, reroutedPath, weight="weight")

    return {
        "algo": algoName,
        "staticruntime": staticEndtime - staticStartTime,
        "dynamicRunTime": dynamicEndTime - dynamicStartTime,
        "staticCost": staticCost,
        "Stuck_In_Traffic_Cost": costStaticAfterAffect,
        "ReroutedCost": reroutedCost,
        "Paths": (staticPath, reroutedPath),
        "affectedEdges": affectedEdges,
    }
