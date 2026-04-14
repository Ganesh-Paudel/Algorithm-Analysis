# Developer Guide

## Overview

This guide is for developers who want to contribute to, extend, or modify the Algorithm Analysis project. It covers coding standards, architecture guidelines, testing practices, and contribution workflows.

## Development Environment Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment tools
- Code editor (VS Code recommended)

### Setup Steps

1. **Fork and Clone:**
   ```bash
   git clone https://github.com/yourusername/Algorithm-Analysis.git
   cd Algorithm-Analysis
   ```

2. **Create Development Environment:**
   ```bash
   python -m venv dev_env
   source dev_env/bin/activate  # Windows: dev_env\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If development dependencies exist
   ```

3. **Install Pre-commit Hooks:**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

4. **Run Tests:**
   ```bash
   python -m pytest tests/
   ```

## Code Organization

### Directory Structure

```
src/
├── algorithms/     # Pathfinding algorithm implementations
├── environments/   # Graph and traffic scenario management
└── utils/         # Shared utilities and helpers

analysis/          # Experiment orchestration and analysis
config/           # Configuration management
tests/            # Unit and integration tests
docs/             # Documentation
```

### Naming Conventions

- **Modules**: lowercase_with_underscores (e.g., `algorithm_factory.py`)
- **Classes**: PascalCase (e.g., `AStarAlgorithm`)
- **Functions/Methods**: lowercase_with_underscores (e.g., `find_path()`)
- **Constants**: UPPERCASE_WITH_UNDERSCORES (e.g., `DEFAULT_POPULATION_SIZE`)
- **Variables**: lowercase_with_underscores (e.g., `path_cost`)

### Import Organization

```python
# Standard library imports
import os
import sys
from typing import List, Dict, Tuple

# Third-party imports
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Local imports
from .base import BaseAlgorithm
from ..utils.performance import PerformanceMonitor
```

## Architecture Guidelines

### Algorithm Implementation

All algorithms must inherit from `BaseAlgorithm` and implement the standard interface:

```python
from .base import BaseAlgorithm, PathResult

class NewAlgorithm(BaseAlgorithm):
    def find_path(self, graph: nx.Graph, start: Tuple[int, int],
                  goal: Tuple[int, int], **kwargs) -> PathResult:
        """
        Find path from start to goal.

        Args:
            graph: NetworkX graph with edge weights
            start: Starting node coordinates
            goal: Goal node coordinates
            **kwargs: Algorithm-specific parameters

        Returns:
            PathResult object with path and metadata
        """
        # Implementation here
        path = self._compute_path(graph, start, goal, **kwargs)
        cost = self._calculate_cost(graph, path)

        return PathResult(
            path=path,
            cost=cost,
            length=len(path) - 1,
            success=len(path) > 1,
            metadata={'algorithm_specific_data': value}
        )
```

### Environment Extensions

New environments should extend `TrafficEnvironment`:

```python
from .trafficEnvironment import TrafficEnvironment

class CustomEnvironment(TrafficEnvironment):
    def apply_traffic_scenario(self, scenario_type: str, **params) -> nx.Graph:
        """Apply custom traffic scenario."""
        if scenario_type == "custom_pattern":
            return self._apply_custom_pattern(**params)
        return super().apply_traffic_scenario(scenario_type, **params)

    def _apply_custom_pattern(self, **params) -> nx.Graph:
        """Implement custom traffic logic."""
        # Implementation here
        pass
```

### Adding Performance Metrics

Extend `PerformanceMonitor` for new metrics:

```python
from .performance import PerformanceMonitor

class ExtendedPerformanceMonitor(PerformanceMonitor):
    def measure_custom_metric(self, algorithm_result) -> float:
        """Calculate custom performance metric."""
        # Implementation here
        return custom_value

    def get_all_metrics(self) -> Dict[str, float]:
        """Return all metrics including custom ones."""
        metrics = super().get_all_metrics()
        metrics['custom_metric'] = self.measure_custom_metric(self._result)
        return metrics
```

## Testing

### Test Structure

Tests are organized in `tests/` directory:

```
tests/
├── __init__.py
├── test_algorithms.py     # Algorithm unit tests
├── test_environments.py   # Environment tests
├── test_performance.py    # Performance monitoring tests
└── test_integration.py    # End-to-end tests
```

### Writing Unit Tests

Use pytest framework:

```python
import pytest
import networkx as nx
from src.algorithms.aStar import AStarAlgorithm

class TestAStarAlgorithm:
    def setup_method(self):
        """Set up test fixtures."""
        self.algorithm = AStarAlgorithm()
        self.graph = nx.grid_2d_graph(5, 5)
        # Add edge weights
        for u, v in self.graph.edges():
            self.graph[u][v]['weight'] = 1.0

    def test_find_path_success(self):
        """Test successful path finding."""
        start, goal = (0, 0), (4, 4)
        result = self.algorithm.find_path(self.graph, start, goal)

        assert result.success
        assert result.path[0] == start
        assert result.path[-1] == goal
        assert result.cost > 0

    def test_find_path_no_solution(self):
        """Test behavior when no path exists."""
        # Remove all edges from start
        start = (0, 0)
        edges_to_remove = list(self.graph.edges(start))
        self.graph.remove_edges_from(edges_to_remove)

        result = self.algorithm.find_path(self.graph, start, (4, 4))

        assert not result.success
        assert result.path == []

    @pytest.mark.parametrize("start,goal,expected_length", [
        ((0, 0), (0, 1), 2),
        ((0, 0), (1, 1), 3),
        ((0, 0), (2, 2), 5),
    ])
    def test_path_lengths(self, start, goal, expected_length):
        """Test path lengths for various start/goal pairs."""
        result = self.algorithm.find_path(self.graph, start, goal)

        assert len(result.path) == expected_length
```

### Integration Tests

Test complete workflows:

```python
from analysis.comparison import AlgorithmComparator
from src.utils.algorithm_factory import AlgorithmFactory

def test_algorithm_comparison():
    """Test end-to-end algorithm comparison."""
    factory = AlgorithmFactory()
    algorithms = [
        factory.create_algorithm('astar'),
        factory.create_algorithm('genetic')
    ]

    comparator = AlgorithmComparator()
    results = comparator.run_comparison(algorithms, runs=3)

    assert len(results) == 6  # 2 algorithms × 3 runs
    assert 'algorithm' in results.columns
    assert 'execution_time' in results.columns
    assert all(results['success'])  # All runs should succeed
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_algorithms.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_algorithms.py::TestAStarAlgorithm::test_find_path_success
```

## Code Quality

### Linting and Formatting

Use black for code formatting and flake8 for linting:

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Fix common issues
autopep8 --in-place --aggressive --aggressive src/
```

### Type Hints

All code should include type hints:

```python
from typing import List, Dict, Tuple, Optional, Union

def find_path(self, graph: nx.Graph, start: Tuple[int, int],
              goal: Tuple[int, int], **kwargs) -> PathResult:
    """Find path with type hints."""
    pass
```

### Documentation

Use Google-style docstrings:

```python
def find_path(self, graph: nx.Graph, start: Tuple[int, int],
              goal: Tuple[int, int], **kwargs) -> PathResult:
    """Find shortest path from start to goal using A* algorithm.

    This method implements the A* pathfinding algorithm with Manhattan
    distance heuristic to find the optimal path in a weighted graph.

    Args:
        graph: NetworkX graph with 'weight' edge attributes
        start: Tuple of (x, y) coordinates for starting node
        goal: Tuple of (x, y) coordinates for goal node
        **kwargs: Additional algorithm-specific parameters
            - heuristic_weight: Multiplier for heuristic function (default: 1.0)

    Returns:
        PathResult object containing:
            - path: List of (x, y) coordinates from start to goal
            - cost: Total cost of the path
            - length: Number of edges in path
            - success: True if path found, False otherwise
            - metadata: Additional algorithm information

    Raises:
        ValueError: If start or goal nodes not in graph

    Examples:
        >>> algorithm = AStarAlgorithm()
        >>> result = algorithm.find_path(graph, (0, 0), (5, 5))
        >>> print(f"Path cost: {result.cost}")
        Path cost: 10.0
    """
```

## Contribution Workflow

### Branching Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Critical fixes

### Pull Request Process

1. **Create Feature Branch:**
   ```bash
   git checkout -b feature/new-algorithm
   ```

2. **Make Changes:**
   - Follow coding standards
   - Add/update tests
   - Update documentation
   - Ensure all tests pass

3. **Commit Changes:**
   ```bash
   git add .
   git commit -m "Add new algorithm implementation

   - Implement NewAlgorithm class
   - Add comprehensive unit tests
   - Update documentation"
   ```

4. **Push and Create PR:**
   ```bash
   git push origin feature/new-algorithm
   # Create pull request on GitHub
   ```

5. **Code Review:**
   - Address reviewer feedback
   - Ensure CI/CD passes
   - Get approval from maintainers

6. **Merge:**
   - Squash merge to maintain clean history
   - Delete feature branch

### Commit Guidelines

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

Examples:
```
feat(algorithms): add Dijkstra algorithm implementation
fix(performance): resolve memory leak in genetic algorithm
docs(api): update API reference for new methods
test(algorithms): add integration tests for path finding
```

## Performance Optimization

### Profiling Code

Use cProfile for performance analysis:

```python
import cProfile
import pstats

def profile_algorithm():
    algorithm = AStarAlgorithm()
    graph = create_large_graph()

    profiler = cProfile.Profile()
    profiler.enable()

    result = algorithm.find_path(graph, (0, 0), (99, 99))

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions

if __name__ == "__main__":
    profile_algorithm()
```

### Memory Optimization

- Use generators for large data processing
- Cache expensive computations
- Avoid unnecessary object creation
- Use appropriate data structures

### Algorithm Tuning

- Profile bottleneck operations
- Optimize hot paths
- Consider algorithmic improvements
- Balance time vs space trade-offs

## Debugging

### Logging

Use Python's logging module:

```python
import logging

logger = logging.getLogger(__name__)

class AStarAlgorithm(BaseAlgorithm):
    def find_path(self, graph, start, goal, **kwargs):
        logger.debug(f"Finding path from {start} to {goal}")

        # Implementation with logging
        logger.info(f"Path found with cost {result.cost}")
        return result
```

### Debug Configuration

```python
# In main.py or test files
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

## Continuous Integration

### GitHub Actions Setup

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pip install pytest pytest-cov
        pytest --cov=src --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Release Process

### Version Management

Use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features
- **PATCH**: Bug fixes

### Release Checklist

- [ ] Update version in `setup.py` or `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Create git tag
- [ ] Create GitHub release
- [ ] Update documentation

### Distribution

```bash
# Build distribution
python setup.py sdist bdist_wheel

# Upload to PyPI
twine upload dist/*
```

## Security Considerations

### Input Validation

Always validate inputs:

```python
def find_path(self, graph, start, goal, **kwargs):
    if not isinstance(graph, nx.Graph):
        raise ValueError("graph must be a NetworkX Graph")

    if start not in graph.nodes():
        raise ValueError(f"start node {start} not in graph")

    if goal not in graph.nodes():
        raise ValueError(f"goal node {goal} not in graph")

    # Validate kwargs
    valid_params = {'heuristic_weight', 'max_iterations'}
    invalid_params = set(kwargs.keys()) - valid_params
    if invalid_params:
        raise ValueError(f"Invalid parameters: {invalid_params}")
```

### Secure Dependencies

- Keep dependencies updated
- Use `pip-audit` to check for vulnerabilities
- Pin dependency versions in `requirements.txt`

## Getting Help

### Resources

- **Architecture.md**: System design overview
- **API_Reference.md**: Detailed API documentation
- **tests/**: Working examples
- **GitHub Issues**: Bug reports and feature requests

### Communication

- Use GitHub issues for bugs and features
- Use GitHub discussions for questions
- Follow code of conduct
- Be respectful and constructive

Happy coding!