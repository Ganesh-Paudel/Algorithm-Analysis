from queue import PriorityQueue
import time 
from datetime import datetime
import pandas as pd
import os

class AStar:
    def __init__(self, graph):
        self.graph = graph
        self.visited_nodes = []
        self.path = []
        self.stats = {"nodes_visited": 0, "path_length": 0, "start_time": 0, "end_time":0,"duration":0}

    def solve(self, start, goal):
        startTime = time.time()
        self.stats['start_time'] = datetime.now().strftime("%H:%M:%S.%f")[:3]
        start, goal = str(start), str(goal)
        pq = PriorityQueue()
        pq.put((0, start))
        
        came_from = {start: None}
        cost_so_far = {start: 0}
        self.visited_nodes = []

        while not pq.empty():
            current = pq.get()[1]
            self.visited_nodes.append(current)
            self.stats["nodes_visited"] += 1

            if current == goal:
                break

            for neighbor, weight in self.graph.adj.get(current, []):
                new_cost = cost_so_far[current] + weight
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.graph.get_heuristic(neighbor, goal)
                    pq.put((priority, neighbor))
                    came_from[neighbor] = current

        curr = goal
        while curr is not None:
            self.path.append(curr)
            curr = came_from.get(curr)
        self.path.reverse()

        endTime = time.time()
        self.stats["end_time"] = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.stats["duration"] = endTime - startTime
        self.stats["path_length"] = cost_so_far.get(goal, 0)
        return self.path

    def print_performance(self):
        print("--- Performance Stats ---")
        print(f"Started at:  {self.stats['start_time']}")
        print(f"Ended at:    {self.stats['end_time']}")
        print(f"Total Time:  {self.stats['duration']:.4f} seconds")
        print(f"Nodes Explored: {self.stats['nodes_visited']}")
        print(f"Path Length: {self.stats['path_length']:.2f} meters")
            
    def save_performance(self,fileName):
        data = {
            'Started at': [self.stats['start_time']],
            'Ended at': [self.stats['end_time']],
            'Total Time': [f"{self.stats['duration']:.4f}"],
            'Nodes Explored': [self.stats['nodes_visited']],
            'Path Length': [f"{self.stats['path_length']:.2f}"]
        }
        df_new = pd.DataFrame(data)

        file_exists = os.path.isfile(fileName)

        df_new.to_csv(fileName,
                    mode='a',
                    index=False,
                    header=not file_exists)
