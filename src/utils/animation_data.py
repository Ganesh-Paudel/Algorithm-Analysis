"""
Animation Data Structures for Manim Visualization
Captures step-by-step algorithm execution for independent animation generation
"""

import json
from typing import List, Dict, Tuple, Any, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass
class AnimationNode:
    """Represents a single step in algorithm exploration"""
    step: int
    node: Tuple[int, int]
    status: str  # "exploring" | "visited" | "solution" | "backtracked"
    metadata: Dict[str, Any] = field(default_factory=dict)  # algorithm-specific data


@dataclass
class AnimationStep:
    """Single animation frame's data"""
    frame: int
    nodes_explored: List[AnimationNode] = field(default_factory=list)
    current_node: Optional[Tuple[int, int]] = None
    open_set: Optional[List[Tuple[int, int]]] = None  # For A*: frontier
    closed_set: Optional[List[Tuple[int, int]]] = None  # For A*: visited
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AlgorithmAnimationData:
    """Complete animation dataset for a single algorithm run"""
    algorithm_name: str
    grid_size: int
    start_node: Tuple[int, int]
    goal_node: Tuple[int, int]
    
    # Graph data
    edges: List[Tuple[Tuple[int, int], Tuple[int, int], float]] = field(default_factory=list)
    obstacles: List[Tuple[int, int]] = field(default_factory=list)
    traffic_affected_edges: List[Tuple[Tuple[int, int], Tuple[int, int]]] = field(default_factory=list)
    
    # Algorithm execution
    steps: List[AnimationStep] = field(default_factory=list)
    final_path: List[Tuple[int, int]] = field(default_factory=list)
    path_cost: float = 0.0
    total_nodes_visited: int = 0
    execution_time: float = 0.0
    
    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_json(self) -> str:
        """Serialize to JSON"""
        return json.dumps(asdict(self), indent=2)
    
    def save(self, filepath: str) -> None:
        """Save animation data to JSON file"""
        with open(filepath, 'w') as f:
            f.write(self.to_json())
        print(f"Animation data saved to {filepath}")
    
    @classmethod
    def from_json(cls, filepath: str) -> "AlgorithmAnimationData":
        """Load animation data from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Reconstruct nested objects
        data['steps'] = [
            AnimationStep(
                frame=s['frame'],
                nodes_explored=[
                    AnimationNode(
                        step=n['step'],
                        node=tuple(n['node']),
                        status=n['status'],
                        metadata=n['metadata']
                    )
                    for n in s['nodes_explored']
                ],
                current_node=tuple(s['current_node']) if s['current_node'] else None,
                open_set=[tuple(n) for n in s['open_set']] if s['open_set'] else None,
                closed_set=[tuple(n) for n in s['closed_set']] if s['closed_set'] else None,
                metadata=s['metadata']
            )
            for s in data['steps']
        ]
        data['final_path'] = [tuple(n) for n in data['final_path']]
        data['obstacles'] = [tuple(o) for o in data['obstacles']]
        data['edges'] = [
            (tuple(e[0]), tuple(e[1]), e[2])
            for e in data['edges']
        ]
        data['traffic_affected_edges'] = [
            (tuple(e[0]), tuple(e[1]))
            for e in data['traffic_affected_edges']
        ]
        
        return cls(**data)


class AnimationDataCollector:
    """Helper class to collect animation data during algorithm execution"""
    
    def __init__(self, algorithm_name: str, grid_size: int, 
                 start: Tuple[int, int], goal: Tuple[int, int]):
        self.data = AlgorithmAnimationData(
            algorithm_name=algorithm_name,
            grid_size=grid_size,
            start_node=start,
            goal_node=goal
        )
        self.frame_counter = 0
    
    def add_step(self, nodes_explored: List[AnimationNode], 
                current_node: Optional[Tuple[int, int]] = None,
                open_set: Optional[List] = None,
                closed_set: Optional[List] = None,
                metadata: Optional[Dict] = None) -> None:
        """Record a search step"""
        step = AnimationStep(
            frame=self.frame_counter,
            nodes_explored=nodes_explored,
            current_node=current_node,
            open_set=open_set,
            closed_set=closed_set,
            metadata=metadata or {}
        )
        self.data.steps.append(step)
        self.frame_counter += 1
    
    def set_graph_data(self, edges: List, obstacles: List = None) -> None:
        """Set the graph structure"""
        self.data.edges = edges
        self.data.obstacles = obstacles or []
    
    def set_traffic_affected_edges(self, affected: List) -> None:
        """Mark which edges were affected by traffic"""
        self.data.traffic_affected_edges = affected
    
    def set_result(self, path: List, cost: float, execution_time: float) -> None:
        """Set the final result"""
        self.data.final_path = path
        self.data.path_cost = cost
        self.data.execution_time = execution_time
        self.data.total_nodes_visited = len([s for step in self.data.steps for s in step.nodes_explored])
    
    def get_data(self) -> AlgorithmAnimationData:
        """Get the collected animation data"""
        return self.data
