def dfs(grid):
    start = grid.start
    end = grid.end
    if not start or not end:
        return [], []

    stack = [start]
    came_from = {start: None}
    visited_order = []

    while stack:
        current = stack.pop()
        if current in visited_order:
            continue
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
                stack.append(neighbor)

    return [], visited_order