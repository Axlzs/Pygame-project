import pygame
from static_variables import *
from static_classes import *
from animations import *
from collections import deque
from game_manager import game_manager

# Define the PLayer class
class Player(pygame.sprite.Sprite):
    def __init__(self, player_type,projectile_group, enemy_projectile_group, enemies):
        game_manager.load_settings()
        self.type = player_type
        self.scale = PLAYER_SCALE
        self.sprite_size = PLAYER_DATA[player_type]['sprite']
        self.player_class = PLAYER_DATA[player_type]['class']
        self.projectile_group = projectile_group
        self.sprite_sheet = self.load_sprite_sheet(player_type, self.scale)
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
        self.animation_queue = deque()
        self.is_animating = False
        self.image = self.start_animation.get_current_frame()

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2+3) # Center the player

        self.hitbox = pygame.Rect(0, 0, PLAYER_DATA[player_type]['hitbox_width']*PLAYER_SCALE, PLAYER_DATA[player_type]['hitbox_height']*PLAYER_SCALE)
        self.hitbox.center = self.rect.center  # Align hitbox and sprite position

        self.enemies = enemies
        self.total_enemies_killed = 0
        self.enemies_killed_for_lvl =0
        self.speed_linear = SPEED_LINEAR
        self.speed_diagonal = SPEED_DIAGONAL
        self.max_xp = STARTING_XP
        self.xp_scale = XP_SCALE
        self.xp_bar_length = 100*PLAYER_SCALE
        self.xp_bar_ratio = self.max_xp/self.xp_bar_length
        self.level = 1

        self.health = PLAYER_DATA[self.type]['health']
        self.target_health = self.health
        self.maxhealth = self.health
        self.health_bar_length = self.maxhealth* PLAYER_SCALE * PLAYER_SCALE# sprite means the length of one player frame 
        self.health_ratio = self.maxhealth/self.health_bar_length
        self.health_change_speed = 1
        self.is_dying = False
        self.officially_dead = False
        self.death_start_time = 0
        self.death_duration = 700
        self.damage_cooldown = COOLDOWNS['damage']
        self.last_damage_time = 0
        self.motion = False
        self.direction = 'down'

        self.enemy_projectile_group = enemy_projectile_group
        self.shooting = False
        self.last_shot_time = 0
        self.shoot_cooldown = PROJECTILE_COOLDOWN
        self.arrow_offset = 0
        self.arrow_offset = 10*self.scale

        self.melee_range = PLAYER_DATA[2]['range'] * self.scale
        self.melee_cooldown = MELEE_COOLDOWN
        self.last_melee_time = 0
        self.heal_factor = PLAYER_DATA[2]['heal_factor']


    def load_sprite_sheet(self, player_type, scale):
        sprite_sheet = pygame.image.load(PLAYER_DATA[player_type]['image']).convert_alpha()

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
    
    def handle_movement(self):
        keys = pygame.key.get_pressed()
        self.motion = False
        if self.is_animating:  # Block movement if an attack is playing
            return
        else:
            # Adjust SPEED based on linear or diagonal movement
            if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
                SPEED = self.speed_diagonal  # Reduce SPEED for diagonal movement
            else:
                SPEED = self.speed_linear  # Adjust SPEED for non-diagonal movement

            if self.is_dying == False:
                if keys[pygame.K_w]:
                    self.rect.y -= SPEED
                    self.motion = True
                    self.direction = 'up'
                if keys[pygame.K_a]:
                    self.rect.x -= SPEED
                    self.motion = True
                    self.direction = 'left'
                if keys[pygame.K_s]:
                    self.rect.y += SPEED
                    self.motion = True
                    self.direction = 'down'
                if keys[pygame.K_d]:
                    self.rect.x += SPEED
                    self.motion = True
                    self.direction = 'right'

                #This handles shooting - detects input->Determines the player type and weather the player is moving
                if keys[pygame.K_SPACE]:
                    self.motion == False
                    self.shooting = True
                    if self.type ==1:
                        self.shoot(self.projectile_group)
                    elif self.type ==2:
                        self.mele_attack()
                    else:
                        print("sum tin wong")
                else:
                    self.shooting = False 
            else:
                pass

    def shoot(self,projectile_group):
        current_time = pygame.time.get_ticks()
        # Check if enough time has passed since the last shot
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            
            #getting player and the mouse position
            recy = self.rect.centery
            recx = self.rect.centerx
            self.camera.update(self.rect)
            mouse_pos = pygame.mouse.get_pos()
            looking_at = pygame.Vector2(mouse_pos[0] + self.camera.offset.x, mouse_pos[1] + self.camera.offset.y)

            angle = math.degrees(math.atan2(-(looking_at[1] - recy), looking_at[0] - recx))
            # Determine direction based on angle
            if -45 <= angle < 45:
                self.direction = 'right'
            elif 45 <= angle < 135:
                self.direction = 'up'
            elif 135 <= angle or angle < -135:
                self.direction = 'left'
            elif -135 <= angle < -45:
                self.direction = 'down'

            self.animation_queue.append(f'shoot {self.direction}')
            self.is_animating = True
            self.last_shot_time = current_time
            #x, y, direction, damage, projectile_type
            projectile = Projectile(recx, recy, looking_at, damage=10, projectile_type=1)
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

            self.animation_queue.append(f'shoot {self.direction}')
            self.is_animating = True

            # Check for collisions with enemies
            melee_hitbox = self.get_melee_hitbox()
            if self.last_melee_time == 0:
                pass
            else:
                for enemy in self.enemies:
                    if melee_hitbox.colliderect(enemy.hitbox):
                        enemy.take_damage(PLAYER_DATA[2]['damage'])
                for projectile in self.enemy_projectile_group:
                    if melee_hitbox.colliderect(projectile.rect):
                        projectile.kill()


    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if self.is_dying == False:
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.last_damage_time = current_time
                self.target_health -= amount
                if self.target_health <= 0:
                    self.start_death_sequence()
                    self.target_health = 0
        else: pass
    
    def heal(self, amount):
        if self.target_health < self.maxhealth:
            self.target_health = min(self.target_health + amount, self.maxhealth)

    def start_death_sequence(self):
        self.is_dying = True
        self.death_start_time = pygame.time.get_ticks()

    def update_projectile_attacks(self,projectile_group):
        for projectile in projectile_group:
            projectile_hitbox = self.camera.apply(projectile.rect)
            for enemy in self.enemies:
                enemy_hitbox = self.camera.apply(enemy.hitbox)
                if enemy_hitbox.colliderect(projectile_hitbox):
                    enemy.take_damage(PLAYER_DATA[1]['damage'])

    def add_to_killed_enemies(self):
        self.total_enemies_killed+=1
        self.enemies_killed_for_lvl+=1
        if self.enemies_killed_for_lvl >= self.max_xp:
            self.enemies_killed_for_lvl = 0
            self.level+=1
            self.max_xp += int(math.log(self.max_xp,2))
            self.xp_bar_ratio = self.max_xp/self.xp_bar_length
        if self.type ==2:
            self.heal(self.heal_factor)

    def update(self):
        # Handle queued animations
        if self.animation_queue:
            animation_name = self.animation_queue[0]  # Peek at the front of the queue
            self.start_animation = self.animations[animation_name]
            self.image = self.start_animation.play_once()

            # If the animation is done, remove it from the queue
            if self.start_animation.is_completed():
                self.start_animation.reset() # Sets the animation to the starting frame
                self.animation_queue.popleft()
                self.is_animating = False  # Reset to allow new actions

        # If no animations are queued, proceed with normal movement or idle animations
        elif not self.is_animating:
            self.handle_movement()
            if self.motion:
                self.start_animation = self.animations[f'walk {self.direction}']
            else:
                self.start_animation = self.animations[f'stand {self.direction}']
            self.image = self.start_animation.get_current_frame()

        # Handle player death
        if self.is_dying:
            self.start_animation = self.animations['death']
            self.image = self.start_animation.play_once()
            if pygame.time.get_ticks() - self.death_start_time >= self.death_duration:
                self.officially_dead = True
        
        self.update_projectile_attacks(self.projectile_group)
