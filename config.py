import os

# Display Settings
TILE_SIZE = 80
GRID_WIDTH = 6
GRID_HEIGHT = 8
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
    BG_COLOR = (20, 25, 35)

# Game Settings
class GameSettings:
    FPS = 30
    MOVE_DELAY = 0.2
    STAR_POINTS = 10
    LEVEL_COMPLETE_POINTS = 50


THEMES = {
    "forest": {
        "wall": (34, 139, 34),
        "path": (144, 238, 144),
        "start": (0, 100, 0),
        "goal": (255, 215, 0),
        "bg": (0, 50, 0),
        "name": "Forest"
    },
    "space": {
        "wall": (25, 25, 112),
        "path": (72, 61, 139),
        "start": (0, 191, 255),
        "goal": (255, 20, 147),
        "bg": (0, 0, 0),
        "name": "Space"
    },
    "desert": {
        "wall": (160, 82, 45),
        "path": (255, 218, 185),
        "start": (255, 140, 0),
        "goal": (255, 215, 0),
        "bg": (139, 69, 19),
        "name": "Desert"
    },
    "ocean": {
        "wall": (0, 105, 148),
        "path": (173, 216, 230),
        "start": (0, 191, 255),
        "goal": (255, 215, 0),
        "bg": (0, 0, 139),
        "name": "Ocean"
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