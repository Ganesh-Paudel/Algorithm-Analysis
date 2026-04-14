import pandas as pd
import os


def recordPerformance(size, result):
    """Record performance metrics to results/performanceResults.csv."""
    if isinstance(result, dict):
        algo_name = result.get("algo") or result.get("Algorithm")
        static_traffic_cost = result.get("cost_after_traffic") or result.get(
            "Stuck_In_Traffic_Cost"
        )
        rerouted_cost = result.get("rerouted_cost") or result.get("ReroutedCost")
        dynamic_runtime = result.get("dynamic_runtime") or result.get("dynamicRunTime")
    else:
        algo_name = getattr(result, "algorithm", None) or getattr(result, "algo", None)
        static_traffic_cost = getattr(result, "cost_after_traffic", None) or getattr(
            result, "Stuck_In_Traffic_Cost", None
        )
        rerouted_cost = getattr(result, "rerouted_cost", None) or getattr(
            result, "ReroutedCost", None
        )
        dynamic_runtime = getattr(result, "dynamic_runtime", None) or getattr(
            result, "dynamicRunTime", None
        )

    if static_traffic_cost is None:
        static_traffic_cost = float("inf")

    if rerouted_cost is None:
        rerouted_cost = float("inf")

    if dynamic_runtime is None:
        dynamic_runtime = 0.0

    static_runtime = getattr(result, "static_runtime", None) if not isinstance(result, dict) else result.get("static_runtime") or result.get("staticRunTime")
    dynamic_runtime = dynamic_runtime if dynamic_runtime is not None else 0.0
    success = getattr(result, "success", None) if not isinstance(result, dict) else result.get("success")
    improvement_value = getattr(result, "improvement", None) if not isinstance(result, dict) else result.get("improvement")
    improvement_percent = getattr(result, "improvement_percent", None) if not isinstance(result, dict) else result.get("improvement_percent")
    nodes_explored = getattr(result, "nodes_explored", None) if not isinstance(result, dict) else result.get("nodes_explored")
    cost_after_traffic = static_traffic_cost

    if static_runtime is None:
        static_runtime = 0.0
    if success is None:
        success = bool(rerouted_cost != float("inf"))
    if improvement_value is None and static_traffic_cost != float("inf"):
        improvement_value = static_traffic_cost - rerouted_cost
    if improvement_percent is None:
        improvement_percent = (
            (improvement_value / static_traffic_cost * 100)
            if static_traffic_cost > 0 and improvement_value is not None
            else 0
        )
    if nodes_explored is None:
        nodes_explored = 0

    if static_traffic_cost == float("inf"):
        static_traffic_cost = 100000000

    data = {
        "Algorithm": [algo_name],
        "Size": [size],
        "Success": [success],
        "StaticRuntimeSec": [static_runtime],
        "DynamicRuntimeSec": [dynamic_runtime],
        "StaticCost": [static_traffic_cost],
        "CostAfterTraffic": [cost_after_traffic],
        "ReroutedCost": [rerouted_cost],
        "Improvement": [improvement_value],
        "ImprovementPercent": [round(improvement_percent, 2) if improvement_percent is not None else 0],
        "NodesExplored": [nodes_explored],
    }

    df = pd.DataFrame(data)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    output_dir = os.path.join(root_dir, "results")
    os.makedirs(output_dir, exist_ok=True)
    outputPath = os.path.join(output_dir, "performanceResults.csv")
    df.to_csv(outputPath, mode="a", header=not os.path.exists(outputPath), index=False)
