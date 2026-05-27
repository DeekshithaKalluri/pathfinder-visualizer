import pygame
import sys
from grid import Grid
from renderer import Renderer, CELL_SIZE
from algorithms.astar import astar
from algorithms.dijkstra import dijkstra
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dstar_lite import DStarLite
from profiler.profiler import Profiler

# === INIT ===
pygame.init()
grid = Grid(25, 25)
grid.set_start(2, 2)
grid.set_end(22, 22)
renderer = Renderer(grid)
profiler  = Profiler()
clock = pygame.time.Clock()

# === STATE ===
algorithm_name = "A*"
visited_cells  = set()
path_cells     = []
profile_result = None
mode           = "draw"        # "draw" or "running"
terrain_brush  = "obstacle"    # cycles: obstacle → mud → highway → normal
config_name    = "Default"
dstar          = None          # holds DStarLite instance across dynamic updates

TERRAIN_CYCLE = ["obstacle", "mud", "highway", "normal"]

PANEL_X = grid.cols * CELL_SIZE


def get_cell_from_mouse(pos):
    x, y = pos
    if x >= PANEL_X:
        return None
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    return grid.get(row, col)


def run_algorithm():
    global visited_cells, path_cells, profile_result, dstar

    profiler.start()

    if algorithm_name == "A*":
        path, visited = astar(grid)
    elif algorithm_name == "Dijkstra":
        path, visited = dijkstra(grid)
    elif algorithm_name == "BFS":
        path, visited = bfs(grid)
    elif algorithm_name == "DFS":
        path, visited = dfs(grid)
    elif algorithm_name == "D* Lite":
        dstar = DStarLite(grid)
        path, visited = dstar.run()
    else:
        path, visited = [], []

    profile_result = profiler.stop(algorithm_name, len(visited))
    profiler.print_last()

    visited_cells = set(visited)
    path_cells    = path


def load_config(name):
    global config_name, visited_cells, path_cells, profile_result, dstar
    paths = {
        "Default": "configs/default.json",
        "Maze":    "configs/maze.json",
        "Highway": "configs/highway.json",
    }
    grid.load_config(paths[name])
    renderer.grid = grid
    config_name   = name
    visited_cells = set()
    path_cells    = []
    profile_result = None
    dstar = None


# === MAIN LOOP ===
running = True
while running:
    clock.tick(60)
    renderer.clear()
    renderer.draw_grid(visited=visited_cells, path=path_cells)
    renderer.draw_panel(
        profile_data=profile_result,
        algorithm=algorithm_name,
        mode=mode,
        terrain_brush=terrain_brush,
        config_name=config_name
    )
    renderer.flip()

    for event in pygame.event.get():

        # --- QUIT ---
        if event.type == pygame.QUIT:
            running = False

        # --- MOUSE: paint terrain ---
        if event.type == pygame.MOUSEBUTTONDOWN or \
           (event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]):
            cell = get_cell_from_mouse(pygame.mouse.get_pos())
            if cell and not cell.is_start and not cell.is_end:
                cell.set_terrain(terrain_brush)
                visited_cells = set()
                path_cells    = []

        # --- KEYBOARD ---
        if event.type == pygame.KEYDOWN:

            # Algorithm select
            if event.key == pygame.K_1:
                algorithm_name = "A*"
            elif event.key == pygame.K_2:
                algorithm_name = "Dijkstra"
            elif event.key == pygame.K_3:
                algorithm_name = "BFS"
            elif event.key == pygame.K_4:
                algorithm_name = "DFS"
            elif event.key == pygame.K_5:
                algorithm_name = "D* Lite"

            # Run
            elif event.key == pygame.K_SPACE:
                run_algorithm()

            # Reset
            elif event.key == pygame.K_r:
                grid.reset_grid()
                grid.set_start(2, 2)
                grid.set_end(22, 22)
                visited_cells  = set()
                path_cells     = []
                profile_result = None
                dstar = None

            # Cycle terrain brush
            elif event.key == pygame.K_t:
                idx = TERRAIN_CYCLE.index(terrain_brush)
                terrain_brush = TERRAIN_CYCLE[(idx + 1) % len(TERRAIN_CYCLE)]

            # Dynamic obstacle (D* Lite replanning)
            elif event.key == pygame.K_d:
                if dstar and path_cells and len(path_cells) > 2:
                    # Block the middle of the current path
                    mid = path_cells[len(path_cells) // 2]
                    dstar.update_obstacle(mid)
                    dstar.compute_shortest_path()
                    new_path    = dstar.extract_path()
                    path_cells  = new_path
                    visited_cells = set(dstar.visited_order)
                    profile_result = profiler.stop(
                        "D* Lite (replan)", len(dstar.visited_order))
                    profiler.print_last()
                else:
                    print("Run D* Lite first (press 5, then SPACE), then press D.")

            # Load configs
            elif event.key == pygame.K_l:
                pass  # placeholder: handled below with number combos

            # L + 1/2/3 = load preset (use F1/F2/F3 for simplicity)
            elif event.key == pygame.K_F1:
                load_config("Default")
            elif event.key == pygame.K_F2:
                load_config("Maze")
            elif event.key == pygame.K_F3:
                load_config("Highway")

            # Print full benchmark report
            elif event.key == pygame.K_p:
                profiler.print_all()

pygame.quit()
sys.exit()