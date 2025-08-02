from config import THEMES, GameSettings

class GameState:
    def __init__(self):
        self.score = 0
        self.stars_collected = 0
        self.total_stars = 0
        self.current_level = 0
        self.current_theme = "forest"
        self.camera_on = False
        self.help_on = False
        self.game_running = True
        self.game_won = False
        
    def add_score(self, points):
        self.score += points
        
    def collect_star(self):
        self.stars_collected += 1
        self.add_score(GameSettings.STAR_POINTS)
        
    def complete_level(self):
        self.add_score(GameSettings.LEVEL_COMPLETE_POINTS)
        self.current_level += 1
        self.stars_collected = 0  # Reset stars for new level
        
    def change_theme(self, theme_name):
        if theme_name in THEMES:
            self.current_theme = theme_name
            return True
        return False
    
    def get_current_theme(self):
        return THEMES[self.current_theme]
    
    def toggle_camera(self):
        self.camera_on = not self.camera_on
        return self.camera_on
    
    def toggle_help(self):
        self.help_on = not self.help_on
        return self.help_on
    
    def set_total_stars(self, count):
        self.total_stars = count
        
    def get_stars_progress(self):
        return f"{self.stars_collected}/{self.total_stars}"
    
    def is_level_complete_stars(self):
        return self.stars_collected >= self.total_stars
    
    def reset_for_new_level(self, total_stars):
        self.stars_collected = 0
        self.total_stars = total_stars
        
    def quit_game(self):
        self.game_running = False
        
    def win_game(self):
        self.game_won = True
        self.game_running = False