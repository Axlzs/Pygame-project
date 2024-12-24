import pygame
from static_variables import Static_variables
from static_classes import *
from animations import *
from game_manager import game_manager

WIDTH, HEIGHT = game_manager.update_dimensions()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, projectile_group, player, droppable_group,enemy_projectile_group):
        pygame.sprite.Sprite.__init__(self)
        self.type = enemy_type  # Who am i
        self.id = Static_variables.ENEMY_DATA[self.type]['id']
        self.player = player    # target player
        self.camera = Camera()  # camera for offsets and stuff
        self.scale = Static_variables.PLAYER_SCALE              # PLAYER_SCALE basically means the game_scale
        self.enemy_projectile_group = enemy_projectile_group    # Where enemy arrows reside
        self.enemy_scale = Static_variables.ENEMY_DATA[self.type]['scale']      # how big am i 
        self.sprite_size = Static_variables.ENEMY_DATA[enemy_type]['sprite']    # how big is a single animation frame 
        self.enemy_animation_data = Static_variables.ENEMY_ANIMATION_DATA[enemy_type]   # What animations enemy has paired with cooldowns
        self.projectile_group = projectile_group    # Where player arrows reside
        self.droppable_group = droppable_group      # Where stuff that drops reside 
        self.sprite_sheet = self.load_sprite_sheet(enemy_type, self.scale)
        self.images = self.create_action_list(self.sprite_sheet,self.scale)
        self.initialize_animations()
        self.start_animation = self.animations['walk down']     # Gives the enemy first set of animations
        self.image = self.start_animation.get_current_frame()   # IDK if this is needed 

        self.rect = self.image.get_rect()
        self.rect.center = self.get_enemy_spawn() # Enemy spawn coordinates

        self.hitbox = pygame.Rect(0, 0, Static_variables.ENEMY_DATA[enemy_type]['hitbox_width']*Static_variables.PLAYER_SCALE, Static_variables.ENEMY_DATA[enemy_type]['hitbox_height']*Static_variables.PLAYER_SCALE)
        self.hitbox.center = self.rect.center  # Align hitbox and sprite position

        self.default_health = Static_variables.ENEMY_DATA[self.type]['health']
        self.health = Static_variables.ENEMY_DATA[self.type]['health']      # Current health
        self.maxhealth = Static_variables.ENEMY_DATA[self.type]['health']   # Maximum heaalth that an enemy can have
        self.health_bar_length = self.hitbox.width                          # How long is the healthar
        self.health_ratio = self.maxhealth/self.health_bar_length           # Ratio to fit all that health in the health_bar_length
        self.is_dying = False       # State of death
        self.death_start_time = 0   # The start of the death animation gets assigned here
        self.death_duration = 700   # How long to player death animation
        self.attack_damage = Static_variables.ENEMY_DATA[self.type]['damage']            # damage that will be done to the player
        self.attack_cooldown = Static_variables.ENEMY_DATA[self.type]['attack_cooldown'] # how long is the players window of immunity
        self.damage_cooldown = Static_variables.ENEMY_COOLDOWNS['damage']                # how long is the window of immunity for enemy
        self.last_damage_time = 0   # The last time enemy took damage, this is for damage_cooldown 
        self.motion = False         # State where enemy is nether dead or attacking 
        self.direction = 'down'
        self.speed = Static_variables.ENEMY_DATA[self.type]['speed']
        if self.type == 1:  # Type 1 is for archer enemy
            self.shooting = False
            self.last_shot_time = 0
            self.shoot_cooldown = Static_variables.ENEMY_PROJECTILE_COOLDOWN
            self.arrow_offset = 0
            self.arrow_offset = 10*self.scale
            self.shoot_dist = Static_variables.ENEMY_DATA[self.type]['shoot dist']
        else:     # For melee enemies
            self.melee_range = Static_variables.ENEMY_DATA[self.type]['range'] * self.scale
            self.melee_cooldown = Static_variables.MELEE_COOLDOWN
            self.last_melee_time = 0
            self.melee_attack_dist = Static_variables.ENEMY_DATA[self.type]['attack dist'] * self.scale # When enemy stops moving and starts attacking 

    def initialize_animations(self):
        self.animations = {
            action: Animation(self.images[action], data['cooldown'])
            for action, data in self.enemy_animation_data.items()
        }

    def load_sprite_sheet(self, enemy_type, scale):
        sprite_sheet = pygame.image.load(Static_variables.ENEMY_DATA[enemy_type]['image']).convert_alpha()

        sprite_width, sprite_height = sprite_sheet.get_size()
        # int is used to negate the appearance of floats
        scaled_size = (int(sprite_width*scale*self.enemy_scale), int(sprite_height*scale*self.enemy_scale))
        sprite_sheet = pygame.transform.scale(sprite_sheet, scaled_size)
        return sprite_sheet

    def create_action_list(self, sprite_sheet, scale):
        action_list = {}
        frame_width = self.sprite_size * scale * self.enemy_scale
        frame_height = self.sprite_size * scale * self.enemy_scale
        #print(self.type)
        for action, data in self.enemy_animation_data.items():
            row = data['row']
            frame_count = data['frames']
            action_frames = []
            #print('action:'+action+'  frame count:'+str(frame_count),'  row: '+str(row)+'  frame width: '+ str(frame_width))
    
            for i in range(frame_count):
                x = i * frame_width
                y = row * frame_height
                frame = sprite_sheet.subsurface((x, y, frame_width, frame_height))
                action_frames.append(frame)
    
            action_list[action] = action_frames
    
        return action_list
    
    def get_enemy_spawn(self):
        square_top_left_x = self.player.hitbox.x - (HEIGHT-Static_variables.ENEMY_SPAWN_DISTANCE)
        square_top_left_y =self.player.hitbox.y - (WIDTH-Static_variables.ENEMY_SPAWN_DISTANCE)
        square_bottom_right_x =self.player.hitbox.x + (HEIGHT+Static_variables.ENEMY_SPAWN_DISTANCE)
        square_bottom_right_y =self.player.hitbox.y + (WIDTH+Static_variables.ENEMY_SPAWN_DISTANCE)
        while True:
            # Generate random x and y coordinates outside the square
            x = random.uniform(square_top_left_x - Static_variables.ENEMY_SPAWN_AREA, square_bottom_right_x + Static_variables.ENEMY_SPAWN_AREA)
            y = random.uniform(square_top_left_y - Static_variables.ENEMY_SPAWN_AREA, square_bottom_right_y + Static_variables.ENEMY_SPAWN_AREA)
            
            # Check if the generated point is outside the square
            if x < square_top_left_x or x > square_bottom_right_x or y < square_top_left_y or y > square_bottom_right_y:
                return (x, y)

    def angle_to_player(self):
        recy = self.rect.centery
        recx = self.rect.centerx
        targetx = self.player.hitbox.centerx
        targety = self.player.hitbox.centery

        return math.degrees(math.atan2(-(targety - recy), targetx - recx))
    def enemy_actions(self):

        self.motion = False

        dx = self.player.hitbox.centerx - self.rect.centerx # Distance between player.x and enemy.x
        dy = self.player.hitbox.centery - self.rect.centery # Distance between player.y and enemy.y
        dist = (dx**2 + dy**2) ** 0.5 # Basically pythagoream theorem, straightest path between enemy and player

        if dist > 0:
            dx, dy = dx / dist, dy / dist  # Normalize direction
        else:
            dx, dy = 0, 0

        if dist>3000:
            self.rect.center = self.get_enemy_spawn()

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
            elif self.type !=1 and dist <= self.melee_attack_dist:
                self.motion = False
                self.shooting = True
            else:
                self.shooting = False
                self.motion = True
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed

            # Calling animations 
            if self.shooting:
                self.start_animation = self.animations[f'attack {self.direction}']
                if self.type ==1:
                    self.shoot(self.projectile_group)
                elif self.type !=1:
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
            targetx = self.player.hitbox.centerx
            targety = self.player.hitbox.centery

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
            return pygame.Rect(self.hitbox.centerx - self.melee_range, self.hitbox.top - self.melee_range, 2*self.melee_range, self.melee_range)
        elif self.direction == 'down':
            return pygame.Rect(self.hitbox.centerx - self.melee_range, self.hitbox.bottom, 2*self.melee_range, self.melee_range)
        elif self.direction == 'left':
            return pygame.Rect(self.hitbox.left - 2*self.melee_range, self.hitbox.centery - self.melee_range, 2*self.melee_range, 2*self.melee_range)
        elif self.direction == 'right':
            return pygame.Rect(self.hitbox.right, self.hitbox.centery - self.melee_range, 2*self.melee_range, 2*self.melee_range)
    
    def mele_attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_melee_time >= self.melee_cooldown:
            self.last_melee_time = current_time
            # Check for collisions with enemies
            melee_hitbox = self.get_melee_hitbox()

            if melee_hitbox.colliderect(self.player.hitbox):
                self.player.take_damage(self.attack_damage)
            

    def update_projectile_attacks(self):
        for projectile in self.enemy_projectile_group:
            projectile_hitbox=self.camera.apply(projectile.rect)
            player_hitbox = self.camera.apply(self.player.hitbox)
            if player_hitbox.colliderect(projectile_hitbox):
                self.player.take_damage(self.attack_damage)  

    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if self.is_dying == False:
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.last_damage_time = current_time
                self.health -= amount
                if self.health <= 0:
                    #self.player.gain_xp() # this is here, because this must run only once on enemy death
                    self.start_death_sequence()
        else: pass

    def heal(self, amount):
        if amount>0:
            if (self.health + amount) > self.maxhealth:
                self.health = self.maxhealth
            else:
                self.health += amount

    def start_death_sequence(self):
        self.is_dying = True
        self.death_start_time = pygame.time.get_ticks()

    def drop_something(self,droppable_group):
        what_drop = random.choices(Static_variables.POPULATION, Static_variables.DROPTABLE)[0]
        if what_drop != 'nothing':
            new_drop = Droppable(what_drop, self.rect.centerx,self.rect.centery)
            droppable_group.add(new_drop)

    def respawn(self):
        self.is_dying = False
        self.health = self.maxhealth
        self.rect.center = self.get_enemy_spawn()

    def update(self):
    #UPDATES STUFF
    #CHECKS IF PLAYER IS DEAD
    #ALIGNS HITBOXES
        if self.is_dying:
            #self.start_animation = self.animations['death']
            self.image = self.start_animation.play_once()
            death_time = pygame.time.get_ticks()
            if death_time - self.death_start_time >= self.death_duration:
                self.start_animation.reset()
                self.drop_something(self.droppable_group)
                self.player.add_to_killed_enemies()
                self.respawn()

        else:
            #Get image -> determine correct action -> add animation to the action 
            self.image = self.start_animation.get_current_frame()
        self.enemy_actions()
        self.update_projectile_attacks()
        self.hitbox.center = self.rect.center  # Align hitbox and sprite position

class LesserEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, player, droppable_group,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.type = enemy_type
        self.player = player
        self.camera = Camera()
        self.scale = Static_variables.PLAYER_SCALE
        self.enemy_scale = Static_variables.LESSER_ENEMIES[self.type]['scale']
        self.sprite_size = Static_variables.LESSER_ENEMIES[enemy_type]['sprite']
        self.enemy_animation_data = Static_variables.LESSER_ENEMIES_ANIMATION[enemy_type]
        self.droppable_group = droppable_group
        self.sprite_sheet = self.load_sprite_sheet()
        self.images = self.create_action_list(self.sprite_sheet,self.scale)
        self.initialize_animations()
        self.start_animation = self.animations['move']
        self.image = self.start_animation.get_current_frame()

        self.rect = self.image.get_rect()
        self.rect.center = (x,y) # Enemy spawn coordinates

        self.hitbox = pygame.Rect(0, 0, Static_variables.LESSER_ENEMIES[enemy_type]['hitbox_width']*Static_variables.PLAYER_SCALE, Static_variables.LESSER_ENEMIES[enemy_type]['hitbox_height']*Static_variables.PLAYER_SCALE)
        self.hitbox.center = self.rect.center  # Align hitbox and sprite position

        self.health = Static_variables.LESSER_ENEMIES[self.type]['health']
        self.maxhealth = Static_variables.LESSER_ENEMIES[self.type]['health']
        self.health_bar_length = self.hitbox.width# sprite means the length of one player frame 
        self.health_ratio = self.maxhealth/self.health_bar_length
        self.damage_cooldown = 100
        self.last_damage_time = 0
        self.attack_damage = Static_variables.LESSER_ENEMIES[self.type]['damage']
        self.speed = Static_variables.LESSER_ENEMIES[self.type]['speed']
        self.is_dying = False
        self.death_start_time = 0
        self.death_duration = 300
        self.motion = False

    def load_sprite_sheet(self):
        sprite_sheet = pygame.image.load(Static_variables.LESSER_ENEMIES[self.type]['image']).convert_alpha()

        sprite_width, sprite_height = sprite_sheet.get_size()
        # int is used to negate the appearance of floats
        scaled_size = (int(sprite_width//2*self.scale*self.enemy_scale), int(sprite_height//2*self.scale*self.enemy_scale))
        sprite_sheet = pygame.transform.scale(sprite_sheet, scaled_size)
        return sprite_sheet
    
    def create_action_list(self, sprite_sheet, scale):
        action_list = {}
        frame_width = self.sprite_size//2 * scale * self.enemy_scale
        frame_height = self.sprite_size//2 * scale * self.enemy_scale
        for action, data in self.enemy_animation_data.items():
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

    def initialize_animations(self):
        self.animations = {
            action: Animation(self.images[action], data['cooldown'])
            for action, data in self.enemy_animation_data.items()
        }
    
    def get_enemy_spawn(self):
        square_top_left_x = self.player.hitbox.x - (HEIGHT-Static_variables.ENEMY_SPAWN_DISTANCE)
        square_top_left_y =self.player.hitbox.y - (WIDTH-Static_variables.ENEMY_SPAWN_DISTANCE)
        square_bottom_right_x =self.player.hitbox.x + (HEIGHT+Static_variables.ENEMY_SPAWN_DISTANCE)
        square_bottom_right_y =self.player.hitbox.y + (WIDTH+Static_variables.ENEMY_SPAWN_DISTANCE)
        while True:
            # Generate random x and y coordinates outside the square
            x = random.uniform(square_top_left_x - Static_variables.ENEMY_SPAWN_AREA, square_bottom_right_x + Static_variables.ENEMY_SPAWN_AREA)
            y = random.uniform(square_top_left_y - Static_variables.ENEMY_SPAWN_AREA, square_bottom_right_y + Static_variables.ENEMY_SPAWN_AREA)
            
            # Check if the generated point is outside the square
            if x < square_top_left_x or x > square_bottom_right_x or y < square_top_left_y or y > square_bottom_right_y:
                return (x, y)

    def enemy_actions(self):
        if self.is_dying == False:
            self.motion = True
            # Calculate distance to the player
            dx = self.player.hitbox.centerx - self.rect.centerx
            dy = self.player.hitbox.centery - self.rect.centery
            dist = (dx**2 + dy**2) ** 0.5

            if dist>3000:
                self.rect.center = self.get_enemy_spawn()

            # Avoid division by zero
            if dist > 0:
                dx, dy = dx / dist, dy / dist  # Normalize direction
            else:
                dx, dy = 0, 0

            # Move the enemy towards the player
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        else: 
            self.start_animation = self.animations['death']
            self.motion = False

    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if self.is_dying == False:
            if current_time - self.last_damage_time >= self.damage_cooldown:
                self.last_damage_time = current_time
                self.health -= amount
                if self.health <= 0:
                    #self.player.gain_xp() # this is here, because this must run only once on enemy death
                    self.start_death_sequence()
        else: pass
        
    def attack(self):
        if self.hitbox.colliderect(self.player.hitbox):
            self.player.take_continous_damage(self.attack_damage)

    def start_death_sequence(self):
        self.is_dying = True
        self.death_start_time = pygame.time.get_ticks()
    
    def drop_something(self,droppable_group):
        what_drop = random.choices(Static_variables.POPULATION, Static_variables.LESSER_DROPTABLE)[0]
        if what_drop != 'nothing':
            new_drop = Droppable(what_drop, self.rect.centerx,self.rect.centery)
            droppable_group.add(new_drop)

    def update(self):
    #UPDATES STUFF
    #CHECKS IF ENEMY IS DEAD
    #ALIGNS HITBOXES
        if self.is_dying:
            self.image = self.start_animation.play_once()
            if pygame.time.get_ticks() - self.death_start_time >= self.death_duration:
                self.player.add_to_killed_lesser_enemies()
                self.kill()
                self.drop_something(self.droppable_group)

        else:
            #Get image -> determine correct action -> add animation to the action 
            self.image = self.start_animation.get_current_frame()
            self.attack()
        self.enemy_actions()
        self.hitbox.center = self.rect.center  # Align hitbox and sprite position