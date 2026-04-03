import time
import random
from datetime import datetime
import pandas as pd
import os

class GeneticAlgorithm:
    def __init__(self, graph, pop_size=100, generations=200, mutation_rate=0.1):
        self.graph = graph
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.visited_nodes = []
        self.stats = {"nodes_visited": 0, "path_length": 0, "start_time": 0, "end_time":0, "duration":0}

    def solve(self, start, goal):
        startTime = time.time()
        self.stats['start_time'] = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        start, goal = str(start), str(goal)
        self.visited_nodes = []
        
       
        population = [self._generate_random_path(start, goal) for _ in range(self.pop_size)]
        
        best_path = []
        for gen in range(self.generations):
           
            population = sorted(population, key=lambda p: self._calculate_fitness(p, goal))
            best_path = population[0]
            
            if best_path[-1] == goal and gen > 50:
                break

            new_population = population[:10] 
            while len(new_population) < self.pop_size:
                p1, p2 = random.choice(population[:20]), random.choice(population[:20])
                child = self._crossover(p1, p2)
                if random.random() < self.mutation_rate:
                    child = self._mutate(child, goal)
                new_population.append(child)
            population = new_population

        endTime = time.time()
        self.stats["end_time"] = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.stats["duration"] = endTime - startTime
        self.stats["path_length"] = self._path_length(best_path)
        self.stats["nodes_visited"] = len(self.visited_nodes)
        return best_path

    def _generate_random_path(self, start, goal, max_steps=40):
        path = [start]
        curr = start
        for _ in range(max_steps):
            if curr == goal: break
            neighbors = self.graph.adj.get(curr, [])
            if not neighbors: break
            curr = random.choice(neighbors)[0]
            path.append(curr)
            if curr not in self.visited_nodes: self.visited_nodes.append(curr)
        return path

    def _calculate_fitness(self, path, goal):
        dist = self._path_length(path)
        if path[-1] != goal: dist += 1000000 
        return dist

    def _path_length(self, path):
        total = 0
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            found = False
            for neighbor, weight in self.graph.adj.get(u, []):
                if neighbor == v:
                    total += weight
                    found = True
                    break
            if not found: total += 5000 
        return total

    def _crossover(self, p1, p2):
        common = list(set(p1) & set(p2))
        if len(common) < 2: return p1
        node = random.choice(common)
        return p1[:p1.index(node)] + p2[p2.index(node):]

    def _mutate(self, path, goal):
        if len(path) < 2: return path
        idx = random.randint(0, len(path)-1)
        new_segment = self._generate_random_path(path[idx], goal, max_steps=15)
        return path[:idx] + new_segment

    def print_performance(self):
        print(f"--- GA Performance Stats ---")
        print(f"Total Time: {self.stats['duration']:.4f}s | Path Length: {self.stats['path_length']:.2f}")

    def save_performance(self, fileName):
        data = {
            'Started at': [self.stats['start_time']],
            'Ended at': [self.stats['end_time']],
            'Total Time': [f"{self.stats['duration']:.4f}"],
            'Nodes Explored': [self.stats['nodes_visited']],
            'Path Length': [f"{self.stats['path_length']:.2f}"]
        }
        df = pd.DataFrame(data)
        if not os.path.isfile(fileName):
            df.to_csv(fileName, index=False)
        else:
            df.to_csv(fileName, mode='a', header=False, index=False)
