import time

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last_move_time = 0
        
    def set_position(self, x, y):
        self.x = x
        self.y = y
        
    def get_position(self):
        return self.x, self.y
        
    def can_move(self, move_delay=0.2):
        current_time = time.time()
        return current_time - self.last_move_time > move_delay
        
    def try_move(self, dx, dy, maze, move_delay=0.2):
        if not self.can_move(move_delay):
            return False
            
        new_x = self.x + dx
        new_y = self.y + dy
        
        if maze.can_move_to(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.last_move_time = time.time()
            return True
            
        return False
        
    def is_at_goal(self, maze):
        return maze.is_goal_position(self.x, self.y)
        
    def collect_star_at_position(self, maze):
        return maze.collect_star(self.x, self.y)