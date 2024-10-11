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

    def load_sprite_sheet(self, filename, sprite_width,sprite_height): # usiversal function
        sprite_sheet = pygame.image.load(filename).convert_alpha()
        width, height = sprite_sheet.get_size() # gets the size of sprite sheet 
        rows = height // sprite_height # sprite_sheet[1] = height
        columns = width // sprite_width # sprite_sheet[0] = width
        images = []
        for row in range(rows):
            for col in range(columns):
                rect = pygame.Rect(col * sprite_size[0], row * sprite_size[1], sprite_size[0], sprite_size[1])
                images.append(sprite_sheet.subsurface(rect))
        return images

    def create_animation_list(self):

        # Creates a list of sprite animations for the player
        # based on the number of steps in each animation.
        # Extracts images from the sprite sheet for each animation sequence.

        global animation_list, action, frame, step_counter, last_update, animation_cooldown, last_lift_up, animation_completed
        animation_list = []
        animation_steps = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7]
        last_update = pygame.time.get_ticks() # Controls animation speed
        animation_cooldown = 150
        action = 4 # Animation that will be set as default when game starts
        frame = 0
        step_counter = 0 # Each step is one frame in the animation
        last_lift_up = pygame.K_s
        animation_completed = False

        # Splits the spritesheet into frames
        for animation in animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(sprite_sheet.get_image(step_counter, 48, 48, 3, BLACK))
                step_counter += 1
            animation_list.append(temp_img_list)
    def update_animation():

        # Advances the animation frame based on a specified cooldown time.
        # Ensures that the animation frames cycle through the available frames for
        # the current action. The animation updates are synchronized with the game's time.

        global frame, last_update, animation_cooldown, animation_completed, action

        current_time = pygame.time.get_ticks()

        if current_time - last_update >= animation_cooldown:
            if not animation_completed:
                frame += 1
                last_update = current_time
                if frame >= len(animation_list[action]):
                    frame = 0
                    animation_completed = True