import time
import networkx as nx
import random


def comparisonRun(city, start, goal, algoFunc, algoName):

    staticStartTime = time.time()
    staticPath, _ = algoFunc(city.graph, start, goal)
    staticEndtime = time.time()
    staticCost = nx.path_weight(city.graph, staticPath, weight="weight")

    middleNode = staticPath[len(staticPath) // 2]
    affectedEdges = city.applyTrafficScenario(
        centerNode=middleNode,
        radius=random.choice([3, 5, 8]),
        intensity=random.choice([15, 20, 30, 40]),
    )
    costStaticAfterAffect = nx.path_weight(city.graph, staticPath, weight="weight")

    dynamicStartTime = time.time()
    reroutedPath, _ = algoFunc(city.graph, start, goal)
    dynamicEndTime = time.time()
    reroutedCost = nx.path_weight(city.graph, reroutedPath, weight="weight")

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
