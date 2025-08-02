import pygame
import os
import random
from config import *

class AssetManager:
    def __init__(self):
        self.characters = {}
        self.theme_assets = {}
        self.sounds = {}
        self.ui_images = {}
        
    def load_all_assets(self):
        self.load_characters()
        self.load_ui_images()
        self.load_sounds()
        
    def load_characters(self):
        if not os.path.exists(CHARACTERS_DIR):
            return
            
        for filename in os.listdir(CHARACTERS_DIR):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    path = os.path.join(CHARACTERS_DIR, filename)
                    img = pygame.image.load(path).convert_alpha()
                    # Scale to fit tile size
                    img = pygame.transform.scale(img, (TILE_SIZE-10, TILE_SIZE-10))
                    self.characters[filename] = img
                except Exception as e:
                    print(f"Error loading character {filename}: {e}")
                    
    def load_theme_assets(self, theme_name):
        if theme_name in self.theme_assets:
            return self.theme_assets[theme_name]
            
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
            
            # Load music
            music_path = os.path.join(theme_path, "music.mp3")
            if os.path.exists(music_path):
                assets['music'] = music_path
            else:
                assets['music'] = None
                
        except Exception as e:
            print(f"Error loading theme assets for {theme_name}: {e}")
            # Create default star if everything fails
            star_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(star_surface, (255, 215, 0), (15, 15), 12)
            assets['star'] = star_surface
            assets['music'] = None
        
        self.theme_assets[theme_name] = assets
        return assets
    
    def load_sounds(self):
        sound_files = {
            'star_collect': 'star_collect.wav',
            'done': 'done.wav',
            'error': 'error.wav'
        }
        
        for sound_name, filename in sound_files.items():
            try:
                path = os.path.join(SOUNDS_DIR, filename)
                if os.path.exists(path):
                    self.sounds[sound_name] = pygame.mixer.Sound(path)
                else:
                    self.sounds[sound_name] = None
            except Exception as e:
                print(f"Error loading sound {filename}: {e}")
                self.sounds[sound_name] = None
                
    def load_ui_images(self):
        ui_files = {
            'camera': 'camera.png',
            'exit': 'exit.png',
            'help': 'help.png'
        }
        
        for ui_name, filename in ui_files.items():
            try:
                path = os.path.join(ASSETS_DIR, filename)
                if os.path.exists(path):
                    img = pygame.image.load(path)
                    self.ui_images[ui_name] = pygame.transform.scale(img, (50, 50))
                else:
                    # Create default colored rectangles
                    surface = pygame.Surface((50, 50))
                    if ui_name == 'camera':
                        surface.fill(Colors.BLUE)
                    elif ui_name == 'exit':
                        surface.fill(Colors.RED)
                    elif ui_name == 'help':
                        surface.fill(Colors.GREEN)
                    self.ui_images[ui_name] = surface
            except Exception as e:
                print(f"Error loading UI image {filename}: {e}")
                
    def get_character(self, filename=None):
        if not self.characters:
            return None
            
        if filename and filename in self.characters:
            return self.characters[filename]
        
        # Random character
        return random.choice(list(self.characters.values()))
    
    def get_all_characters(self):
        return [(img, name) for name, img in self.characters.items()]
    
    def get_theme_assets(self, theme_name):
        return self.load_theme_assets(theme_name)
    
    def get_sound(self, sound_name):
        return self.sounds.get(sound_name)
    
    def get_ui_image(self, ui_name):
        return self.ui_images.get(ui_name)
    
    def play_sound(self, sound_name):
        sound = self.get_sound(sound_name)
        if sound:
            sound.play()
            
    def play_theme_music(self, theme_name):
        assets = self.get_theme_assets(theme_name)
        if assets['music']:
            try:
                pygame.mixer.music.load(assets['music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)
                return True
            except Exception as e:
                print(f"Error playing music: {e}")
        return False