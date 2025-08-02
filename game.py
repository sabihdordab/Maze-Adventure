import pygame
import os
import cv2
import mediapipe as mp
import time
import random
import math
import sys

pygame.init()
pygame.mixer.init()

TILE_SIZE = 80
GRID_WIDTH = 6
GRID_HEIGHT = 8
WIDTH = GRID_WIDTH * TILE_SIZE
HEIGHT = GRID_HEIGHT * TILE_SIZE


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Adventure")

BLACK, WHITE, BLUE, GREEN, RED = (0,0,0), (255,255,255), (0,120,255), (0,255,0), (255,0,0)
ACCENT_COLOR = (0, 200, 150) 
HOVER_COLOR = (255, 180, 0)   
TEXT_COLOR = (230, 230, 230)
BG_COLOR = (20, 25, 35)

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CHARACTERS_DIR = os.path.join(ASSETS_DIR, "characters")
THEMES_DIR = os.path.join(ASSETS_DIR, "themes")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
MAZE_FILE = os.path.join(BASE_DIR, "mazes.txt")

current_theme = "forest"
score = 0
stars_collected = 0
total_stars = 0



def calculate_positions(num_items):
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


def draw_character_card(screen, image, name, x, y, size, is_hovered, font=pygame.font.SysFont("arial", 20)):
    if is_hovered:
        scale = 1.1
        color = HOVER_COLOR
        float_offset = math.sin(pygame.time.get_ticks() * 0.008) * 5
    else:
        scale = 1.0
        color = ACCENT_COLOR
        float_offset = 0
    
    scaled_size = int(size * scale)
    draw_x = x + (size - scaled_size) // 2
    draw_y = y + (size - scaled_size) // 2 + float_offset
    
    bg_rect = pygame.Rect(draw_x - 10, draw_y - 10, scaled_size + 20, scaled_size + 20)
    pygame.draw.rect(screen, (40, 50, 65), bg_rect, border_radius=15)
    
    border_rect = pygame.Rect(draw_x - 5, draw_y - 5, scaled_size + 10, scaled_size + 10)
    pygame.draw.rect(screen, color, border_rect, 3, border_radius=10)
    
    scaled_image = pygame.transform.scale(image, (scaled_size, scaled_size))
    screen.blit(scaled_image, (draw_x, draw_y))
    
    clean_name = name.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
    name_surface = font.render(clean_name, True, TEXT_COLOR)
    name_rect = name_surface.get_rect(center=(x + size//2, draw_y + scaled_size + 25))
    
    shadow_surface = font.render(clean_name, True, (0, 0, 0))
    # screen.blit(shadow_surface, (name_rect.x + 2, name_rect.y + 2))
    # screen.blit(name_surface, name_rect)
    
    return pygame.Rect(x, y, size, size)

def draw_gradient_background(screen):
    for y in range(HEIGHT):
        factor = y / HEIGHT
        r = int(BG_COLOR[0] + factor * 10)
        g = int(BG_COLOR[1] + factor * 15)
        b = int(BG_COLOR[2] + factor * 20)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def load_characters():
    characters = []
    folder = os.path.join(os.path.dirname(__file__), CHARACTERS_DIR)
    
    if not os.path.exists(folder):
        return characters
    
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                path = os.path.join(folder, filename)
                img = pygame.image.load(path).convert_alpha()
                characters.append((img, filename))
            except:
                pass
    
    return characters

def character_selection():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Character Selection")
    clock = pygame.time.Clock()
    
    
    characters = load_characters()
    if not characters:
        return None
    
    char_size = 100
    pixelated_characters = []
    for img, name in characters:
        scaled_img = pygame.transform.scale(img, (char_size, char_size))
        pixelated_characters.append((scaled_img, name))
    
    positions = calculate_positions(len(pixelated_characters))
    
    selected_character = None
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, (img, name) in enumerate(pixelated_characters):
                    x, y = positions[i]
                    rect = pygame.Rect(x, y, char_size, char_size)
                    if rect.collidepoint(mouse_pos):
                        selected_character = img
                        running = False
                        break
        
        draw_gradient_background(screen)
        
        for i, (img, name) in enumerate(pixelated_characters):
            x, y = positions[i]
            rect = pygame.Rect(x, y, char_size, char_size)
            is_hovered = rect.collidepoint(mouse_pos)
            
            draw_character_card(screen, img, name, x, y, char_size, is_hovered)
        
        pygame.display.flip()
        clock.tick(60)
    
    return selected_character

def load_random_character():
    try:
        if os.path.exists(CHARACTERS_DIR):
            character_files = [f for f in os.listdir(CHARACTERS_DIR) 
                             if f.lower().endswith('.png')]
            
            if character_files:
                selected_character = random.choice(character_files)
                character_path = os.path.join(CHARACTERS_DIR, selected_character)
                
                character_img = pygame.image.load(character_path)
                character_img = pygame.transform.scale(character_img, (TILE_SIZE-10, TILE_SIZE-10))
                
                print(f"Character loaded: {selected_character}")
                return character_img
            else:
                print("No PNG files found in characters directory")
                return None
        else:
            print("Characters directory not found")
            return None
    except Exception as e:
        print(f"Error loading character: {e}")
        return None

def load_theme_assets(theme_name):
    theme_path = os.path.join(THEMES_DIR, theme_name)
    assets = {}
    
    try:
        star_path = os.path.join(theme_path, "star.png")
        if os.path.exists(star_path):
            star_img = pygame.image.load(star_path)
            assets['star'] = pygame.transform.scale(star_img, (30, 30))
        else:
            star_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(star_surface, (255, 215, 0), (15, 15), 12)
            pygame.draw.circle(star_surface, (255, 255, 0), (15, 15), 8)
            assets['star'] = star_surface
        
        music_path = os.path.join(theme_path, "music.mp3")
        if os.path.exists(music_path):
            assets['music'] = music_path
        else:
            assets['music'] = None
            print(f"No music found for {theme_name} theme")
            
    except Exception as e:
        print(f"Error loading theme assets for {theme_name}: {e}")
        star_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(star_surface, (255, 215, 0), (15, 15), 12)
        assets['star'] = star_surface
        assets['music'] = None
    
    return assets

def change_theme(theme_name):
    global current_theme, theme_assets
    if theme_name in THEMES:
        current_theme = theme_name
        theme_assets = load_theme_assets(theme_name)
        if theme_assets['music']:
            try:
                pygame.mixer.music.load(theme_assets['music'])
                pygame.mixer.music.play(-1) 
                pygame.mixer.music.set_volume(0.3)
                print(f"Music loaded for {theme_name} theme")
            except Exception as e:
                print(f"Error loading music: {e}")

character_image = load_random_character()
theme_assets = load_theme_assets(current_theme)

try:
    star_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "star_collect.wav"))
    done_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "done.wav"))
    error_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "error.wav"))
except:
    star_sound = None
    done_sound = None
    error_sound = None

try:
    camera_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "camera.png")), (50, 50))
    exit_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "exit.png")), (50, 50))
    help_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "help.png")), (50, 50))
except:
    camera_img = pygame.Surface((50, 50))
    camera_img.fill(BLUE)
    exit_img = pygame.Surface((50, 50))
    exit_img.fill(RED)
    help_img = pygame.Surface((50, 60))
    help_img.fill(GREEN)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

class HandGestureController:
    def __init__(self):
        self.last_positions = []
        self.position_history_size = 5
        self.movement_threshold = 60
        self.last_direction = (0, 0)
        self.direction_hold_time = 0.3  
        self.last_direction_time = 0
        self.center_zone = 50
        
    def add_position(self, x, y):
        self.last_positions.append((x, y))
        if len(self.last_positions) > self.position_history_size:
            self.last_positions.pop(0)
    
    def get_smoothed_position(self):
        if not self.last_positions:
            return None
        
        avg_x = sum(pos[0] for pos in self.last_positions) / len(self.last_positions)
        avg_y = sum(pos[1] for pos in self.last_positions) / len(self.last_positions)
        return avg_x, avg_y
    
    def get_direction(self, results, frame_width, frame_height):
        if not results.multi_hand_landmarks:
            return 0, 0
        
        current_time = time.time()
        
        for hand_landmarks in results.multi_hand_landmarks:
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_tip.x * frame_width)
            y = int(index_tip.y * frame_height)
            
            self.add_position(x, y)
            
            smoothed_pos = self.get_smoothed_position()
            if not smoothed_pos:
                return 0, 0
            
            smooth_x, smooth_y = smoothed_pos
            
            center_x, center_y = frame_width // 2, frame_height // 2
            
            dx = smooth_x - center_x
            dy = smooth_y - center_y
            
            if abs(dx) < self.center_zone and abs(dy) < self.center_zone:
                return 0, 0
            
            new_direction = (0, 0)
            
            if abs(dx) > abs(dy): 
                if abs(dx) > self.movement_threshold:
                    new_direction = (1 if dx > 0 else -1, 0)
            else:
                if abs(dy) > self.movement_threshold:
                    new_direction = (0, 1 if dy > 0 else -1)
            
            if (new_direction != self.last_direction and 
                current_time - self.last_direction_time < self.direction_hold_time):
                return self.last_direction
            
            if new_direction != (0, 0):
                self.last_direction = new_direction
                self.last_direction_time = current_time
            
            return new_direction
        
        return 0, 0

def load_mazes_from_file(filename):
    mazes, current = [], []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    if current: 
                        mazes.append(current)
                    current = []
                elif line:
                    current.append(list(map(int, line.split())))
            if current: 
                mazes.append(current)
    except FileNotFoundError:
        sample_maze = [
            [0, 0, 0, 0, 0, 0],
            [0, 2, 1, 4, 1, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 4, 1, 0, 4, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 3, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        mazes = [sample_maze]
    return mazes

def find_start(maze):
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 2:
                return x, y
    return 1, 1 

def count_stars(maze):
    count = 0
    for row in maze:
        for tile in row:
            if tile == 4:  
                count += 1
    return count

def draw_maze(maze, stars_positions):
    theme = THEMES[current_theme]
    
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
            if tile == 0:  
                pygame.draw.rect(screen, theme["wall"], rect)
            elif tile == 1:  
                pygame.draw.rect(screen, theme["path"], rect)
            elif tile == 2:  
                pygame.draw.rect(screen, theme["start"], rect)
            elif tile == 3:  
                pygame.draw.rect(screen, theme["goal"], rect)
            elif tile == 4:  
                pygame.draw.rect(screen, theme["path"], rect)
                if (x, y) in stars_positions:
                    star_rect = theme_assets['star'].get_rect()
                    star_rect.center = (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2)
                    screen.blit(theme_assets['star'], star_rect)

def draw_player(x, y, character_img):
    if character_img:
        img_rect = character_img.get_rect()
        img_rect.center = (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2)
        screen.blit(character_img, img_rect)
    else:
        center = (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2)
        pygame.draw.circle(screen, RED, center, TILE_SIZE//3)

def draw_ui():
    font = pygame.font.SysFont("arial", 20)
    
    status_text = "Camera: ON" if camera_on else "Camera: OFF"
    status_color = GREEN if camera_on else RED
    screen.blit(font.render(status_text, True, status_color), (10, 10))
    
    level_text = f"Level: {maze_index + 1}"
    screen.blit(font.render(level_text, True, WHITE), (10, 40))
    
    theme_text = f"Theme: {THEMES[current_theme]['name']}"
    screen.blit(font.render(theme_text, True, WHITE), (10, 70))
    
    score_text = f"Score: {score}"
    screen.blit(font.render(score_text, True, WHITE), (WIDTH - 150, 10))
    
    stars_text = f"Stars: {stars_collected}/{total_stars}"
    screen.blit(font.render(stars_text, True, WHITE), (WIDTH - 150, 40))

def handle_input(keys):
    return (
        -1 if keys[pygame.K_LEFT] else 1 if keys[pygame.K_RIGHT] else 0,
        -1 if keys[pygame.K_UP] else 1 if keys[pygame.K_DOWN] else 0
    )

def can_move(maze, x, y):
    return 0 <= x < len(maze[0]) and 0 <= y < len(maze) and maze[y][x] in [1, 3, 4]

def collect_star(x, y, stars_positions):
    global score, stars_collected
    if (x, y) in stars_positions:
        stars_positions.remove((x, y))
        stars_collected += 1
        score += 10
        if star_sound:
            star_sound.play()
        print(f"Star collected! Total: {stars_collected}")

def next_maze(mazes, idx):
    global total_stars, stars_collected
    idx += 1
    if idx < len(mazes):
        # new_character = load_random_character()
        new_maze = mazes[idx]
        
        themes_list = list(THEMES.keys())
        new_theme = themes_list[idx % len(themes_list)]
        if new_theme != current_theme:
            change_theme(new_theme)
        
        total_stars = count_stars(new_maze)
        stars_collected = 0
        
        stars_pos = []
        for y, row in enumerate(new_maze):
            for x, tile in enumerate(row):
                if tile == 4:
                    stars_pos.append((x, y))
        
        return idx, new_maze, find_start(new_maze), stars_pos
    return None, None, (0, 0), None, []

def show_game_over():
    animation_time = 0
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
        screen.fill(THEMES[current_theme]["bg"])
        
        for particle in particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.1 
            
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
            
            if particle['y'] > HEIGHT:
                particle['y'] = 0
                particle['x'] = random.randint(0, WIDTH)
        
        
        font_big = pygame.font.SysFont("arial", 64, bold=True)
        
        text_shadow = font_big.render("YOU WON!", True, (50, 50, 50))
        screen.blit(text_shadow, (WIDTH//2 - text_shadow.get_width()//2 + 3, HEIGHT//2 - 80 + 3))
        
        text = font_big.render("YOU WON!", True, (255, 215, 0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 80))
        
        font_score = pygame.font.SysFont("arial", 32, bold=True)
        score_text = font_score.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))
        
        if frame > 120: 
            font_small = pygame.font.SysFont("arial", 20)
            continue_text = font_small.render("Press any key to continue...", True, (200, 200, 200))
            screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 80))
        
        pygame.display.update()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
        
        animation_time += 1

def get_hand_frame(cap):
    ret, frame = cap.read()
    if not ret: 
        return None, None
    
    frame = cv2.flip(frame, 1)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
            
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = frame.shape
            tip_x, tip_y = int(index_tip.x * w), int(index_tip.y * h)
            cv2.circle(frame, (tip_x, tip_y), 10, (255, 255, 0), -1)
            
            center_x, center_y = w // 2, h // 2
            cv2.rectangle(frame, 
                         (center_x - 80, center_y - 80), 
                         (center_x + 80, center_y + 80), 
                         (0, 255, 255), 2)
    
    return frame, results

def cvframe_to_pygame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (200, 150))
    return pygame.surfarray.make_surface(frame.swapaxes(0, 1))

def draw_icons(img, pos):
    screen.blit(img, pos)
    return pygame.Rect(*pos, img.get_width(), img.get_height())

def draw_help():
    for y in range(HEIGHT):
        color_ratio = y / HEIGHT
        r = int(240 - (color_ratio * 40))  
        g = int(240 - (color_ratio * 60))  
        b = int(255 - (color_ratio * 55)) 
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
    
    main_rect = pygame.Rect(30, 30, WIDTH-60, HEIGHT-60)
    shadow_rect = pygame.Rect(35, 35, WIDTH-60, HEIGHT-60)
    
    pygame.draw.rect(screen, (100, 100, 100, 100), shadow_rect, border_radius=15)
    pygame.draw.rect(screen, (255, 255, 255, 230), main_rect, border_radius=15)
    pygame.draw.rect(screen, (70, 130, 180), main_rect, 3, border_radius=15)
    
    font_title = pygame.font.SysFont("arial", 42, bold=True)
    title_text = "Game Instructions"
    
    title_shadow = font_title.render(title_text, True, (100, 100, 100))
    title_rect_shadow = title_shadow.get_rect(center=(WIDTH//2 + 2, 72))
    screen.blit(title_shadow, title_rect_shadow)
    
    title_surface = font_title.render(title_text, True, (25, 25, 112))
    title_rect = title_surface.get_rect(center=(WIDTH//2, 70))
    screen.blit(title_surface, title_rect)
    
    pygame.draw.line(screen, (70, 130, 180), (60, 100), (WIDTH-60, 100), 3)
    pygame.draw.line(screen, (135, 206, 235), (60, 103), (WIDTH-60, 103), 1)
    
    font_section = pygame.font.SysFont("arial", 20, bold=True)
    font_text = pygame.font.SysFont("arial", 16)
    font_sub = pygame.font.SysFont("arial", 14)
    
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
            "items": [
                "• Use arrow keys to move",            ],
            "color": (139, 69, 19)
        },
        {
            "title": "Game Features:",
            "items": [
                "Collect stars for +10 points each",
                "Themes change every levels",
                "Each theme has unique background music",
                "Complete levels to increase your score"
            ],
            "color": (128, 0, 128)
        }
    ]
    
    current_y = 130
    
    for section in sections:
        section_surface = font_section.render(section["title"], True, section["color"])
        screen.blit(section_surface, (70, current_y))
        current_y += 35
        
        for item in section["items"]:
            item_surface = font_text.render(item, True, (40, 40, 40))
            screen.blit(item_surface, (90, current_y))
            current_y += 22
        
        current_y += 10  
    
    tips_rect = pygame.Rect(50, current_y, WIDTH-100, 80)
    pygame.draw.rect(screen, (255, 248, 220), tips_rect, border_radius=10)
    pygame.draw.rect(screen, (255, 165, 0), tips_rect, 2, border_radius=10)
    

    
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
        screen.blit(tip_surface, (90, current_y + 12 + i*18))
    
    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 80, 200, 40)
    
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        button_color = (100, 149, 237)
        text_color = (255, 255, 255)
    else:
        button_color = (70, 130, 180)
        text_color = (255, 255, 255)
    
    shadow_button_rect = pygame.Rect(WIDTH//2 - 98, HEIGHT - 78, 200, 40)
    pygame.draw.rect(screen, (50, 50, 50, 100), shadow_button_rect, border_radius=20)
    
    pygame.draw.rect(screen, button_color, button_rect, border_radius=20)
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=20)
    
    font_button = pygame.font.SysFont("arial", 18, bold=True)
    button_text = font_button.render("Press SPACE to return", True, text_color)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    
    for i in range(5):
        alpha = 255 - (i * 50)
        
        pygame.draw.circle(screen, (255, 255, 255, alpha//3), (60 + i*3, 60 + i*3), 3-i, 1)
        pygame.draw.circle(screen, (255, 255, 255, alpha//3), (WIDTH-60 - i*3, 60 + i*3), 3-i, 1)
    
    font_version = pygame.font.SysFont("arial", 12)
    version_text = font_version.render("Maze Adventure v1.0", True, (150, 150, 150))
    screen.blit(version_text, (WIDTH - 140, HEIGHT - 25))


def main():
    global maze_index, score, stars_collected, total_stars, camera_on
    current_character = character_selection()
    mazes = load_mazes_from_file(MAZE_FILE)
    maze_index = 0
    maze = mazes[maze_index]
    player_x, player_y = find_start(maze)
    
    total_stars = count_stars(maze)
    stars_positions = []
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 4:
                stars_positions.append((x, y))
    
    change_theme(current_theme)
    
    # current_character = character_image
    hand_controller = HandGestureController()
    
    cap, camera_on, help_on = None, False, False
    camera_pos, exit_pos, help_pos = (10, HEIGHT-130), (70, HEIGHT-130), (140, HEIGHT-130)
    clock = pygame.time.Clock()
    
    last_move_time = 0
    move_delay = 0.2  

    while True:
        current_time = time.time()
        screen.fill(THEMES[current_theme]["bg"])
        
        draw_maze(maze, stars_positions)
        draw_player(player_x, player_y, current_character)
        draw_ui()
        
        cam_rect = draw_icons(camera_img, camera_pos)
        exit_rect = draw_icons(exit_img, exit_pos)
        help_rect = draw_icons(help_img, help_pos)

        if not camera_on:
            pygame.draw.line(screen, (255, 0, 0), camera_pos, 
                           (camera_pos[0]+50, camera_pos[1]+50), 4)
            pygame.draw.line(screen, (255, 0, 0), 
                           (camera_pos[0], camera_pos[1]+50), 
                           (camera_pos[0]+50, camera_pos[1]), 4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if cap: 
                    cap.release()
                hands.close()
                pygame.quit()
                return
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                help_on = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if cam_rect.collidepoint(mx, my):
                    if cap: 
                        cap.release()
                        cap = None
                        camera_on = False
                    else: 
                        cap = cv2.VideoCapture(0)
                        if cap.isOpened():
                            camera_on = True
                            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                            cap.set(cv2.CAP_PROP_FPS, 30)
                        else:
                            cap = None
                            
                elif exit_rect.collidepoint(mx, my): 
                    if cap:
                        cap.release()
                    hands.close()
                    pygame.quit()
                    return
                    
                elif help_rect.collidepoint(mx, my): 
                    help_on = True

        if help_on:
            draw_help()
        else:
            dx, dy = 0, 0
            
            if camera_on and cap:
                frame, results = get_hand_frame(cap)
                if frame is not None:
                    pygame_surface = cvframe_to_pygame(frame)
                    screen.blit(pygame_surface, (WIDTH - 200, HEIGHT - 150))
                    
                    dx, dy = hand_controller.get_direction(results, frame.shape[1], frame.shape[0])
            else:
                keys = pygame.key.get_pressed()
                dx, dy = handle_input(keys)

            if (dx != 0 or dy != 0) and current_time - last_move_time > move_delay:
                new_x, new_y = player_x + dx, player_y + dy
                if can_move(maze, new_x, new_y):
                    player_x, player_y = new_x, new_y
                    last_move_time = current_time
                    
                    collect_star(player_x, player_y, stars_positions)

            if maze[player_y][player_x] == 3:
                print(f"Level {maze_index + 1} completed! Score: {score}")
                
                score += 50
                
                result = next_maze(mazes, maze_index)
                if result[0] is not None:
                    if done_sound:
                        done_sound.play()
                    maze_index, maze, (player_x, player_y), stars_positions = result
                    print(f"New level! Theme: {THEMES[current_theme]['name']}")
                    pygame.time.delay(500)
                else:
                    show_game_over()
                    if cap:
                        cap.release()
                    hands.close()

        pygame.display.update()
        clock.tick(30) 

if __name__ == "__main__":
    main()
