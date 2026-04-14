# Architecture Documentation

## Overview

The Algorithm Analysis project follows a modular, object-oriented architecture designed for comparing pathfinding algorithms in dynamic traffic environments. The system is structured to support easy extension of algorithms, environments, and analysis tools while maintaining clean separation of concerns.

## Core Architecture Principles

- **Modularity**: Each component (algorithms, environments, analysis) is self-contained and interchangeable
- **Extensibility**: New algorithms and environments can be added without modifying existing code
- **Separation of Concerns**: Data generation, algorithm execution, and result analysis are distinct layers
- **Reproducibility**: Seeded random number generation ensures consistent experimental results

## System Components

### 1. Algorithm Layer (`src/algorithms/`)

**Purpose**: Contains implementations of pathfinding algorithms with a common interface.

**Key Components**:
- `base.py`: Abstract base class defining the algorithm interface
- `aStar.py`: A* algorithm implementation with Manhattan distance heuristic
- `geneticAlgo.py`: Genetic algorithm with population-based optimization

**Interface Contract**:
```python
class BaseAlgorithm:
    def find_path(self, graph, start, goal, **kwargs) -> PathResult
```

**Mathematical Foundation**:
- A*: f(n) = g(n) + h(n) where h(n) is admissible heuristic
- Genetic: Population evolution with selection, crossover, mutation operators

### 2. Environment Layer (`src/environments/`)

**Purpose**: Manages graph creation and traffic scenario generation.

**Key Components**:
- `trafficEnvironment.py`: Main environment class handling graph setup
- `traffic.py`: Traffic scenario generation with congestion modeling

**Features**:
- Dynamic edge weight modification for traffic simulation
- Configurable graph sizes and obstacle placement
- Support for single and multi-point congestion scenarios

### 3. Utilities Layer (`src/utils/`)

**Purpose**: Shared utilities for algorithm instantiation and performance measurement.

**Key Components**:
- `algorithm_factory.py`: Factory pattern for algorithm creation
- `performance.py`: Comprehensive performance metrics collection

**Metrics Collected**:
- Execution time
- Path cost and length
- Memory usage
- Convergence data (for iterative algorithms)
- Success rate

### 4. Analysis Layer (`analysis/`)

**Purpose**: Experiment orchestration, result aggregation, and visualization.

**Key Components**:
- `runner.py`: Experiment execution engine
- `comparison.py`: Algorithm comparison and charting
- `results_aggregator.py`: Data aggregation and statistical analysis
- `unified_comparison.py`: Unified analysis interface

**Data Flow**:
1. Configuration → Experiment setup
2. Algorithm execution → Performance data collection
3. Result aggregation → Statistical analysis
4. Visualization → Charts and reports

### 5. Configuration Layer (`config/`)

**Purpose**: Centralized configuration management.

**Key Components**:
- `config.py`: Global configuration parameters

**Configuration Areas**:
- Algorithm parameters (population size, generations, etc.)
- Environment settings (graph size, traffic scenarios)
- Performance settings (metrics to collect, output formats)

## Data Flow Architecture

```
Input Data (CSV)
    ↓
Configuration
    ↓
Environment Setup (Graph + Traffic)
    ↓
Algorithm Factory → Algorithm Instances
    ↓
Parallel/Sequential Execution
    ↓
Performance Measurement
    ↓
Result Aggregation
    ↓
Visualization & Reporting
```

## Design Patterns Used

### Factory Pattern
- `AlgorithmFactory` creates algorithm instances based on configuration
- Supports runtime algorithm selection without code changes

### Strategy Pattern
- Algorithms implement common interface for interchangeable execution
- Environment classes provide different traffic scenarios

### Observer Pattern
- Performance monitoring during algorithm execution
- Event-driven result collection

### Template Method Pattern
- Base algorithm class defines execution framework
- Subclasses implement specific pathfinding logic

## Dependencies and Coupling

### Low Coupling Areas
- Algorithms are independent of environments
- Analysis tools work with any algorithm output
- Visualization is decoupled from computation

### High Cohesion Areas
- Related functionality grouped in modules
- Clear responsibility boundaries
- Minimal cross-module dependencies

## Extensibility Points

### Adding New Algorithms
1. Implement `BaseAlgorithm` interface
2. Add to `AlgorithmFactory`
3. Update configuration options

### Adding New Environments
1. Extend `TrafficEnvironment` class
2. Implement traffic generation logic
3. Register in configuration

### Adding New Metrics
1. Extend `PerformanceMonitor` class
2. Add metric calculation methods
3. Update result aggregation

## Performance Considerations

### Memory Management
- Graph objects cached where possible
- Population-based algorithms use optimized data structures
- Result data streamed to disk for large experiments

### Computational Efficiency
- A* uses priority queues for O(log n) operations
- Genetic algorithm parameters tuned for convergence speed
- Parallel execution support for multiple runs

### Scalability
- Modular design supports distributed execution
- Configuration-driven parameter adjustment
- Incremental result processing

## Testing Architecture

### Unit Testing (`tests/`)
- Individual component testing
- Mock environments for algorithm testing
- Performance regression detection

### Integration Testing
- End-to-end experiment execution
- Cross-component interaction validation
- Data pipeline verification

## Deployment and Distribution

### Local Execution
- Self-contained Python package
- Virtual environment support
- Cross-platform compatibility

### Research Integration
- CSV output for external analysis
- Modular components for embedding
- Reproducible experiment configurations

## Future Architecture Evolution

### Planned Extensions
- Plugin architecture for third-party algorithms
- Web-based visualization interface
- Real-time traffic data integration
- Machine learning-based optimization

### Scalability Improvements
- Distributed computing support
- Database integration for large datasets
- Cloud deployment options