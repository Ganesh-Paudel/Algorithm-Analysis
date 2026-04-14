# Algorithm Analysis Project

## Overview

This project is a comprehensive analysis and comparison framework for pathfinding algorithms in dynamic traffic environments. It implements and evaluates multiple algorithms (A* and Genetic Algorithm) on graph-based traffic scenarios, measuring performance metrics such as path cost, execution time, and convergence behavior. The system generates synthetic traffic data, runs comparative experiments, and produces detailed visualizations and performance reports.

The project is designed to help researchers and developers understand how different pathfinding approaches perform under varying traffic conditions, from single congestion points to complex multi-obstacle scenarios. It provides a modular architecture that makes it easy to add new algorithms, environments, and analysis tools.

## Key Features

- **Modular Algorithm Implementation**: Clean separation of algorithms, environments, and analysis tools
- **Dynamic Traffic Simulation**: Realistic traffic scenarios with configurable congestion points
- **Comprehensive Performance Analysis**: 11+ metrics per experiment including execution time, path quality, and convergence data
- **Visualization Tools**: Charts and graphs for algorithm comparison and performance trends
- **Scalable Testing**: Support for varying graph sizes and traffic complexity
- **Data-Driven Insights**: CSV-based results for statistical analysis and reporting

## Technologies Used

- **Python 3.8+**: Core programming language
- **NetworkX**: Graph creation, manipulation, and pathfinding operations
- **Matplotlib**: Data visualization and chart generation
- **Pandas**: Data manipulation and CSV handling
- **NumPy**: Numerical computations and array operations
- **Random/Seed Management**: Reproducible random number generation for consistent testing

## Algorithms Implemented

### A* Algorithm

**Overview**: A* is a best-first search algorithm that finds the shortest path between two nodes in a graph. It uses both the actual cost from start to current node and an estimated cost from current node to goal.

**Implementation Details**:
- Located in `src/algorithms/aStar.py`
- Uses Manhattan distance heuristic for grid-based graphs
- Implements priority queue for efficient node exploration
- Handles dynamic edge weights for traffic simulation

**Mathematical Foundation**:
- **Heuristic Function**: h(n) = |x_goal - x_current| + |y_goal - y_current| (Manhattan distance)
- **Total Cost**: f(n) = g(n) + h(n), where:
  - g(n): Actual cost from start to node n
  - h(n): Estimated cost from node n to goal
- **Admissibility**: h(n) ≤ h*(n) (true cost), ensuring optimality
- **Consistency**: h(n) ≤ c(n,n') + h(n') for all neighbors n'

### Genetic Algorithm

**Overview**: A population-based optimization algorithm inspired by natural evolution. It evolves a population of potential solutions through selection, crossover, and mutation to find optimal paths.

**Implementation Details**:
- Located in `src/algorithms/geneticAlgo.py`
- Population size: 50 individuals (optimized for performance)
- Uses tournament selection for parent selection
- Implements single-point crossover and mutation operators
- Cost caching mechanism to avoid redundant calculations
- NetworkX seeding for reproducible graph operations

**Mathematical Foundation**:
- **Fitness Function**: f(path) = total_edge_weight(path) (minimize for shortest path)
- **Selection**: Tournament selection with tournament size k=3
- **Crossover**: Single-point crossover with probability p_c = 0.8
- **Mutation**: Random node replacement with probability p_m = 0.1
- **Elitism**: Preserves best 10% of population per generation
- **Termination**: Maximum 100 generations or convergence criteria

## Project Structure

```
Algorithm-Analysis/
├── src/
│   ├── algorithms/
│   │   ├── aStar.py          # A* algorithm implementation
│   │   ├── geneticAlgo.py    # Genetic algorithm implementation
│   │   └── base.py           # Base algorithm interface
│   ├── environments/
│   │   ├── traffic.py        # Traffic scenario generation
│   │   └── trafficEnvironment.py  # Environment management
│   └── utils/
│       ├── algorithm_factory.py   # Algorithm instantiation
│       └── performance.py         # Performance measurement
├── analysis/
│   ├── comparison.py         # Algorithm comparison and visualization
│   ├── results_aggregator.py # Results aggregation
│   ├── runner.py             # Experiment orchestration
│   └── unified_comparison.py # Unified analysis tools
├── config/
│   └── config.py             # Configuration management
├── data/
│   └── inputTestData.csv     # Test data input
├── results/
│   ├── performanceResults.csv # Performance data output
│   └── charts/               # Generated visualizations
├── tests/
│   └── quick_test.py         # Unit tests
├── visualization/
│   └── visualize.py          # Visualization utilities
├── scripts/
│   └── comparison_runner.py  # Script execution
├── docs/
│   ├── Architecture.md       # Architecture documentation
│   └── Readme.md             # Additional documentation
├── main.py                   # Main entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Algorithm-Analysis
   ```

2. **Create Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**:
   ```bash
   python -c "import networkx, matplotlib, pandas, numpy; print('All dependencies installed successfully')"
   ```

## Usage

### Running Experiments

1. **Basic Experiment**:
   ```bash
   python main.py
   ```
   This runs the default experiment comparing A* and Genetic algorithms on standard traffic scenarios.

2. **Custom Configuration**:
   - Modify `config/config.py` to adjust algorithm parameters, graph sizes, or traffic scenarios
   - Edit `data/inputTestData.csv` to provide custom test data

3. **Running Specific Tests**:
   ```bash
   python tests/quick_test.py
   ```

### Generating Visualizations

```bash
python analysis/comparison.py
```

This generates comparison charts and saves them to `results/charts/`.

### Analyzing Results

Performance data is automatically saved to `results/performanceResults.csv`. Use the analysis tools in `analysis/` to process and visualize results.

### Key Configuration Options

- **Graph Size**: Configure in `config/config.py` (default: 20x20 grid)
- **Traffic Scenarios**: Adjust congestion points and severity in `src/environments/traffic.py`
- **Algorithm Parameters**: Modify population size, generations, etc. in respective algorithm files
- **Performance Metrics**: Customize metrics in `src/utils/performance.py`

## Understanding the Output

### Performance Metrics

The system records 11+ metrics per experiment:
- Execution time
- Path cost/length
- Convergence generation (for Genetic Algorithm)
- Memory usage
- Success rate
- Path quality metrics

### Visualization Types

- Algorithm comparison charts
- Performance trend graphs
- Path visualization on traffic maps
- Convergence plots for evolutionary algorithms

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed and virtual environment is activated
2. **Performance Issues**: Reduce graph size or algorithm parameters for faster execution
3. **Visualization Errors**: Check matplotlib backend compatibility
4. **Memory Issues**: Decrease population size for Genetic Algorithm

### Getting Help

- Check the `docs/` directory for detailed documentation
- Review `tests/quick_test.py` for usage examples
- Examine `config/config.py` for configuration options

## Future Enhancements

- Additional algorithms (Dijkstra, BFS, etc.)
- Real-time traffic data integration
- Machine learning-based traffic prediction
- Web-based visualization interface
- Parallel processing for large-scale experiments