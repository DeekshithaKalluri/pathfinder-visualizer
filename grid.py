import json
import random

# === TERRAIN TYPES AND THEIR MOVEMENT COSTS ===
TERRAIN_COSTS = {
    "normal":   1,
    "mud":      5,
    "highway":  0.5,
    "obstacle": float('inf')
}

TERRAIN_COLORS = {
    "normal":   (200, 200, 200),
    "mud":      (139, 90,  43),
    "highway":  (255, 223, 0),
    "obstacle": (30,  30,  30)
}


class Cell:
    def __init__(self, row, col, terrain="normal"):
        self.row = row
        self.col = col
        self.terrain = terrain
        self.cost = TERRAIN_COSTS[terrain]
        self.is_start = False
        self.is_end = False

    def set_terrain(self, terrain):
        self.terrain = terrain
        self.cost = TERRAIN_COSTS[terrain]

    def is_walkable(self):
        return self.terrain != "obstacle"


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.start = None
        self.end = None

    def get(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    def set_start(self, row, col):
        if self.start:
            self.start.is_start = False
        self.start = self.cells[row][col]
        self.start.is_start = True

    def set_end(self, row, col):
        if self.end:
            self.end.is_end = False
        self.end = self.cells[row][col]
        self.end.is_end = True

    def set_terrain(self, row, col, terrain):
        self.cells[row][col].set_terrain(terrain)

    def get_neighbors(self, cell):
        neighbors = []
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        for dr, dc in directions:
            neighbor = self.get(cell.row + dr, cell.col + dc)
            if neighbor and neighbor.is_walkable():
                neighbors.append(neighbor)
        return neighbors

    def reset_grid(self):
        for row in self.cells:
            for cell in row:
                cell.set_terrain("normal")
        self.start = None
        self.end = None

    def load_config(self, filepath):
        with open(filepath) as f:
            config = json.load(f)

        self.rows = config["rows"]
        self.cols = config["cols"]
        self.cells = [[Cell(r, c) for c in range(self.cols)] for r in range(self.rows)]

        self.set_start(*config["start"])
        self.set_end(*config["end"])

        terrain = config.get("terrain", {})

        # Build maze walls with gaps
        if "wall_rows" in terrain:
            for i, wall_row in enumerate(terrain["wall_rows"]):
                gap = terrain["gap_cols"][i]
                for col in range(self.cols):
                    if col != gap:
                        self.set_terrain(wall_row, col, "obstacle")

        # Build highway lanes
        for hr in terrain.get("highway_rows", []):
            for col in range(self.cols):
                self.set_terrain(hr, col, "highway")

        # Build mud regions [r1, c1, r2, c2]
        for region in terrain.get("mud_regions", []):
            r1, c1, r2, c2 = region
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    self.set_terrain(r, c, "mud")