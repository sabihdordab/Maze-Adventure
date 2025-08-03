import pygame
import sys
from config import *
from game.game_state import GameState
from game.maze import MazeLoader
from game.player import Player
from game.ui import UI, CharacterSelection
from assets.asset_manager import AssetManager
from controllers.hand_controller import HandGestureController, CameraManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Adventure")
        
        self.asset_manager = AssetManager()
        self.game_state = GameState()
        self.ui = UI(self.screen, self.asset_manager)
        self.character_selection = CharacterSelection(self.screen, self.asset_manager)
        self.hand_controller = HandGestureController()
        self.camera_manager = CameraManager()
        
        self.asset_manager.load_all_assets()
        
        self.mazes = []
        self.current_maze = None
        self.player = None
        self.selected_character = None
        
        self.clock = pygame.time.Clock()
        self.current_camera_frame = None 
        
    def initialize_game(self):
        self.selected_character = self.character_selection.show_selection()
        if not self.selected_character:
            self.selected_character = self.asset_manager.get_character()
        
        self.mazes = MazeLoader.load_mazes_from_file()
        if not self.mazes:
            print("No mazes loaded!")
            return False
        
        self.start_level(0)
        return True
    
    def start_level(self, level_index):
        if level_index >= len(self.mazes):
            self.game_state.win_game()
            return
        
        self.current_maze = self.mazes[level_index]
        self.game_state.current_level = level_index
        
        start_x, start_y = self.current_maze.get_start_position()
        self.player = Player(start_x, start_y)
        
        total_stars = self.current_maze.get_total_stars_count()
        self.game_state.reset_for_new_level(total_stars)
        
        themes_list = list(THEMES.keys())
        new_theme = themes_list[level_index % len(themes_list)]
        self.game_state.change_theme(new_theme)
        self.asset_manager.play_theme_music(new_theme)
        self.current_maze.generate_item_positions(new_theme, self.asset_manager)
        print(f"Level {level_index + 1} started! Theme: {THEMES[new_theme]['name']}")
    
    def handle_input(self):
        dx, dy = 0, 0
        
        if self.game_state.camera_on:
            frame = self.camera_manager.get_frame()
            if frame is not None:
                processed_frame, results = self.hand_controller.process_frame(frame)
                self.current_camera_frame = processed_frame
                dx, dy = self.hand_controller.get_direction(results, frame.shape[1], frame.shape[0])
            else:
                self.current_camera_frame = None
        else:
            self.current_camera_frame = None
        
        # Keyboard input (overrides hand gesture)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        elif keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1
        
        return dx, dy
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.cleanup()
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game_state.help_on = False
                elif event.key == pygame.K_ESCAPE:
                    self.cleanup()
                    return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_state.help_on:
                    self.handle_mouse_click(pygame.mouse.get_pos())
        
        return True
    
    def handle_mouse_click(self, mouse_pos):
        cam_rect, exit_rect, help_rect = self.get_ui_rects()
        
        if cam_rect.collidepoint(mouse_pos):
            # Toggle camera
            if self.game_state.camera_on:
                self.camera_manager.stop_camera()
                self.game_state.camera_on = False
            else:
                if self.camera_manager.start_camera():
                    self.game_state.camera_on = True
                    
        elif exit_rect.collidepoint(mouse_pos):
            self.cleanup()
            self.game_state.quit_game()
            
        elif help_rect.collidepoint(mouse_pos):
            self.game_state.toggle_help()
    
    def get_ui_rects(self):
        camera_pos = (10, HEIGHT-130)
        exit_pos = (70, HEIGHT-130)
        help_pos = (140, HEIGHT-130)
        
        return (
            pygame.Rect(*camera_pos, 50, 50),
            pygame.Rect(*exit_pos, 50, 50),
            pygame.Rect(*help_pos, 50, 50)
        )
    
    def update_game_logic(self):
        if self.game_state.help_on:
            return
        
        dx, dy = self.handle_input()
        
        if (dx != 0 or dy != 0):
            if self.player.try_move(dx, dy, self.current_maze, GameSettings.MOVE_DELAY):
                if self.player.collect_star_at_position(self.current_maze):
                    self.game_state.collect_star()
                    self.asset_manager.play_sound('star_collect')
                    print(f"Star collected! Total: {self.game_state.stars_collected}")
                
                if self.player.is_at_goal(self.current_maze):
                    self.complete_level()
    
    def update_camera_preview(self):
        if self.game_state.camera_on:
            frame = self.camera_manager.get_frame()
            if frame is not None:
                processed_frame, _ = self.hand_controller.process_frame(frame)
                self.ui.draw_camera_preview(processed_frame)
    
    def complete_level(self):
        print(f"Level {self.game_state.current_level + 1} completed! Score: {self.game_state.score}")
        
        self.game_state.complete_level()
        self.asset_manager.play_sound('done')
        
        next_level = self.game_state.current_level
        if next_level < len(self.mazes):
            pygame.time.delay(500)  #
            self.start_level(next_level)
        else:
            self.game_state.win_game()
    
    def render(self):
        if self.game_state.help_on:
            self.ui.draw_help_screen()
        else:
            theme = self.game_state.get_current_theme()
            self.screen.fill(theme["bg"])
            
            self.ui.draw_maze(self.current_maze, theme, self.game_state.current_theme)
            
            self.ui.draw_player(self.player, self.selected_character)
            
            self.ui.draw_game_ui(self.game_state)
            self.ui.draw_icons(self.game_state)
            
            if self.game_state.camera_on and hasattr(self, 'current_camera_frame') and self.current_camera_frame is not None:
                self.ui.draw_camera_preview(self.current_camera_frame)
    
    def run(self):
        if not self.initialize_game():
            print("Failed to initialize game!")
            return
        
        while self.game_state.game_running:
            if not self.handle_events():
                break
            
            self.update_game_logic()
            
            self.render()
            
            pygame.display.update()
            self.clock.tick(GameSettings.FPS)
        
        if self.game_state.game_won:
            self.ui.show_game_over(self.game_state.score)
        
        self.cleanup()
    
    def cleanup(self):
        self.camera_manager.stop_camera()
        self.hand_controller.close()
        pygame.quit()