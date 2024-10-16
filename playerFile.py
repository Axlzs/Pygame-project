import pygame
from static_variables import *
from animations import *


# Define the PLayer class
class Player(pygame.sprite.Sprite):
    def __init__(self, player_type):
        self.type = player_type
        self.scale = PLAYER_SCALE
        self.sprite_sheet = self.load_sprite_sheet(player_type, self.scale)
        self.images = self.extract_frames(self.sprite_sheet, 48, 48, scale_factor=self.scale)
        self.animations = {
            'walk down' : Animation(self.images['walk down'],COOLDOWNS['movement']),
            'walk left' : Animation(self.images['walk left'],COOLDOWNS['movement']),
            'walk right' : Animation(self.images['walk right'],COOLDOWNS['movement']),
            'walk up' : Animation(self.images['walk up'],COOLDOWNS['movement']),

            'stand down' : Animation(self.images['stand down'],COOLDOWNS['movement']),
            'stand left' : Animation(self.images['stand left'],COOLDOWNS['movement']),
            'stand right' : Animation(self.images['stand right'],COOLDOWNS['movement']),
            'stand up' : Animation(self.images['stand up'],COOLDOWNS['movement']),

            'shoot down' : Animation(self.images['shoot down'],COOLDOWNS['shoot']),
            'shoot left' : Animation(self.images['shoot left'],COOLDOWNS['shoot']),
            'shoot right' : Animation(self.images['shoot right'],COOLDOWNS['shoot']),
            'shoot up' : Animation(self.images['shoot up'],COOLDOWNS['shoot']),

            'death' : Animation(self.images['death'],COOLDOWNS['movement'])
        }
        self.start_animation = self.animations['stand down']
        self.image = self.start_animation.get_current_frame()

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2) # Center the player
        self.health = PLAYER_HEALTH[player_type]

    def load_sprite_sheet(self, player_type, scale): # usiversal function
        sprite_sheet = pygame.image.load(PLAYER_IMAGES[player_type]).convert_alpha()

        if scale !=1:
            sprite_width, sprite_height = sprite_sheet.get_size()
            # int is used to negate the appearance of floats
            scaled_size = (int(sprite_width*scale), int(sprite_height*scale))
            sprite_sheet = pygame.transform.scale(sprite_sheet, scaled_size)
        return sprite_sheet

    def create_action_list(self, sprite_sheet):
        action_list = {}
        action_mapping = {
            'walk down': 0,
            'walk left': 1,
            'walk right': 2,
            'walk up': 3,
            'stand down': 4,
            'stand left': 5,
            'stand right': 6,
            'stand up': 7,
            'shoot down': 8,
            'shoot left': 9,
            'shoot right': 10,
            'shoot up': 11,
            'death': 12
        }
        frame_width = 48
        frame_height = 48
        for row,action in action_mapping.items(): # For loop for tuples can contain multiple variables 
            action_frames = []
            for i in range(6): # Each action will have 6 frames
                x = i * frame_width # Which frame is being copied
                y = row * frame_height
                frame = sprite_sheet.subsurface((x, y, 48, 48))
                action_frames.append(frame)
            action_list[action] = action_frames
        return action_list
    
    def update(self):
        self.image = self.start_animation.get_current_frame()
        #animation changes
        #player movement
        #probably player attacks
        #also probably death as well


    
    def create_animation_list(self, sprite_sheet):

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