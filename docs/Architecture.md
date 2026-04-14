# Modular Algorithm Analysis Framework

## Overview

This framework provides a flexible, modular architecture for comparing pathfinding algorithms. It's designed to make it easy to:

- **Switch between algorithms** with a single parameter
- **Configure algorithm parameters** centrally
- **Run comprehensive comparisons** with automatic visualization
- **Add new algorithms** without changing existing code

## Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                       │
│  (main.py, quick_test.py, custom experiments)              │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌──────────────┐  ┌──────────────────┐
│   Algorithm   │  │  Comparison  │  │   Results &      │
│   Factory     │  │  & Vis.      │  │   Aggregation    │
│ (switch algo) │  │  Module      │  │                  │
└───────┬───────┘  └──────┬───────┘  └────────┬─────────┘
        │                 │                    │
        ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│              Configuration Manager                          │
│          (centralized parameter control)                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ A* Algorithm │  │   Genetic    │  │ Other Algos  │
│              │  │  Algorithm   │  │ (extensible) │
└──────────────┘  └──────────────┘  └──────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    Traffic Env       Graph Processing    Visualization
```

### Key Files

1. **`pathfinding_algorithm.py`** - Abstract base class defining the algorithm interface
2. **`a_star.py`** - A* implementation
3. **`genetic_algorithm.py`** - Genetic algorithm implementation
4. **`algorithm_factory.py`** - Factory pattern for creating algorithms
5. **`config.py`** - Centralized configuration management
6. **`unified_comparison.py`** - Algorithm testing and visualization
7. **`results_aggregator.py`** - Results collection and analysis
8. **`main.py`** - Main entry point with full experiment runner
9. **`quick_test.py`** - Quick testing utilities

## Usage Examples

### Example 1: Run Default Comparison

```python
# main.py already configured to run A* and Genetic
python main.py
```

### Example 2: Quick Test Single Algorithm

```python
from quick_test import quick_test

# Test A*
quick_test("astar", grid_size=20)

# Test Genetic
quick_test("genetic", grid_size=25)
```

### Example 3: Custom Configuration

```python
from config import get_config
from algorithm_factory import AlgorithmFactory
from unified_comparison import run_algorithm_test
from traffic_environment import CityGraph

# Setup
config = get_config()
config.set_algorithm_config(
    "genetic",
    population_size=100,      # Larger population
    generations=200,          # More generations
    mutation_rate=0.3,        # Higher mutation rate
    elite_ratio=0.15,         # Different elite preservation
)

# Create and test
algo = AlgorithmFactory.create("genetic", **config.get_algorithm_kwargs("genetic"))
city = CityGraph(size=30)
result = run_algorithm_test(city, (5, 5), (25, 25), algo)
```

### Example 4: Add New Algorithm

To add a new algorithm:

1. Create implementation inheriting from `PathfindingAlgorithm`:

```python
# my_algorithm.py
from pathfinding_algorithm import PathfindingAlgorithm

class MyAlgorithm(PathfindingAlgorithm):
    def __init__(self, custom_param=10):
        self.name = "My Algorithm"
        self.custom_param = custom_param

    def find_path(self, graph, start, goal):
        # Your implementation
        # Must return (path, cost, visited_nodes)
        return path, cost, visited
```

2. Register it with the factory:

```python
# In your experiment script
from algorithm_factory import AlgorithmFactory
from my_algorithm import MyAlgorithm

AlgorithmFactory.register("myalgo", MyAlgorithm)

# Now use it like any other algorithm
algo = AlgorithmFactory.create("myalgo", custom_param=20)
```

### Example 5: Compare Multiple Configurations

```python
from config import get_config
from algorithm_factory import AlgorithmFactory
from unified_comparison import run_algorithm_test
from traffic_environment import CityGraph

config = get_config()

# Test different genetic algorithm configurations
configurations = [
    {"label": "Conservative", "population_size": 30, "generations": 50},
    {"label": "Balanced", "population_size": 50, "generations": 100},
    {"label": "Aggressive", "population_size": 100, "generations": 200},
]

for config_params in configurations:
    label = config_params.pop("label")
    print(f"\nTesting: {label}")
    
    config.set_algorithm_config("genetic", **config_params)
    algo = AlgorithmFactory.create("genetic", **config.get_algorithm_kwargs("genetic"))
    
    city = CityGraph(size=20)
    result = run_algorithm_test(city, (5, 5), (15, 15), algo)
    print(f"  Cost: {result.rerouted_cost:.2f}")
    print(f"  Runtime: {result.dynamic_runtime:.4f}s")
```

## Configuration Management

### Centralized via `config.py`

```python
from config import get_config

config = get_config()

# Set active algorithms to test
config.set_active_algorithms("astar", "genetic")

# Configure parameters
config.set_algorithm_config("genetic",
    population_size=75,
    generations=150,
    mutation_rate=0.25)

# Get configuration for factory
kwargs = config.get_algorithm_kwargs("genetic")  # Returns dict with all params

# Print current config
print(config.get_summary())
```

### Per-Algorithm Configuration

Each algorithm can have custom parameters without affecting others.

## Running Comparisons

### Full Comparison (main.py)

Tests all configured algorithms on all test data:

```bash
python main.py
```

Produces:
- Console output with detailed metrics
- Path visualization for each experiment
- Comparison charts (success rate, costs, runtime, etc.)

### Quick Testing (quick_test.py)

```python
from quick_test import quick_test, compare_all_algorithms, test_with_custom_parameters

# Single algorithm
quick_test("astar", grid_size=20)

# Compare all algorithms
compare_all_algorithms(grid_size=20)

# Test with custom parameters
test_with_custom_parameters()
```

## Results Analysis

### Aggregated Results

```python
from results_aggregator import ResultsAggregator

aggregator = ResultsAggregator()
# ... add rounds ...

# Get summary for one algorithm
summary = aggregator.get_summary_by_algorithm("astar")

# Get comparison table
comparison = aggregator.get_comparison_table()

# Print formatted summary
aggregator.print_summary()

# Export to JSON
json_data = aggregator.to_json()
```

### Available Metrics

Per algorithm per test:
- `success` - Whether a path was found
- `static_cost` - Cost of initial path
- `cost_after_traffic` - Cost of same path under traffic
- `rerouted_cost` - Cost after dynamic replanning
- `improvement_percent` - Improvement from rerouting
- `nodes_explored` - Search space size
- `static_runtime` - Time for initial search
- `dynamic_runtime` - Time for rerouting

## Visualization

### Path Visualizations

```python
from unified_comparison import visualize_path_comparison

visualize_path_comparison(
    graph,
    static_path,
    rerouted_path,
    affected_edges,
    "algorithm_name",
    title="My Algorithm Paths",
    output_path="output/my_visualization.png"
)
```

### Comparison Charts

```python
from unified_comparison import visualize_comparison_charts

visualize_comparison_charts(
    results_aggregator,
    output_dir="output/images/ComparisionCharts"
)
```

Generates:
1. Success rate comparison
2. Static path cost by grid size
3. Rerouted path cost by grid size
4. Improvement percentage by grid size
5. Search space exploration
6. Total runtime comparison

## Genetic Algorithm Improvements

The genetic algorithm implementation now includes:

- **Tournament selection** - Better selection pressure than pure random
- **Convergence detection** - Early termination when population stagnates
- **Elitism** - Preserves best solutions across generations
- **Hybrid mutation** - Both regeneration and swap mutations
- **Path validation** - Ensures all generated paths are valid
- **Dynamic segment regeneration** - Smarter mutation strategy

## Extending the Framework

### Add New Metric

```python
# In results_aggregator.py, add to AlgorithmResult:
@dataclass
class AlgorithmResult:
    # ... existing fields ...
    my_new_metric: float = 0.0

# Populate when creating result:
result = AlgorithmResult(..., my_new_metric=value)
```

### Add New Visualization

```python
# In unified_comparison.py:
def visualize_my_metric(results_aggregator, output_dir):
    # Create your visualization
    pass

# Call from main.py:
visualize_my_metric(results_aggregator)
```

### Add New Algorithm Type

```python
# my_algorithm.py
from pathfinding_algorithm import PathfindingAlgorithm

class MyAlgorithm(PathfindingAlgorithm):
    def __init__(self):
        self.name = "My Algorithm"

    def find_path(self, graph, start, goal):
        # Implementation
        return path, cost, visited_nodes

# Register in main.py or experiment script:
from algorithm_factory import AlgorithmFactory
AlgorithmFactory.register("myalgo", MyAlgorithm)
```

## Testing Workflow

1. **Configure** which algorithms and parameters to test
2. **Run** experiments using `main.py` or `quick_test.py`
3. **Analyze** results using `ResultsAggregator`
4. **Visualize** with built-in comparison charts
5. **Iterate** by adjusting configuration and running again

## Benefits of Modular Architecture

✓ **Easy algorithm switching** - Change one parameter  
✓ **Centralized configuration** - All settings in one place  
✓ **Extensible design** - Add algorithms without modifying existing code  
✓ **Comprehensive testing** - Automated experiment runner  
✓ **Rich visualization** - Automatic chart generation  
✓ **Testable** - Each component can be tested independently  
✓ **Reusable** - Components can be used in other projects  
✓ **Maintainable** - Clear separation of concerns  

