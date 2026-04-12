import pandas as pd
import os


def recordPerformance(size, result):

    improvement = (
        (result["Stuck_In_Traffic_Cost"] - result["ReroutedCost"])
        / result["Stuck_In_Traffic_Cost"]
        * 100
    )

    data = {
        "Algorithm": [result["algo"]],
        "Size": [size],
        "RerouteRuntimeSec": [result["dynamicRunTime"]],
        "Efficiency_Gain": [round(improvement, 2)],
        "StaticCost": [result["Stuck_In_Traffic_Cost"]],
        "ReroutedCost": [result["ReroutedCost"]],
    }

    df = pd.DataFrame(data)
    outputPath = "./output/performanceResults.csv"
    df.to_csv(outputPath, mode="a", header=not os.path.exists(outputPath), index=False)
