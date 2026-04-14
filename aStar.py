import heapq


class AStar:
    @staticmethod
    def runAlgo(graph, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}  # actual cost
        f_score = {start: heuristic(start, goal)}

        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)
            visited.add(current)

            if current == goal:
                # reconstruct path
                path = []
                total_cost = g_score[current]

                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)

                return path[::-1], total_cost, visited

            for neighbor in graph.neighbors(current):
                weight = graph[current][neighbor].get("weight", 1)
                tentative_g = g_score[current] + weight

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g

                    f = tentative_g + heuristic(neighbor, goal)
                    f_score[neighbor] = f

                    heapq.heappush(open_set, (f, neighbor))

        return None, float("inf"), visited

    def calculatePathCost(graph, path, weight="weight"):
        total_cost = 0
        for u, v in zip(path, path[1:]):
            if graph.has_edge(u, v):
                total_cost += graph[u][v].get(weight, 1)
            else:
                return float("inf")  # invalid path

        return total_cost
