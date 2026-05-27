import heapq
import math

class DStarLite:
    """
    D* Lite: replans efficiently after obstacles are added mid-search.
    Searches backwards from goal → start so replanning is cheap.
    """
    def __init__(self, grid):
        self.grid = grid
        self.start = grid.start
        self.goal = grid.end
        self.k_m = 0
        self.rhs = {}
        self.g = {}
        self.open_set = []
        self.visited_order = []
        self._initialize()

    def _h(self, a, b):
        return abs(a.row - b.row) + abs(a.col - b.col)

    def _key(self, node):
        g_rhs = min(self.g.get(node, math.inf), self.rhs.get(node, math.inf))
        return (g_rhs + self._h(self.start, node) + self.k_m,
                g_rhs)

    def _initialize(self):
        for row in self.grid.cells:
            for cell in row:
                self.rhs[cell] = math.inf
                self.g[cell] = math.inf
        self.rhs[self.goal] = 0
        heapq.heappush(self.open_set, (self._key(self.goal), id(self.goal), self.goal))

    def _update_vertex(self, node):
        if node != self.goal:
            best = math.inf
            for nb in self.grid.get_neighbors(node):
                val = self.g.get(nb, math.inf) + nb.cost
                if val < best:
                    best = val
            self.rhs[node] = best

        self.open_set = [(k, i, n) for k, i, n in self.open_set if n != node]
        heapq.heapify(self.open_set)

        if self.g.get(node, math.inf) != self.rhs.get(node, math.inf):
            heapq.heappush(self.open_set, (self._key(node), id(node), node))

    def compute_shortest_path(self):
        while self.open_set:
            k_old, _, u = heapq.heappop(self.open_set)
            self.visited_order.append(u)

            if k_old >= self._key(self.start) and \
               self.rhs.get(self.start, math.inf) == self.g.get(self.start, math.inf):
                break

            if self.g.get(u, math.inf) > self.rhs.get(u, math.inf):
                self.g[u] = self.rhs[u]
                for nb in self.grid.get_neighbors(u):
                    self._update_vertex(nb)
            else:
                self.g[u] = math.inf
                self._update_vertex(u)
                for nb in self.grid.get_neighbors(u):
                    self._update_vertex(nb)

    def extract_path(self):
        path = []
        current = self.start
        visited = set()
        while current != self.goal:
            if current in visited:
                return []
            visited.add(current)
            path.append(current)
            neighbors = self.grid.get_neighbors(current)
            if not neighbors:
                return []
            current = min(neighbors, key=lambda n: self.g.get(n, math.inf))
        path.append(self.goal)
        return path

    def update_obstacle(self, cell):
        """Call this when a new obstacle is added mid-search."""
        self.k_m += self._h(self.start, cell)
        self.start = self.grid.start
        cell.set_terrain("obstacle")
        self._update_vertex(cell)
        for nb in self.grid.get_neighbors(cell):
            self._update_vertex(nb)

    def run(self):
        self.compute_shortest_path()
        path = self.extract_path()
        return path, self.visited_order