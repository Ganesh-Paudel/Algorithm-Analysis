class GeneticAlgorithm:
    def __init__(self, graph, pop_size=50, generations=100):
        self.graph = graph
        self.pop_size = pop_size
        self.generations = generations
        self.visited_nodes = [] # All nodes touched during evolution

    def _get_random_path(self, start, goal, max_steps=100):
        path = [start]
        curr = start
        for _ in range(max_steps):
            if curr == goal: break
            neighbors = self.graph.adj.get(curr, [])
            if not neighbors: return None
            curr = neighbors[np.random.randint(len(neighbors))][0]
            path.append(curr)
            self.visited_nodes.append(curr)
        return path if path[-1] == goal else None

    def calculate_fitness(self, path):
        if not path: return 0
        length = sum(next(w for v, w in self.graph.adj[path[i]] if v == path[i+1]) 
                     for i in range(len(path)-1))
        return 1 / (length + 1e-6)

    def solve(self, start, goal):
        start, goal = str(start), str(goal)
        population = [p for _ in range(self.pop_size * 2) if (p := self._get_random_path(start, goal))]
        population = population[:self.pop_size]

        for _ in range(self.generations):
            if not population: break
            population = sorted(population, key=self.calculate_fitness, reverse=True)
        
        self.path = population[0] if population else []
        return self.path
