from collections import deque

def bfs(grid):
    start = grid.start
    end = grid.end
    if not start or not end:
        return [], []

    queue = deque([start])
    came_from = {start: None}
    visited_order = []

    while queue:
        current = queue.popleft()
        visited_order.append(current)

        if current == end:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1], visited_order

        for neighbor in grid.get_neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    return [], visited_order