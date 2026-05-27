# Adaptive Pathfinding Visualizer

A systems-level pathfinding benchmarking tool built with Python and Pygame.

## Features
- 5 algorithms: A*, Dijkstra, BFS, DFS, D* Lite
- Weighted terrain: mud, highway, obstacles
- Dynamic mid-search obstacle insertion with D* Lite replanning
- Performance profiler: nodes visited, time (ms), memory (KB)
- 3 grid presets: Default, Maze, Highway

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install pygame networkx psutil
python main.py
```

## Controls
| Key | Action |
|-----|--------|
| 1–5 | Select algorithm |
| SPACE | Run algorithm |
| T | Cycle terrain brush |
| Click/Drag | Paint terrain |
| R | Reset grid |
| D | Dynamic obstacle + D* Lite replan |
| F1/F2/F3 | Load preset config |
| P | Print benchmark report |

## Tech Stack
- Python, Pygame, NetworkX, psutil
- D* Lite for dynamic replanning
- JSON config system for grid presets