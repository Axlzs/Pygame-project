import pygame
from static_variables import *
from static_classes import *
from animations import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, projectile_group, player):
        pygame.sprite.Sprite.__init__(self)
        self.type = enemy_type
        self.scale = PLAYER_SCALE
        self.player = player
        self.sprite_size = ENEMY_DATA[enemy_type]['sprite']
        self.player_class = ENEMY_DATA[enemy_type]['class']
        self.projectile_group = projectile_group
        self.sprite_sheet = self.load_sprite_sheet(enemy_type, self.scale)
        self.images = self.create_action_list(self.sprite_sheet,self.scale)
        self.camera = Camera()
        self.animations = {
            'walk down' : Animation(self.images['walk down'],COOLDOWNS['movement']),
            'walk left' : Animation(self.images['walk left'],COOLDOWNS['movement']),
            'walk right' : Animation(self.images['walk right'],COOLDOWNS['movement']),
            'walk up' : Animation(self.images['walk up'],COOLDOWNS['movement']),

            'stand down' : Animation(self.images['stand down'],COOLDOWNS['movement']),
            'stand left' : Animation(self.images['stand left'],COOLDOWNS['movement']),
            'stand right' : Animation(self.images['stand right'],COOLDOWNS['movement']),
            'stand up' : Animation(self.images['stand up'],COOLDOWNS['movement']),

            'shoot down' : Animation(self.images['shoot down'],COOLDOWNS['shoot animation']),
            'shoot left' : Animation(self.images['shoot left'],COOLDOWNS['shoot animation']),
            'shoot right' : Animation(self.images['shoot right'],COOLDOWNS['shoot animation']),
            'shoot up' : Animation(self.images['shoot up'],COOLDOWNS['shoot animation']),

            'death' : Animation(self.images['death'],COOLDOWNS['movement'])
        }
        self.start_animation = self.animations['stand down']
        self.image = self.start_animation.get_current_frame()

        self.rect = self.image.get_rect()
        self.rect.center = self.get_enemy_spawn() # Enemy spawn coordinates

        self.hitbox = pygame.Rect(0, 0, ENEMY_DATA[enemy_type]['hitbox_width']*PLAYER_SCALE, ENEMY_DATA[enemy_type]['hitbox_height']*PLAYER_SCALE)
        self.hitbox.center = self.rect.center  # Align hitbox and sprite position

        self.health = ENEMY_DATA[self.type]['health']
        self.maxhealth = ENEMY_DATA[self.type]['health']
        self.health_bar_length = 20* PLAYER_SCALE# sprite means the length of one player frame 
        self.health_ratio = self.maxhealth/self.health_bar_length
        self.is_dying = False
        self.death_start_time = 0
        self.death_duration = 700
        self.damage_cooldown = COOLDOWNS['damage']
        self.last_damage_time = 0
        self.motion = False
        self.direction = 'down'

        self.shooting = False
        self.last_shot_time = 0
        self.shoot_cooldown = ENEMY_PROJECTILE_COOLDOWN
        self.arrow_offset = 0
        self.arrow_offset = 10*self.scale
        self.shoot_dist = ENEMY_DATA[1]['shoot dist']

        self.melee_damage = ENEMY_DATA[2]['damage']
        self.melee_range = ENEMY_DATA[2]['range'] * self.scale
        self.melee_cooldown = MELEE_COOLDOWN
        self.last_melee_time = 0
        self.melee_attack_dist = ENEMY_DATA[2]['attack dist'] # When enemy stops moving and starts attacking 


    def load_sprite_sheet(self, enemy_type, scale):
        sprite_sheet = pygame.image.load(ENEMY_DATA[enemy_type]['image']).convert_alpha()

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
        frame_width = self.sprite_size * scale
        frame_height = self.sprite_size * scale
        for action, row in action_mapping.items():  # Unpack the dictionary correctly
            action_frames = []
            for i in range(6):  # Each action will have 6 frames
                x = i * frame_width  # Which frame is being copied
                y = row * frame_height  # Row based on action index
                frame = sprite_sheet.subsurface((x, y, frame_width, frame_height))  # Use the variables correctly
                action_frames.append(frame)
            action_list[action] = action_frames
        return action_list
    
    def get_enemy_spawn(self):
        square_top_left_x = self.player.rect.x - (HEIGHT/2)-ENEMY_SPAWN_DISTANCE
        square_top_left_y =self.player.rect.y - (WIDTH/2)-ENEMY_SPAWN_DISTANCE
        square_bottom_right_x =self.player.rect.x + (HEIGHT/2)+ENEMY_SPAWN_DISTANCE
        square_bottom_right_y =self.player.rect.y + (WIDTH/2)+ENEMY_SPAWN_DISTANCE
        while True:
            # Generate random x and y coordinates outside the square
            x = random.uniform(square_top_left_x - ENEMY_SPAWN_AREA, square_bottom_right_x + ENEMY_SPAWN_AREA)
            y = random.uniform(square_top_left_y - ENEMY_SPAWN_AREA, square_bottom_right_y + ENEMY_SPAWN_AREA)
            
            # Check if the generated point is outside the square
            if x < square_top_left_x or x > square_bottom_right_x or y < square_top_left_y or y > square_bottom_right_y:
                return (x, y)

    def angle_to_player(self):
        recy = self.rect.centery
        recx = self.rect.centerx
        targetx = self.player.rect.centerx
        targety = self.player.rect.centery

        return math.degrees(math.atan2(-(targety - recy), targetx - recx))
    def enemy_actions(self):

        self.motion = False

        dx = self.player.rect.centerx - self.rect.centerx # Distance between player.x and enemy.x
        dy = self.player.rect.centery - self.rect.centery # Distance between player.y and enemy.y
        dist = (dx**2 + dy**2) ** 0.5 # Basically pythagoream theorem, straightest path between enemy and player

        # Adjust SPEED based on linear or diagonal movement
        if dx != 0 and dy != 0:
            SPEED = ENEMY_SPEED_DIAGONAL  # Set speed to diagonal speed if moving diagonally
        else:
            SPEED = ENEMY_SPEED_LINEAR  # Use linear speed for straight movements


        if self.is_dying == False:
            # Understanding which way should the enemy face
            angle = self.angle_to_player()
            if -45 <= angle < 45:
                self.direction = 'right'
                self.motion = True
            elif 45 <= angle < 135:
                self.direction = 'up'
                self.motion = True
            elif 135 <= angle or angle < -135:
                self.direction = 'left'
                self.motion = True
            elif -135 <= angle < -45:
                self.direction = 'down'
                self.motion = True

            # Handling movement - moving enemy
            if self.type ==1 and dist <= self.shoot_dist:
                self.motion = False
                self.shooting = True
            elif self.type ==2 and dist <= self.melee_attack_dist:
                self.motion = False
                self.shooting = True
            else:
                self.shooting = False
                self.motion = True
                dx, dy = dx / dist, dy / dist
                self.rect.x += dx * SPEED
                self.rect.y += dy * SPEED

            # Calling animations 
            if self.shooting:
                self.start_animation = self.animations[f'shoot {self.direction}']
                if self.type ==1:
                    self.shoot(self.projectile_group)
                elif self.type ==2:
                    self.mele_attack()
            elif self.motion:
                self.start_animation = self.animations[f'walk {self.direction}']
            else:
                self.start_animation = self.animations[f'stand {self.direction}']
        else:
            self.start_animation = self.animations['death']
    def shoot(self,projectile_group):
        current_time = pygame.time.get_ticks()
        # Check if enough time has passed since the last shot
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.last_shot_time = current_time

            recy = self.rect.centery
            recx = self.rect.centerx
            targetx = self.player.rect.centerx
            targety = self.player.rect.centery

            angle = self.angle_to_player()
            # Determine direction based on angle
            if -45 <= angle < 45:
                self.direction = 'right'
            elif 45 <= angle < 135:
                self.direction = 'up'
            elif 135 <= angle or angle < -135:
                self.direction = 'left'
            elif -135 <= angle < -45:
                self.direction = 'down'
            
            #x, y, direction, damage, projectile_type
            projectile = Projectile(recx, recy, (targetx,targety), damage=10, projectile_type=1)
            projectile_group.add(projectile)
    
    def get_melee_hitbox(self):
        # Create a rect for the melee hitbox based on the player's direction and position
        if self.direction == 'up':
            return pygame.Rect(self.rect.centerx - self.melee_range, self.rect.top + (7+self.scale), 2*self.melee_range, self.melee_range)
        elif self.direction == 'down':
            return pygame.Rect(self.rect.centerx - self.melee_range, self.rect.bottom - (self.melee_range + self.scale), 2*self.melee_range, self.melee_range)
        elif self.direction == 'left':
            return pygame.Rect(self.rect.left + (7*self.scale), self.rect.centery - self.melee_range, self.melee_range, 2*self.melee_range)
        elif self.direction == 'right':
            return pygame.Rect(self.rect.right - (self.melee_range + (7*self.scale)), self.rect.centery - self.melee_range, self.melee_range, 2*self.melee_range)

    def mele_attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_melee_time >= self.melee_cooldown:
            self.last_melee_time = current_time
            # Check for collisions with enemies
            melee_hitbox = self.get_melee_hitbox()

            mele_range = self.camera.apply(self.player.hitbox)
            if mele_range.colliderect(self.player.hitbox):
                self.player.take_damage(ENEMY_DATA[2]['damage'])


    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if self.is_dying == False:
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.last_damage_time = current_time
                self.health -= amount
                if self.health <= 0:
                    self.player.add_to_killed_enemies() # this is here, because this must run only once on enemy death
                    self.start_death_sequence()
        else: pass

    def start_death_sequence(self):
        self.is_dying = True
        self.death_start_time = pygame.time.get_ticks()

    def update(self):
    #UPDATES STUFF
    #CHECKS IF PLAYER IS DEAD
    #ALIGNS HITBOXES
        if self.is_dying:
            self.image = self.start_animation.play_once()
            if pygame.time.get_ticks() - self.death_start_time >= self.death_duration:
                self.kill()
        else:
            #Get image -> determine correct action -> add animation to the action 
            self.image = self.start_animation.get_current_frame()
        self.enemy_actions()
        self.hitbox.center = self.rect.center  # Align hitbox and sprite position
