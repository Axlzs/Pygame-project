import pygame
from static_variables import Static_variables
from static_classes import *
from animations import *
from collections import deque
from game_manager import game_manager

# Define the PLayer class
class Player(pygame.sprite.Sprite):
    def __init__(self, player_type,projectile_group, enemy_projectile_group, all_enemies, droppable_group):
        game_manager.load_settings()
        self.type = player_type
        self.scale = Static_variables.PLAYER_SCALE
        self.player_scale = Static_variables.PLAYER_DATA[player_type]['scale'] 
        self.sprite_size = Static_variables.PLAYER_DATA[player_type]['sprite']
        self.player_animation_data = Static_variables.PLAYER_ANIMATION_DATA[player_type]
        self.projectile_group = projectile_group
        self.camera = Camera()
        self.sprite_sheet = self.load_sprite_sheet(player_type, self.scale)
        self.images = self.create_action_list(self.sprite_sheet,self.scale)
        self.initialize_animations()

        self.start_animation = self.animations['stand down']
        self.animation_queue = deque()
        self.is_animating = False
        self.image = self.start_animation.get_current_frame()

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2+3) # Center the player

        self.hitbox = pygame.Rect(0, 0, Static_variables.PLAYER_DATA[player_type]['hitbox_width']*Static_variables.PLAYER_SCALE, Static_variables.PLAYER_DATA[player_type]['hitbox_height']*Static_variables.PLAYER_SCALE)
        self.hitbox.center = self.rect.center  # Align hitbox and sprite position

        self.enemies = all_enemies
        self.total_enemies_killed = 0
        self.total_lessers_killed = 0
        self.xp = 0
        self.speed_linear = Static_variables.PLAYER_DATA[self.type]['default_speed_linear']
        self.speed_diagonal = Static_variables.PLAYER_DATA[self.type]['default_speed_diagonal']
        self.max_xp = Static_variables.STARTING_XP
        self.xp_scale = Static_variables.XP_SCALE
        self.xp_bar_length = 100*Static_variables.PLAYER_SCALE
        self.xp_bar_ratio = self.max_xp/self.xp_bar_length
        self.level = 1

        self.droppable_group = droppable_group
        self.health = Static_variables.PLAYER_DATA[self.type]['health']
        self.target_health = self.health
        self.maxhealth = self.health
        self.health_bar_length = self.maxhealth* Static_variables.PLAYER_SCALE * Static_variables.PLAYER_SCALE# sprite means the length of one player frame 
        self.health_ratio = self.maxhealth/self.health_bar_length
        self.health_change_speed = 1
        self.is_dying = False
        self.officially_dead = False
        self.death_start_time = 0
        self.death_duration = 700

        self.dealing_damage = Static_variables.PLAYER_DATA[self.type]['damage']
        self.damage_cooldown = Static_variables.COOLDOWNS['damage']
        self.last_damage_time = 0
        self.motion = False
        self.direction = 'down'

        self.enemy_projectile_group = enemy_projectile_group
        if self.type ==1:
            self.shooting = False
            self.last_shot_time = 0
            self.shoot_cooldown = Static_variables.PROJECTILE_COOLDOWN
            self.arrow_offset = 0
            self.arrow_offset = 10*self.scale
        else:
            self.melee_range_width = Static_variables.PLAYER_DATA[self.type]['hit_range_width'] * self.scale
            self.melee_range_height = Static_variables.PLAYER_DATA[self.type]['hit_range_height'] * self.scale
            self.melee_cooldown = Static_variables.MELEE_COOLDOWN
            self.last_melee_time = 0
            self.heal_factor = Static_variables.PLAYER_DATA[self.type]['heal_factor']

   
    def initialize_animations(self):
        self.animations = {
            action: Animation(self.images[action], data['cooldown'])
            for action, data in self.player_animation_data.items()
        }

    def load_sprite_sheet(self, player_type, scale):
        sprite_sheet = pygame.image.load(Static_variables.PLAYER_DATA[player_type]['image']).convert_alpha()
        
        sprite_width, sprite_height = sprite_sheet.get_size()
        # int is used to negate the appearance of floats
        scaled_size = (int(sprite_width//2*scale*self.player_scale), int(sprite_height//2*scale*self.player_scale))
        sprite_sheet = pygame.transform.scale(sprite_sheet, scaled_size)
        return sprite_sheet

    def create_action_list(self, sprite_sheet, scale):
        action_list = {}
        frame_width = self.sprite_size//2 * scale * self.player_scale
        frame_height = self.sprite_size//2 * scale * self.player_scale
    
        for action, data in self.player_animation_data.items():
            row = data['row']
            frame_count = data['frames']
            #print('action:'+action+'  frame count:'+str(frame_count),'  row: '+str(row)+'  frame width: '+ str(frame_width))
            action_frames = []
    
            for i in range(frame_count):
                x = i * frame_width
                y = row * frame_height
                frame = sprite_sheet.subsurface((x, y, frame_width, frame_height))
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

            else:
                pass
    def handle_attack(self):
        if self.is_animating == False and self.is_dying == False:  # Block movement if an attack is playing
                #This handles shooting - detects input->Determines the player type and weather the player is moving
                self.motion == False
                self.shooting = True
                if self.type ==1:
                    self.shoot(self.projectile_group)
                elif self.type ==2:
                    self.animation_queue.append(f'attack {self.direction}')
                    self.is_animating = True
                else:
                    print("This type of player does not exist")

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

            self.animation_queue.append(f'attack {self.direction}')
            self.is_animating = True
            self.last_shot_time = current_time
            #x, y, direction, damage, projectile_type
            projectile = Projectile(recx, recy, looking_at, damage=10, projectile_type=1)
            projectile_group.add(projectile)
 
    def get_melee_hitbox(self):
        # Create a rect for the melee hitbox based on the player's direction and position
        if self.direction == 'up':
            return pygame.Rect(self.hitbox.centerx - 1.5*self.melee_range_width, self.hitbox.top - self.melee_range_height, 3*self.melee_range_width, 2*self.melee_range_height)
        elif self.direction == 'down':
            return pygame.Rect(self.hitbox.centerx - 1.5*self.melee_range_width, self.hitbox.bottom - self.melee_range_height, 3*self.melee_range_width, 2*self.melee_range_height)
        elif self.direction == 'left':
            return pygame.Rect(self.hitbox.left - 2*self.melee_range_width, self.hitbox.centery - self.melee_range_height, 3*self.melee_range_width, 2*self.melee_range_height)
        elif self.direction == 'right':
            return pygame.Rect(self.hitbox.right - self.melee_range_width, self.hitbox.centery - self.melee_range_height, 3*self.melee_range_width, 2*self.melee_range_height)
        
    def mele_attack(self):
        # Check for collisions with enemies
        melee_hitbox = self.get_melee_hitbox()

        for enemy in self.enemies:
            if melee_hitbox.colliderect(enemy.hitbox):
                enemy.take_damage(self.dealing_damage)

        for projectile in self.enemy_projectile_group:
            if melee_hitbox.colliderect(projectile.rect):
                projectile.kill()


    def take_damage(self, amount, damage_cooldown):
        current_time = pygame.time.get_ticks()
        if self.is_dying == False:
            if current_time - self.last_damage_time >= damage_cooldown:
                self.last_damage_time = current_time
                self.target_health -= amount
                if self.target_health <= 0:
                    self.start_death_sequence()
                    self.target_health = 0
            pass
        else: pass

    def take_continous_damage(self,amount):
        if self.is_dying == False:
            self.target_health -= amount
            if self.target_health <= 0:
                self.start_death_sequence()
                self.target_health = 0
            pass
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
                    enemy.take_damage(self.dealing_damage)

    def collect_drop(self):
        for drop in self.droppable_group:
            if self.hitbox.colliderect(drop.rect):
                drop.interact(self)

    def add_to_killed_enemies(self):
        self.total_enemies_killed+=1

    def add_to_killed_lesser_enemies(self):
        self.total_lessers_killed+=1
    
    def gain_xp(self, amount):
        self.xp+=amount
        if self.xp >= self.max_xp:
            self.xp = 0
            self.level+=1 
            self.max_xp += int(math.log(self.max_xp,2))
            self.xp_bar_ratio = self.max_xp/self.xp_bar_length
        if self.type ==2:
            self.heal(self.heal_factor)

    def restart(self):
        """
        To reset player we basically only need to reset the parameters that were upgraded:
        -Health
        -Player dealt damage 
        -Attack speed 
        -Running speed
        """
        # Restart health
        self.health = Static_variables.PLAYER_DATA[self.type]['health']
        self.target_health = self.health
        self.maxhealth = self.health
        self.health_bar_length = self.maxhealth* Static_variables.PLAYER_SCALE * Static_variables.PLAYER_SCALE# sprite means the length of one player frame 
        self.health_ratio = self.maxhealth/self.health_bar_length

        # Reset player dealt damage
        self.dealing_damage = Static_variables.PLAYER_DATA[self.type]['damage']

        # Reset attack and shoot speed
        Static_variables.COOLDOWNS = {'idle':100,'movement':100,'shoot animation':100,'damage':500}

        if self.type ==1:
            self.shooting = False
            self.last_shot_time = 0
            self.shoot_cooldown = Static_variables.PROJECTILE_COOLDOWN
            self.arrow_offset = 0
            self.arrow_offset = 10*self.scale
        else:
            self.melee_range = Static_variables.PLAYER_DATA[self.type]['range'] * self.scale
            self.melee_cooldown = Static_variables.MELEE_COOLDOWN
            self.last_melee_time = 0
            self.heal_factor = Static_variables.PLAYER_DATA[self.type]['heal_factor']

    def update(self):
        # Handle queued animations
        if self.animation_queue:
            if self.type == 2:
                self.mele_attack()
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
        self.collect_drop()
        self.hitbox.center = self.rect.center
