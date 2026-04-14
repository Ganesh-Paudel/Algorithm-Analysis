# User Guide

## Introduction

Welcome to the Algorithm Analysis project! This guide will help you get started with comparing pathfinding algorithms in traffic environments. Whether you're a researcher, student, or developer, this guide covers everything from installation to advanced usage.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Basic familiarity with command line

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Algorithm-Analysis
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python -c "import networkx, matplotlib, pandas; print('Ready!')"
   ```

### First Experiment

Run your first algorithm comparison:

```bash
python main.py
```

This executes a default experiment comparing A* and Genetic algorithms on a 20x20 grid with traffic congestion.

## Understanding the Project Structure

```
Algorithm-Analysis/
├── main.py              # Main entry point
├── config/config.py     # Configuration settings
├── src/                 # Core implementation
├── analysis/            # Experiment tools
├── results/             # Output data and charts
└── docs/               # Documentation
```

## Running Experiments

### Basic Usage

The simplest way to run experiments is through `main.py`:

```bash
python main.py
```

This will:
- Load default configuration
- Run A* and Genetic algorithms
- Generate performance comparisons
- Save results to `results/performanceResults.csv`
- Create charts in `results/charts/`

### Customizing Experiments

#### Modifying Configuration

Edit `config/config.py` to change:

```python
# Graph size
GRAPH_SIZE = 30  # Increase for larger environments

# Algorithm parameters
GENETIC_PARAMS = {
    'population_size': 100,  # Larger population
    'max_generations': 200   # More generations
}

# Traffic scenarios
TRAFFIC_SCENARIOS = ['single_obstacle', 'multiple_obstacles']
```

#### Command Line Options

For advanced users, you can modify `main.py` to accept command line arguments:

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--algorithms', nargs='+', default=['astar', 'genetic'])
parser.add_argument('--size', type=int, default=20)
args = parser.parse_args()
```

### Running Specific Scenarios

Use the analysis tools directly:

```python
from analysis.comparison import AlgorithmComparator
from src.utils.algorithm_factory import AlgorithmFactory

# Create comparator
comparator = AlgorithmComparator()

# Define algorithms
factory = AlgorithmFactory()
algorithms = [
    factory.create_algorithm('astar'),
    factory.create_algorithm('genetic', population_size=75)
]

# Run comparison
results = comparator.run_comparison(algorithms, runs=5)
print(results.head())
```

## Configuring Traffic Scenarios

### Available Scenarios

1. **Single Obstacle**: Circular congestion area
2. **Multiple Obstacles**: Several congestion points
3. **Random Traffic**: Probabilistic congestion distribution

### Customizing Traffic

Modify `src/environments/traffic.py`:

```python
# Create custom scenario
def create_custom_traffic(graph, centers, radii):
    for center, radius in zip(centers, radii):
        graph = generate_single_obstacle(graph, center, radius, weight_multiplier=10.0)
    return graph
```

### Adjusting Traffic Intensity

```python
# High congestion
traffic_graph = env.apply_traffic_scenario(
    "single_obstacle",
    center=(10, 10),
    radius=5,
    weight_multiplier=10.0  # High traffic penalty
)

# Low congestion
traffic_graph = env.apply_traffic_scenario(
    "random_traffic",
    congestion_probability=0.05,  # 5% chance per edge
    weight_multiplier=2.0
)
```

## Understanding Results

### Performance Metrics

The system collects 11+ metrics per experiment:

- **Execution Time**: Wall-clock time in seconds
- **Path Cost**: Total edge weights of the found path
- **Path Length**: Number of nodes in the path
- **Memory Usage**: Peak memory consumption
- **Convergence Generation**: When genetic algorithm found solution
- **Success Rate**: Whether a valid path was found

### Reading CSV Output

Results are saved as CSV with columns:
```
algorithm,scenario,run_id,execution_time,path_cost,path_length,memory_usage,...
```

### Interpreting Charts

Generated charts include:
- **Algorithm Comparison**: Bar charts of average performance
- **Convergence Plots**: How genetic algorithm improves over generations
- **Traffic Impact**: Path visualization on traffic maps

## Advanced Usage

### Custom Algorithms

To add a new algorithm:

1. Create new class in `src/algorithms/`
2. Inherit from `BaseAlgorithm`
3. Implement `find_path()` method
4. Register in `AlgorithmFactory`

Example:

```python
from src.algorithms.base import BaseAlgorithm

class DijkstraAlgorithm(BaseAlgorithm):
    def find_path(self, graph, start, goal, **kwargs):
        # Implementation here
        return PathResult(path=path, cost=cost, success=True)
```

### Custom Environments

Create new traffic patterns:

```python
from src.environments.trafficEnvironment import TrafficEnvironment

class UrbanEnvironment(TrafficEnvironment):
    def apply_traffic_scenario(self, scenario_type, **params):
        if scenario_type == "rush_hour":
            return self._create_rush_hour_traffic(**params)
        return super().apply_traffic_scenario(scenario_type, **params)
```

### Batch Experiments

Run multiple configurations:

```python
from analysis.runner import ExperimentRunner

runner = ExperimentRunner()

# Define experiment matrix
configs = [
    {'algorithm': 'astar', 'size': 20},
    {'algorithm': 'astar', 'size': 30},
    {'algorithm': 'genetic', 'population_size': 50},
    {'algorithm': 'genetic', 'population_size': 100}
]

results = runner.run_batch_experiments(configs)
```

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Memory Issues:**
- Reduce graph size in config
- Decrease genetic algorithm population
- Run fewer parallel experiments

**Slow Performance:**
- Use A* for large graphs (faster than genetic)
- Reduce max_generations for genetic algorithm
- Increase heuristic weight for A*

**Visualization Errors:**
- Ensure matplotlib backend is set
- Check write permissions for results/ directory

### Performance Tuning

**For A* Algorithm:**
- Adjust heuristic weight (1.0 = balanced, >1.0 = greedy)
- Use different heuristics for specific domains

**For Genetic Algorithm:**
- Population size: 50-200 (trade-off between quality and speed)
- Generations: 50-200 (more generations = better solutions)
- Mutation rate: 0.05-0.2 (higher = more exploration)

### Debugging

Enable debug output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug
python main.py
```

## Best Practices

### Experiment Design

1. **Reproducibility**: Use fixed random seeds
2. **Statistical Validity**: Run multiple trials (n≥10)
3. **Parameter Ranges**: Test meaningful parameter combinations
4. **Baseline Comparison**: Always include standard configurations

### Performance Analysis

1. **Multiple Metrics**: Don't rely on single performance measure
2. **Statistical Tests**: Use appropriate significance tests
3. **Scalability Testing**: Test with varying problem sizes
4. **Robustness**: Test under different traffic conditions

### Code Organization

1. **Modular Changes**: Modify one component at a time
2. **Version Control**: Commit frequently with descriptive messages
3. **Documentation**: Update docs when changing APIs
4. **Testing**: Validate changes with existing tests

## Example Workflows

### Research Study

1. Define research question
2. Design experiment matrix
3. Configure algorithms and environments
4. Run batch experiments
5. Analyze results statistically
6. Generate publication-ready charts

### Algorithm Development

1. Implement new algorithm
2. Add to factory and config
3. Create unit tests
4. Compare against baselines
5. Tune parameters
6. Document implementation

### Performance Benchmarking

1. Set up standard test cases
2. Run algorithms with various parameters
3. Collect comprehensive metrics
4. Generate comparison reports
5. Identify performance bottlenecks

## Getting Help

### Documentation Resources

- `docs/Architecture.md`: System design and components
- `docs/API_Reference.md`: Detailed API documentation
- `docs/Developer_Guide.md`: Contributing and extending

### Community Support

- Check existing issues on GitHub
- Review test cases in `tests/`
- Examine example configurations

### Reporting Issues

When reporting bugs, include:
- Python version and OS
- Full error traceback
- Configuration used
- Steps to reproduce
- Expected vs actual behavior

## Next Steps

Now that you're familiar with basic usage:

1. Explore the `analysis/` directory for advanced tools
2. Check `tests/` for usage examples
3. Review `config/config.py` for customization options
4. Read the API documentation for programmatic access

Happy experimenting!