"""
Manim animation scene for visualizing pathfinding algorithm exploration.

This script loads animation data from JSON and creates Manim visualizations.
Run with: manim -pql manim_scene.py PathfindingAnimation
"""

try:
    import manim as mnim
    from manim import *
except ImportError:
    print("Manim not installed. Install with: pip install manim")
    exit(1)

import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.animation_data import AlgorithmAnimationData


class PathfindingAnimation(mnim.Scene):
    """
    Manim scene for visualizing pathfinding algorithm exploration.
    
    Usage:
        1. Generate animation data: python examples/animation_example.py
        2. Run Manim: manim -pql visualization/manim_scene.py PathfindingAnimation
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None
        self.grid = None
        self.cell_size = 0.3
        
    def load_animation_data(self, json_file: str) -> None:
        """Load animation data from JSON file"""
        if not os.path.exists(json_file):
            print(f"Error: Animation data file not found: {json_file}")
            return
        print(json_file)
        self.data = AlgorithmAnimationData.from_json(json_file)
        print(f"Loaded animation data for {self.data.algorithm_name}")
    
    def setup_grid(self) -> None:
        """Create and setup the grid visualization"""
        if not self.data:
            print("No animation data loaded")
            return
        
        grid_size = self.data.grid_size
        self.grid = VMobject()
        
        # Create grid cells
        for x in range(grid_size):
            for y in range(grid_size):
                cell = Square(side_length=self.cell_size, stroke_width=0.5)
                cell.set_stroke(GRAY, width=0.5)
                cell.move_to([x * self.cell_size, y * self.cell_size, 0])
                self.grid.add(cell)
        
        # Center the grid
        self.grid.center()
        
        # Scale to fit in frame
        self.grid.scale_to_fit_width(self.camera.frame_width * 0.9)
        
        print(f"Grid created: {grid_size}x{grid_size}")
    
    def mark_start_goal(self) -> None:
        """Mark start and goal positions"""
        if not self.data:
            return
        
        # Create start marker
        start_x, start_y = self.data.start_node
        start_circle = Circle(radius=self.cell_size * 0.4, color=GREEN, fill_opacity=0.7)
        
        # Create goal marker
        goal_x, goal_y = self.data.goal_node
        goal_circle = Circle(radius=self.cell_size * 0.4, color=RED, fill_opacity=0.7)
        
        # Position them relative to grid
        scale_factor = self.grid.width / self.data.grid_size
        grid_offset_x = self.grid.get_left()[0]
        grid_offset_y = self.grid.get_bottom()[1]
        
        start_circle.move_to([
            grid_offset_x + start_x * scale_factor + scale_factor / 2,
            grid_offset_y + start_y * scale_factor + scale_factor / 2,
            0
        ])
        
        goal_circle.move_to([
            grid_offset_x + goal_x * scale_factor + scale_factor / 2,
            grid_offset_y + goal_y * scale_factor + scale_factor / 2,
            0
        ])
        
        self.add(start_circle, goal_circle)
        print(f"Start: {self.data.start_node} (green), Goal: {self.data.goal_node} (red)")
    
    def animate_exploration(self) -> None:
        """Animate the exploration steps"""
        if not self.data or not self.data.steps:
            print("No exploration steps to animate")
            return
        
        print(f"Animating {len(self.data.steps)} exploration steps...")
        
        # Get grid dimensions for positioning
        scale_factor = self.grid.width / self.data.grid_size
        grid_offset_x = self.grid.get_left()[0]
        grid_offset_y = self.grid.get_bottom()[1]
        
        # Animate each step
        for step_idx, step in enumerate(self.data.steps):
            if step_idx % max(1, len(self.data.steps) // 50) == 0:  # Log progress
                print(f"  Step {step_idx}/{len(self.data.steps)}")
            
            for node_data in step.nodes_explored:
                x, y = node_data.node
                
                # Create cell for this node
                cell = Square(side_length=self.cell_size * 0.95, stroke_width=0)
                
                # Color based on status
                if node_data.status == "visited":
                    cell.set_fill(BLUE, opacity=0.5)
                elif node_data.status == "solution":
                    cell.set_fill(GREEN, opacity=0.7)
                elif node_data.status == "generation":
                    cell.set_fill(YELLOW, opacity=0.5)
                else:
                    cell.set_fill(BLUE, opacity=0.3)
                
                # Position cell
                cell.move_to([
                    grid_offset_x + x * scale_factor + scale_factor / 2,
                    grid_offset_y + y * scale_factor + scale_factor / 2,
                    0
                ])
                
                # Animate appearance
                self.play(FadeIn(cell, run_time=0.05))
    
    def animate_final_path(self) -> None:
        """Animate the final solution path"""
        if not self.data or not self.data.final_path:
            print("No final path to animate")
            return
        
        print("Animating final path...")
        
        # Get grid dimensions
        scale_factor = self.grid.width / self.data.grid_size
        grid_offset_x = self.grid.get_left()[0]
        grid_offset_y = self.grid.get_bottom()[1]
        
        # Create line for the path
        path_points = []
        for x, y in self.data.final_path:
            point = np.array([
                grid_offset_x + x * scale_factor + scale_factor / 2,
                grid_offset_y + y * scale_factor + scale_factor / 2,
                0
            ])
            path_points.append(point)
        
        if len(path_points) > 1:
            path_line = VMobject()
            path_line.set_points_as_corners(path_points)
            path_line.set_stroke(GOLD, width=2)
            
            self.play(Create(path_line, run_time=1))
            self.wait(1)
    
    def construct(self):
        """Main scene construction"""
        # Try to load animation data from default location
        animation_files = [
            "results/animation_data/genetic_algo_example.json"
        ]
        
        loaded = False
        for json_file in animation_files:
            if os.path.exists(json_file):
                self.load_animation_data(json_file)
                loaded = True
                break
        
        if not loaded:
            print("No animation data found. Run: python examples/animation_example.py")
            return
        
        # Setup scene
        self.setup_grid()
        self.add(self.grid)
        self.mark_start_goal()
        
        # Add title
        title = Text(f"{self.data.algorithm_name} - Pathfinding Visualization")
        title.to_edge(UP)
        self.add(title)
        
        # Add info text
        info = Text(
            f"Path Cost: {self.data.path_cost:.2f} | "
            f"Time: {self.data.execution_time:.4f}s | "
            f"Nodes: {self.data.total_nodes_visited}",
            font_size=24
        )
        info.to_edge(DOWN)
        self.add(info)
        
        self.wait(1)
        
        # Animate exploration
        self.animate_exploration()
        
        # Animate final path
        self.animate_final_path()
        
        self.wait(2)


if __name__ == "__main__":
    # This allows running the file directly
    print("To render this animation, run:")
    print("  manim -pql visualization/manim_scene.py PathfindingAnimation")
