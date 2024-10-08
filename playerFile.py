import pygame
from static_variables import *


# Define the PLayer class
class Player(pygame.sprite.Sprite):
    def __init__(self, player_type, player_id):
        super().__init__()
        self.type = player_type
        self.images = self.load_sprite_sheet(PLAYER_IMAGES[player_type], PLAYER_WIDTH,PLAYER_HEIGHT)
        self.image_index = 0 # starting frame of animation 
        self.image = self.images[self.image_index] # this is the image that will be displayed
        self.last_animation_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        icon_x, icon_y = (WIDTH - PLAYER_WIDTH) / 2, (HEIGHT - PLAYER_HEIGHT) / 2 
        self.rect.topleft = pygame.Rect(icon_x, icon_y, PLAYER_WIDTH/3,PLAYER_HEIGHT/2)
        self.health = PLAYER_HEALTH[player_type]
        self.id = player_id

    def load_sprite_sheet(self, filename, sprite_size): # usiversal function
        sprite_sheet = pygame.image.load(filename).convert_alpha()
        width, height = sprite_sheet.get_size() # gets the size of sprite sheet 
        rows = height // sprite_size[1] # sprite_sheet[1] = height
        columns = width // sprite_size[0] # sprite_sheet[0] = width
        images = []
        for row in range(rows):
            for col in range(columns):
                rect = pygame.Rect(col * sprite_size[0], row * sprite_size[1], sprite_size[0], sprite_size[1])
                images.append(sprite_sheet.subsurface(rect))
        return images

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time > PLAYER_ANIMATION_SPEED:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
            self.last_animation_time = current_time