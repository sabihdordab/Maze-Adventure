from config import TileType, MAZE_FILE
import random
class Maze:
    def __init__(self, maze_data):
        self.data = maze_data
        self.item_positions = {}
        self.stars_positions = self._find_stars()
        
    def _find_stars(self):
        stars = []
        for y, row in enumerate(self.data):
            for x, tile in enumerate(row):
                if tile == TileType.STAR:
                    stars.append((x, y))
        return stars
    
    def get_start_position(self):
        for y, row in enumerate(self.data):
            for x, tile in enumerate(row):
                if tile == TileType.START:
                    return x, y
        return 1, 1  # Default fallback
    
    def can_move_to(self, x, y):
        if not (0 <= x < len(self.data[0]) and 0 <= y < len(self.data)):
            return False
        
        tile_type = self.data[y][x]
        return tile_type in [TileType.PATH, TileType.GOAL, TileType.STAR]
    
    def get_tile_type(self, x, y):
        if 0 <= x < len(self.data[0]) and 0 <= y < len(self.data):
            return self.data[y][x]
        return TileType.WALL
    
    def collect_star(self, x, y):
        if (x, y) in self.stars_positions:
            self.stars_positions.remove((x, y))
            return True
        return False
    
    def has_star_at(self, x, y):
        return (x, y) in self.stars_positions
    
    def get_stars_count(self):
        return len(self.stars_positions)
    
    def get_total_stars_count(self):
        count = 0
        for row in self.data:
            for tile in row:
                if tile == TileType.STAR:
                    count += 1
        return count
    
    def is_goal_position(self, x, y):
        return self.get_tile_type(x, y) == TileType.GOAL
    
    def get_width(self):
        return len(self.data[0]) if self.data else 0
    
    def get_height(self):
        return len(self.data)

    def generate_item_positions(self, theme_name, asset_manager):
        items = asset_manager.get_theme_assets(theme_name)['items']
        if not items:
            return
        
        for y, row in enumerate(self.data):
            for x, tile in enumerate(row):
                if tile == TileType.WALL and random.random() < 0.1: 
                    if (x, y) not in self.item_positions:
                        self.item_positions[(x, y)] = random.choice(items)

class MazeLoader:
    @staticmethod
    def load_mazes_from_file(filename=MAZE_FILE):
        mazes = []
        current_maze = []
        
        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#"):
                        if current_maze:
                            mazes.append(Maze(current_maze))
                        current_maze = []
                    elif line:
                        current_maze.append(list(map(int, line.split())))
                
                if current_maze:
                    mazes.append(Maze(current_maze))
                    
        except FileNotFoundError:
            sample_maze_data = [
                [0, 0, 0, 0, 0, 0],
                [0, 2, 1, 4, 1, 0],
                [0, 1, 0, 0, 1, 0],
                [0, 4, 1, 0, 4, 0],
                [0, 0, 1, 0, 1, 0],
                [0, 1, 1, 1, 3, 0],
                [0, 0, 0, 0, 0, 0]
            ]
            mazes = [Maze(sample_maze_data)]
            
        return mazes
    
    @staticmethod
    def get_sample_maze():
        sample_data = [
            [0, 0, 0, 0, 0, 0],
            [0, 2, 1, 4, 1, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 4, 1, 0, 4, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 3, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        return Maze(sample_data)