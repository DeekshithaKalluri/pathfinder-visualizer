import heapq

def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def astar(grid):
    start = grid.start
    end = grid.end
    if not start or not end:
        return [], []

    open_set = []
    heapq.heappush(open_set, (0, id(start), start))

    came_from = {}
    g_score = {start: 0}
    visited_order = []

    while open_set:
        _, _, current = heapq.heappop(open_set)
        visited_order.append(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], visited_order

        for neighbor in grid.get_neighbors(current):
            tentative_g = g_score[current] + neighbor.cost
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, end)
                heapq.heappush(open_set, (f, id(neighbor), neighbor))

    return [], visited_order