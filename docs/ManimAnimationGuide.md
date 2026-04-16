# Manim Animation Data Integration Guide

## Overview

This guide explains how to capture algorithm execution data for Manim animation generation without re-running algorithms.

## Key Principles

1. **Capture during execution** — Modified algorithms collect data while running
2. **Save as JSON** — Serialized data can be regenerated independently
3. **Replay for animation** — Manim reads JSON and creates animations
4. **Separation of concerns** — Algorithm logic stays unchanged; data collection is separate

## Integration Steps

### Step 1: Modify Algorithm Base Class

Update `src/algorithms/base.py` to accept an optional collector:

```python
@abstractmethod
def find_path(
    self, graph: Any, start: Tuple[int, int], goal: Tuple[int, int],
    animation_collector: Optional[AnimationDataCollector] = None
) -> Tuple[Optional[list], float, Set]:
    """Find path, optionally collecting animation data"""
    pass
```

### Step 2: Update A* Algorithm

In `src/algorithms/aStar.py`, capture exploration order:

```python
def find_path(self, graph, start, goal, animation_collector=None):
    # ... existing A* code ...
    
    if animation_collector:
        explored_nodes = []
        at_step = 0
        
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        # Collect animation data
        if animation_collector:
            explored_nodes.append(AnimationNode(
                step=at_step,
                node=current,
                status="visited",
                metadata={
                    "g_score": g_score[current],
                    "f_score": f_score[current],
                    "heuristic": heuristic(current, goal)
                }
            ))
            at_step += 1
            
            animation_collector.add_step(
                nodes_explored=[explored_nodes[-1]],
                current_node=current,
                open_set=list(dict.fromkeys([n for _, n in open_set])),
                closed_set=list(visited)
            )
```

### Step 3: Update Genetic Algorithm

For genetic algorithm, capture generation data:

```python
def find_path(self, graph, start, goal, animation_collector=None):
    # ... initialization ...
    
    if animation_collector:
        animation_collector.add_step(
            nodes_explored=[AnimationNode(
                step=0,
                node=start,
                status="initial_population",
                metadata={"population_size": len(population)}
            )],
            metadata={
                "generation": 0,
                "population_size": len(population),
                "best_fitness": sorted([f for _, f in population])[0]
            }
        )
    
    for generation in range(self.generations):
        # ... GA logic ...
        
        if animation_collector:
            animation_collector.add_step(
                nodes_explored=[AnimationNode(
                    step=generation,
                    node=best_path[0],  # First node of best path
                    status="generation",
                    metadata={
                        "generation": generation,
                        "best_path_length": len(best_path),
                        "best_fitness": best_fitness,
                        "avg_fitness": sum(f for _, f in population) / len(population)
                    }
                )],
                metadata={
                    "generation": generation,
                    "best_fitness": best_fitness
                }
            )
```

### Step 4: Update Runner/Caller Code

Modify `analysis/runner.py`:

```python
from src.utils.animation_data import AnimationDataCollector
import json
import os

def comparison_run_with_animation(city, start, goal, algo_func, algo_name, save_animation=True):
    # Create collector
    collector = AnimationDataCollector(
        algorithm_name=algo_name,
        grid_size=city.size,
        start=start,
        goal=goal
    )
    
    # Run with animation collection
    start_time = time.time()
    path, cost, visited = algo_func.find_path(
        city.graph, 
        start, 
        goal,
        animation_collector=collector  # Pass collector
    )
    exec_time = time.time() - start_time
    
    # Set graph data
    edges = [(u, v, city.graph[u][v]['weight']) for u, v in city.graph.edges()]
    collector.set_graph_data(edges)
    collector.set_result(path, cost, exec_time)
    
    # Save animation data
    if save_animation:
        output_dir = "results/animation_data"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{algo_name}_{start}_{goal}_{int(time.time())}.json"
        collector.get_data().save(filename)
    
    return {
        "algo": algo_name,
        "path": path,
        "cost": cost,
        "animation_file": filename if save_animation else None
    }
```

### Step 5: Load and Use Data in Manim

```python
import manim as mnim
from src.utils.animation_data import AlgorithmAnimationData

class PathfindingAnimation(mnim.Scene):
    def __init__(self, animation_data_file):
        super().__init__()
        self.data = AlgorithmAnimationData.from_json(animation_data_file)
    
    def construct(self):
        # Create grid
        grid = mnim.VGroup()
        for x in range(self.data.grid_size):
            for y in range(self.data.grid_size):
                cell = mnim.Square(side_length=0.3)
                cell.move_to([x, y, 0])
                grid.add(cell)
        
        self.add(grid)
        
        # Animate exploration steps
        for step in self.data.steps:
            for node in step.nodes_explored:
                x, y = node.node
                cell = mnim.Square(side_length=0.3).move_to([x, y, 0])
                
                if node.status == "visited":
                    cell.set_fill(mnim.BLUE, opacity=0.5)
                elif node.status == "solution":
                    cell.set_fill(mnim.GREEN, opacity=0.7)
                
                self.play(mnim.FadeIn(cell, duration=0.1))
        
        # Draw final path
        path_points = [mnim.np.array([x, y, 0]) for x, y in self.data.final_path]
        path_line = mnim.VMobject()
        path_line.set_points_as_corners(path_points)
        path_line.set_stroke(mnim.RED, width=3)
        
        self.play(mnim.Create(path_line))
        self.wait(2)
```

## Data Structure Saved

Each JSON file contains:

```json
{
  "algorithm_name": "A*",
  "grid_size": 50,
  "start_node": [0, 0],
  "goal_node": [49, 49],
  "edges": [[u, v, weight], ...],
  "obstacles": [[x, y], ...],
  "steps": [
    {
      "frame": 0,
      "nodes_explored": [
        {
          "step": 0,
          "node": [0, 1],
          "status": "visited",
          "metadata": {
            "g_score": 1.5,
            "f_score": 50.2,
            "heuristic": 48.7
          }
        }
      ],
      "current_node": [0, 1],
      "open_set": [...],
      "closed_set": [...]
    }
  ],
  "final_path": [[0,0], [0,1], ...],
  "path_cost": 45.3,
  "execution_time": 0.023
}
```

## Workflow

1. **Run once** → Algorithms save `algorithm_<name>_<timestamp>.json`
2. **Iterate on Manim** → Load JSON, adjust visuals, no need to re-run algorithms
3. **Store data** → Keep JSON files in `results/animation_data/` for future use

## Directory Structure

```
animation_data/
├── aStar_2024-04-16_123456.json
├── genetic_algo_2024-04-16_123457.json
└── comparison_2024-04-16_123458.json
```

## Benefits

✓ **No repeated computation** — Run algorithm once, iterate on animation many times  
✓ **Shareable** — Send JSON files to colleagues for animation generation  
✓ **Reproducible** — Exact same data regenerates deterministic animations  
✓ **Debuggable** — Inspect JSON to understand algorithm behavior  
✓ **Scalable** — Generate multiple animations from single run
