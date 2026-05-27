import heapq

def dijkstra(grid):
    start = grid.start
    end = grid.end
    if not start or not end:
        return [], []

    open_set = [(0, id(start), start)]
    came_from = {}
    dist = {start: 0}
    visited_order = []

    while open_set:
        cost, _, current = heapq.heappop(open_set)
        visited_order.append(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], visited_order

        for neighbor in grid.get_neighbors(current):
            new_cost = dist[current] + neighbor.cost
            if new_cost < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(open_set, (new_cost, id(neighbor), neighbor))

    return [], visited_order