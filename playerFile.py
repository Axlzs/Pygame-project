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
        self.rect.center = (WIDTH // 2, HEIGHT // 2+3) # Center the player

        self.hitbox = pygame.Rect(0, 0, HITBOX_WIDTH*PLAYER_SCALE, HITBOX_HEIGHT*PLAYER_SCALE)
        self.hitbox.center = self.rect.center  # Align hitbox and sprite position

        self.health = PLAYER_HEALTH[player_type]
        self.motion = False
        self.direction = 'down'
        self.shooting = False

    def load_sprite_sheet(self, player_type, scale):
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
    
    def handle_movement(self):
        keys = pygame.key.get_pressed()
        self.motion = False

        # Adjust SPEED based on linear or diagonal movement
        if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
            SPEED = SPEED_DIAGONAL  # Reduce SPEED for diagonal movement
        else:
            SPEED = SPEED_LINEAR  # Adjust SPEED for non-diagonal movement

        if keys[pygame.K_w]:
            self.rect.y -= SPEED
            self.motion = True
            self.direction = 'up'
            #self.start_animation = self.animations['walk up']
        if keys[pygame.K_a]:
            self.rect.x -= SPEED
            self.motion = True
            self.direction = 'left'
            #self.start_animation = self.animations['walk left']
        if keys[pygame.K_s]:
            self.rect.y += SPEED
            self.motion = True
            self.direction = 'down'
            #self.start_animation = self.animations['walk down']
        if keys[pygame.K_d]:
            self.rect.x += SPEED
            self.motion = True
            self.direction = 'right'
            #self.start_animation = self.animations['walk right']

        if keys[pygame.K_SPACE] and self.motion == False:
            self.shooting = True
        else:
            self.shooting = False

    def handle_motion(self):
        if self.shooting:
            self.start_animation = self.animations[f'shoot {self.direction}']
        elif self.motion:
            self.start_animation = self.animations[f'walk {self.direction}']
        else:
            self.start_animation = self.animations[f'stand {self.direction}'] 
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.start_animation = self.animations['death']

    def update(self):
        #Get image -> determine correct action -> add animation to the action 
        self.image = self.start_animation.get_current_frame()
        self.handle_movement()
        self.handle_motion()
        #animation changes
        #player movement
        #probably player attacks
        #also probably death as well