import pygame
import math
import cv2
import random
import sys
from config import *

class UI:
    def __init__(self, screen, asset_manager):
        self.screen = screen
        self.asset_manager = asset_manager
        self.font_small = pygame.font.SysFont("arial", 16)
        self.font_medium = pygame.font.SysFont("arial", 20)
        self.font_large = pygame.font.SysFont("arial", 32)
        self.font_xlarge = pygame.font.SysFont("arial", 64, bold=True)
        
    def draw_gradient_background(self, color):
        for y in range(HEIGHT):
            factor = y / HEIGHT
            r = int(color[0] + factor * 10)
            g = int(color[1] + factor * 15)
            b = int(color[2] + factor * 20)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
    
    def draw_maze(self, maze, theme, theme_name):
        for y, row in enumerate(maze.data):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if tile == TileType.WALL:
                    pygame.draw.rect(self.screen, theme["wall"], rect)
                    if (x, y) in maze.item_positions:
                        item = maze.item_positions[(x, y)]
                        item_rect = item.get_rect()
                        item_rect.center = rect.center
                        self.screen.blit(item, item_rect)
                elif tile == TileType.PATH:
                    pygame.draw.rect(self.screen, theme["path"], rect)
                elif tile == TileType.START:
                    pygame.draw.rect(self.screen, theme["start"], rect)
                elif tile == TileType.GOAL:
                    pygame.draw.rect(self.screen, theme["goal"], rect)
                elif tile == TileType.STAR:
                    pygame.draw.rect(self.screen, theme["path"], rect)
                    if maze.has_star_at(x, y):
                        star_img = self.asset_manager.get_theme_assets(theme_name)['star']
                        scale_factor = 0.5 + 0.1 * math.sin(pygame.time.get_ticks() * 0.01)
                        star_img = pygame.transform.scale(star_img, (int(TILE_SIZE * scale_factor), int(TILE_SIZE * scale_factor)))
                        star_rect = star_img.get_rect()
                        star_rect.center = (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2)
                        self.screen.blit(star_img, star_rect)

        fog_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(fog_surface, (200, 200, 200, 50), (WIDTH//2, HEIGHT//2), 300)
        self.screen.blit(fog_surface, (0, 0))

    
    def draw_player(self, player, character_img):
        x, y = player.get_position()
        if character_img:
            img_rect = character_img.get_rect()
            img_rect.center = (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2)
            self.screen.blit(character_img, img_rect)
        else:
            center = (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2)
            pygame.draw.circle(self.screen, Colors.RED, center, TILE_SIZE//3)
    
    def draw_game_ui(self, game_state):
        status_text = "Camera: ON" if game_state.camera_on else "Camera: OFF"
        status_color = Colors.GREEN if game_state.camera_on else Colors.RED
        self.screen.blit(self.font_medium.render(status_text, True, status_color), (10, 10))
        
        level_text = f"Level: {game_state.current_level + 1}"
        self.screen.blit(self.font_medium.render(level_text, True, Colors.WHITE), (10, 40))
        
        theme_text = f"Theme: {THEMES[game_state.current_theme]['name']}"
        self.screen.blit(self.font_medium.render(theme_text, True, Colors.WHITE), (10, 70))
        
        score_text = f"Score: {game_state.score}"
        self.screen.blit(self.font_medium.render(score_text, True, Colors.WHITE), (WIDTH - 150, 10))
        
        stars_text = f"Stars: {game_state.get_stars_progress()}"
        self.screen.blit(self.font_medium.render(stars_text, True, Colors.WHITE), (WIDTH - 150, 40))
    
    def draw_icons(self, game_state):
        camera_pos = (10, HEIGHT-130)
        exit_pos = (70, HEIGHT-130)
        help_pos = (140, HEIGHT-130)
        
        camera_img = self.asset_manager.get_ui_image('camera')
        self.screen.blit(camera_img, camera_pos)
        cam_rect = pygame.Rect(*camera_pos, 50, 50)
        
        if not game_state.camera_on:
            pygame.draw.line(self.screen, Colors.RED, camera_pos, 
                           (camera_pos[0]+50, camera_pos[1]+50), 4)
            pygame.draw.line(self.screen, Colors.RED, 
                           (camera_pos[0], camera_pos[1]+50), 
                           (camera_pos[0]+50, camera_pos[1]), 4)
        
        exit_img = self.asset_manager.get_ui_image('exit')
        self.screen.blit(exit_img, exit_pos)
        exit_rect = pygame.Rect(*exit_pos, 50, 50)
        
        help_img = self.asset_manager.get_ui_image('help')
        self.screen.blit(help_img, help_pos)
        help_rect = pygame.Rect(*help_pos, 50, 50)
        
        return cam_rect, exit_rect, help_rect
    
    def draw_camera_preview(self, frame):
        if frame is not None:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (CameraSettings.PREVIEW_WIDTH, CameraSettings.PREVIEW_HEIGHT))
            pygame_surface = pygame.surfarray.make_surface(frame_resized.swapaxes(0, 1))
            self.screen.blit(pygame_surface, (WIDTH - CameraSettings.PREVIEW_WIDTH, HEIGHT - CameraSettings.PREVIEW_HEIGHT))
    
    def draw_help_screen(self):
        for y in range(HEIGHT):
            color_ratio = y / HEIGHT
            r = int(240 - (color_ratio * 40))
            g = int(240 - (color_ratio * 60))
            b = int(255 - (color_ratio * 55))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
        
        main_rect = pygame.Rect(30, 30, WIDTH-60, HEIGHT-60)
        shadow_rect = pygame.Rect(35, 35, WIDTH-60, HEIGHT-60)
        
        pygame.draw.rect(self.screen, (100, 100, 100, 100), shadow_rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 255, 255, 230), main_rect, border_radius=15)
        pygame.draw.rect(self.screen, (70, 130, 180), main_rect, 3, border_radius=15)
        
        title_text = "Game Instructions"
        title_shadow = self.font_xlarge.render(title_text, True, (100, 100, 100))
        title_rect_shadow = title_shadow.get_rect(center=(WIDTH//2 + 2, 72))
        self.screen.blit(title_shadow, title_rect_shadow)
        
        title_surface = self.font_xlarge.render(title_text, True, (25, 25, 112))
        title_rect = title_surface.get_rect(center=(WIDTH//2, 70))
        self.screen.blit(title_surface, title_rect)
        
        pygame.draw.line(self.screen, (70, 130, 180), (60, 100), (WIDTH-60, 100), 3)
        
        sections = [
            {
                "title": "Camera Control:",
                "items": [
                    "• Use your index finger as a virtual joystick",
                    "• Move your finger to control the character", 
                    "• Stay in center zone to stop moving"
                ],
                "color": (0, 100, 0)
            },
            {
                "title": "Keyboard Control:",
                "items": ["• Use arrow keys to move"],
                "color": (139, 69, 19)
            },
            {
                "title": "Game Features:",
                "items": [
                    "Collect stars for +10 points each",
                    "Themes change every level",
                    "Each theme has unique background music",
                    "Complete levels to increase your score"
                ],
                "color": (128, 0, 128)
            }
        ]
        
        current_y = 130
        font_section = pygame.font.SysFont("arial", 20, bold=True)
        
        for section in sections:
            section_surface = font_section.render(section["title"], True, section["color"])
            self.screen.blit(section_surface, (70, current_y))
            current_y += 35
            
            for item in section["items"]:
                item_surface = self.font_small.render(item, True, (40, 40, 40))
                self.screen.blit(item_surface, (90, current_y))
                current_y += 22
            
            current_y += 10
        
        tips_rect = pygame.Rect(50, current_y, WIDTH-100, 80)
        pygame.draw.rect(self.screen, (255, 248, 220), tips_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 165, 0), tips_rect, 2, border_radius=10)
        
        tips_text = [
            "Pro Tips:",
            "• Collect all stars in a level for bonus points!",
            "• Each completed level gives +50 points"
        ]
        
        for i, tip in enumerate(tips_text):
            color = (255, 140, 0) if i == 0 else (60, 60, 60)
            weight = True if i == 0 else False
            tip_font = pygame.font.SysFont("arial", 15, bold=weight)
            tip_surface = tip_font.render(tip, True, color)
            self.screen.blit(tip_surface, (90, current_y + 12 + i*18))
        
        button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 80, 200, 40)
        mouse_pos = pygame.mouse.get_pos()
        
        if button_rect.collidepoint(mouse_pos):
            button_color = (100, 149, 237)
        else:
            button_color = (70, 130, 180)
        
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=20)
        pygame.draw.rect(self.screen, Colors.WHITE, button_rect, 2, border_radius=20)
        
        font_button = pygame.font.SysFont("arial", 18, bold=True)
        button_text = font_button.render("Press SPACE to return", True, Colors.WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)
    
    def show_game_over(self, final_score):
        particles = []
        
        for _ in range(30):
            particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-2, 0),
                'color': random.choice([(255, 215, 0), (255, 20, 147), (0, 191, 255)]),
                'size': random.randint(2, 4)
            })
        
        clock = pygame.time.Clock()
        
        for frame in range(180):
            self.screen.fill((0, 0, 50))
            
            for particle in particles:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += 0.1
                
                pygame.draw.circle(self.screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), 
                                 particle['size'])
                
                if particle['y'] > HEIGHT:
                    particle['y'] = 0
                    particle['x'] = random.randint(0, WIDTH)
            
            text_shadow = self.font_xlarge.render("YOU WON!", True, (50, 50, 50))
            self.screen.blit(text_shadow, (WIDTH//2 - text_shadow.get_width()//2 + 3, HEIGHT//2 - 80 + 3))
            
            text = self.font_xlarge.render("YOU WON!", True, (255, 215, 0))
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 80))
            
            score_text = self.font_large.render(f"Final Score: {final_score}", True, Colors.WHITE)
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))
            
            if frame > 120:
                continue_text = self.font_medium.render("Press any key to continue...", True, (200, 200, 200))
                self.screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 80))
            
            pygame.display.update()
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


class CharacterSelection:
    def __init__(self, screen, asset_manager):
        self.screen = screen
        self.asset_manager = asset_manager
        
    def calculate_positions(self, num_items):
        item_size = 100
        spacing = 135
        
        cols = min(num_items, 2)
        rows = math.ceil(num_items / cols)
        
        total_width = cols * spacing - (spacing - item_size)
        total_height = rows * spacing - (spacing - item_size)
        
        start_x = (WIDTH - total_width) // 2
        start_y = (HEIGHT - total_height) // 2 + 30
        
        positions = []
        for i in range(num_items):
            row = i // cols
            col = i % cols
            x = start_x + col * spacing
            y = start_y + row * spacing
            positions.append((x, y))
        
        return positions
    
    def draw_character_card(self, image, name, x, y, size, is_hovered):
        if is_hovered:
            scale = 1.1
            color = Colors.HOVER_COLOR
            float_offset = math.sin(pygame.time.get_ticks() * 0.008) * 5
        else:
            scale = 1.0
            color = Colors.ACCENT_COLOR
            float_offset = 0
        
        scaled_size = int(size * scale)
        draw_x = x + (size - scaled_size) // 2
        draw_y = y + (size - scaled_size) // 2 + float_offset
        
        bg_rect = pygame.Rect(draw_x - 10, draw_y - 10, scaled_size + 20, scaled_size + 20)
        pygame.draw.rect(self.screen, (240, 0, 65), bg_rect, border_radius=15)
        
        border_rect = pygame.Rect(draw_x - 5, draw_y - 5, scaled_size + 10, scaled_size + 10)
        pygame.draw.rect(self.screen, color, border_rect, 3, border_radius=10)
        
        scaled_image = pygame.transform.scale(image, (scaled_size, scaled_size))
        self.screen.blit(scaled_image, (draw_x, draw_y))
        
        # clean_name = name.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
        # font = pygame.font.SysFont("arial", 20)
        # name_surface = font.render(clean_name, True, Colors.TEXT_COLOR)
        # name_rect = name_surface.get_rect(center=(x + size//2, draw_y + scaled_size + 25))
        # self.screen.blit(name_surface, name_rect)
        
        return pygame.Rect(x, y, size, size)
    
    def draw_gradient_background(self):
        for y in range(HEIGHT):
            factor = y / HEIGHT
            r = int(Colors.BG_COLOR[0] + factor * 10)
            g = int(Colors.BG_COLOR[1] + factor * 15)
            b = int(Colors.BG_COLOR[2] + factor * 20)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
    
    def show_selection(self):
        characters = self.asset_manager.get_all_characters()
        if not characters:
            return None
        
        char_size = 100
        positions = self.calculate_positions(len(characters))
        
        selected_character = None
        running = True
        clock = pygame.time.Clock()
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, (img, name) in enumerate(characters):
                        x, y = positions[i]
                        rect = pygame.Rect(x, y, char_size, char_size)
                        if rect.collidepoint(mouse_pos):
                            selected_character = img
                            running = False
                            break
            
            self.draw_gradient_background()
            
            for i, (img, name) in enumerate(characters):
                x, y = positions[i]
                rect = pygame.Rect(x, y, char_size, char_size)
                is_hovered = rect.collidepoint(mouse_pos)
                self.draw_character_card(img, name, x, y, char_size, is_hovered)
            
            pygame.display.flip()
            clock.tick(60)
        
        return selected_character