import pygame
import random
from static_variables import *


# Define the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, player):
        super().__init__()
        self.type = enemy_type
        self.images = self.load_sprite_sheet(ENEMY_IMAGES[enemy_type], ENEMY_SIZE)
        self.image_index = 0 # starting frame of animation 
        self.image = self.images[self.image_index] # this is the image that will be displayed
        self.last_animation_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.spawn_enemy_position(player) # for enemy hitboxes 
        self.health = ENEMY_HEALTH[enemy_type]

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

    def spawn_enemy_position(self, player):
        square_top_left_x = player.x - 600
        square_top_left_y = player.y - 500
        square_bottom_right_x = player.x + 600
        square_bottom_right_y = player.y + 500
        while True:
            # Generate random x and y coordinates outside the square
            x = random.uniform(square_top_left_x - 200, square_bottom_right_x + 200)
            y = random.uniform(square_top_left_y - 200, square_bottom_right_y + 200)
            
            # Check if the generated point is outside the square
            if x < square_top_left_x or x > square_bottom_right_x or y < square_top_left_y or y > square_bottom_right_y:
                return x, y 

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_time > ENEMY_ANIMATION_SPEED:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
            self.last_animation_time = current_time