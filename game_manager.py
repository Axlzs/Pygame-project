import pygame
import json
import os

CONFIG_PATH = "config.json"

class GameManager:
    def __init__(self):
        pygame.init()
        self.display = self.get_display_res()
        self.settings = self.load_settings()
        self.screen = self.apply_settings()
        self.update_dimensions()

    def get_display_res(self):
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        display_info = pygame.display.Info()
        display_width = display_info.current_w
        display_height = display_info.current_h
        return display_width,display_height

    def load_settings(self):
        """Load default or saved settings"""
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as file:
                return json.load(file)
        else:
            # Default settings if config doesn't exist
            return {
                "screen_mode": "fullscreen",
                "resolution": [800, 600]
            }

    def save_settings(self):
        """Save current settings to the configuration file"""
        with open(CONFIG_PATH, 'w') as file: # w - write; r - read; a - append; x - create
            json.dump(self.settings, file)

    def apply_settings(self):
        if self.settings["screen_mode"] == "fullscreen":
            return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            width, height = self.settings["resolution"]
            d_width, d_height = self.display

            if d_width >= width and d_height >= height:
                return pygame.display.set_mode((width, height), pygame.RESIZABLE)
            else: 
                self.settings["resolution"] = 1000,700
                width, height = self.settings["resolution"]
                return pygame.display.set_mode((width, height), pygame.RESIZABLE)
            
    def update_dimensions(self):
        """Update cached screen dimensions"""
        WIDTH, HEIGHT = self.screen.get_size()
        return WIDTH,HEIGHT


game_manager = GameManager() # creating a single instance of GameManager, so it can be used by all files