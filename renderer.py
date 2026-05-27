import pygame
from grid import TERRAIN_COLORS

# Color constants
WHITE       = (255, 255, 255)
BLACK       = (0,   0,   0)
GREEN       = (0,   200, 0)
RED         = (200, 0,   0)
BLUE        = (0,   100, 255)
LIGHT_BLUE  = (173, 216, 230)
ORANGE      = (255, 140, 0)
PURPLE      = (148, 0,   211)
DARK_GRAY   = (50,  50,  50)
PANEL_COLOR = (20,  20,  40)
TEXT_COLOR  = (220, 220, 220)

CELL_SIZE   = 24
PANEL_WIDTH = 280


class Renderer:
    def __init__(self, grid):
        self.grid = grid
        self.width  = grid.cols * CELL_SIZE + PANEL_WIDTH
        self.height = grid.rows * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Adaptive Pathfinder Visualizer")
        self.font       = pygame.font.SysFont("monospace", 13)
        self.font_large = pygame.font.SysFont("monospace", 15, bold=True)

    def draw_grid(self, visited=None, path=None):
        visited = visited or set()
        path    = path    or []
        path_set = set(path)

        for row in self.grid.cells:
            for cell in row:
                x = cell.col * CELL_SIZE
                y = cell.row * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE - 1, CELL_SIZE - 1)

                if cell.is_start:
                    color = GREEN
                elif cell.is_end:
                    color = RED
                elif cell in path_set:
                    color = ORANGE
                elif cell in visited:
                    color = LIGHT_BLUE
                else:
                    color = TERRAIN_COLORS.get(cell.terrain, WHITE)

                pygame.draw.rect(self.screen, color, rect)

    def draw_panel(self, profile_data=None, algorithm="None", mode="draw",
                   terrain_brush="obstacle", config_name="Default"):
        panel_x = self.grid.cols * CELL_SIZE
        pygame.draw.rect(self.screen, PANEL_COLOR,
                         pygame.Rect(panel_x, 0, PANEL_WIDTH, self.height))

        lines = [
            "=== PATHFINDER ===",
            "",
            f"Config   : {config_name}",
            f"Algorithm: {algorithm}",
            f"Mode     : {mode}",
            f"Brush    : {terrain_brush}",
            "",
            "--- CONTROLS ---",
            "1: A*        2: Dijkstra",
            "3: BFS       4: DFS",
            "5: D* Lite",
            "",
            "SPACE: Run algorithm",
            "R    : Reset grid",
            "D    : Dynamic obstacle",
            "",
            "T    : Cycle terrain brush",
            "Click: Paint terrain/walls",
            "",
            "L1: Load Default",
            "L2: Load Maze",
            "L3: Load Highway",
            "",
            "P    : Print full report",
            "",
            "--- LAST PROFILE ---",
        ]

        y = 10
        for line in lines:
            surf = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(surf, (panel_x + 8, y))
            y += 17

        if profile_data:
            stats = [
                f"Algo  : {profile_data['algorithm']}",
                f"Nodes : {profile_data['nodes_visited']}",
                f"Time  : {profile_data['time_ms']} ms",
                f"Mem   : {profile_data['memory_kb']} KB",
            ]
            for s in stats:
                surf = self.font.render(s, True, (100, 255, 100))
                self.screen.blit(surf, (panel_x + 8, y))
                y += 17

    def clear(self):
        self.screen.fill(BLACK)

    def flip(self):
        pygame.display.flip()