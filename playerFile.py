import pygame
from static_variables import *
from animations import *


# Define the PLayer class
class Player(pygame.sprite.Sprite):
    def __init__(self, player_type):
        self.type = player_type
        self.scale = PLAYER_SCALE
        self.sprite_sheet = self.load_sprite_sheet(player_type, self.scale)
        self.images = self.create_action_list(self.sprite_sheet,self.scale)
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

    def create_action_list(self, sprite_sheet, scale):
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
        frame_width = 48 * scale
        frame_height = 48 * scale
        for action, row in action_mapping.items():  # Unpack the dictionary correctly
            action_frames = []
            for i in range(6):  # Each action will have 6 frames
                x = i * frame_width  # Which frame is being copied
                y = row * frame_height  # Row based on action index
                frame = sprite_sheet.subsurface((x, y, frame_width, frame_height))  # Use the variables correctly
                action_frames.append(frame)
            action_list[action] = action_frames
        return action_list
    
    def update(self):
        self.image = self.start_animation.get_current_frame()
        #animation changes
        #player movement
        #probably player attacks
        #also probably death as well

    def handle_movement(self):
    # Example for movement handling with keyboard inputs
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            print("w in the chat ")
            #self.rect.y -= speed
            self.start_animation = self.animations['walk up']
        if keys[pygame.K_a]:
            #self.rect.x -= speed
            self.start_animation = self.animations['walk left']
        if keys[pygame.K_s]:
            #self.rect.y -= speed
            self.start_animation = self.animations['walk down']
        if keys[pygame.K_d]:
            #self.rect.x += speed
            self.start_animation = self.animations['walk right']

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.start_animation = self.animations['death']