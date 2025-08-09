import os

# Display Settings
TILE_SIZE = 80
GRID_WIDTH = 10
GRID_HEIGHT = 9
WIDTH = GRID_WIDTH * TILE_SIZE
HEIGHT = GRID_HEIGHT * TILE_SIZE

# Colors
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 120, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    ACCENT_COLOR = (0, 200, 150)
    HOVER_COLOR = (255, 180, 0)
    TEXT_COLOR = (230, 230, 230)
    BG_COLOR = (20, 25, 100)

# Game Settings
class GameSettings:
    FPS = 30
    MOVE_DELAY = 0.2
    STAR_POINTS = 10
    LEVEL_COMPLETE_POINTS = 50

THEMES = {

    "space": {
        "wall": (15, 15, 67),
        "path": (43, 37, 84),
        "start": (0, 115, 153),
        "goal": (153, 12, 88),
        "bg": (15, 15, 67),
        "name": "Space"
    },

    "volcano": {
        "wall": (84, 0, 0),
        "path": (153, 59, 43),
        "start": (153, 41, 0),
        "goal": (153, 129, 0),
        "bg": (84, 0, 0),
        "name": "Volcano"
    },

    "candyland": {
        "wall": (153, 63, 108),
        "path": (153, 109, 116),
        "start": (153, 12, 88),
        "goal": (0, 77, 153),
        "bg": (153, 63, 108),
        "name": "Candyland"
    },

    "winter": {
        "wall": (81, 124, 150),
        "path": (144, 149, 153),
        "start": (0, 77, 153),
        "goal": (0, 77, 153),
        "bg": (81, 124, 150),
        "name": "Winter"
    },

    "desert": {
        "wall": (96, 49, 27),
        "path": (153, 131, 111),
        "start": (153, 84, 0),
        "goal": (153, 129, 0),
        "bg": (96, 49, 27),
        "name": "Desert"
    },

    "forest": {
        "wall": (20, 84, 20),
        "path": (86, 143, 86),
        "start": (0, 60, 0),
        "goal": (153, 129, 0),
        "bg": (20, 84, 20),
        "name": "Forest"
    },

    "ocean": {
        "wall": (0, 63, 89),
        "path": (104, 130, 138),
        "start": (0, 115, 153),
        "goal": (153, 129, 0),
        "bg": (0, 63, 89),
        "name": "Ocean"
    },

    "city": {
        "wall": (30, 30, 30),
        "path": (101, 101, 101),
        "start": (0, 77, 77),
        "goal": (153, 129, 0),
        "bg": (30, 30, 30),
        "name": "City"
    }
}


# File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CHARACTERS_DIR = os.path.join(ASSETS_DIR, "characters")
THEMES_DIR = os.path.join(ASSETS_DIR, "themes")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
MAZE_FILE = os.path.join(BASE_DIR, "mazes.txt")

# Hand Gesture Settings
class HandGestureSettings:
    POSITION_HISTORY_SIZE = 5
    MOVEMENT_THRESHOLD = 60
    DIRECTION_HOLD_TIME = 0.3
    CENTER_ZONE = 50
    MIN_DETECTION_CONFIDENCE = 0.7
    MIN_TRACKING_CONFIDENCE = 0.7

# Camera Settings
class CameraSettings:
    WIDTH = 640
    HEIGHT = 480
    FPS = 30
    PREVIEW_WIDTH = 200
    PREVIEW_HEIGHT = 150

# Maze Tile Types
class TileType:
    WALL = 0
    PATH = 1
    START = 2
    GOAL = 3
    STAR = 4