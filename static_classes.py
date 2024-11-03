import pygame
import random
from static_variables import *
from animations import Animation

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)

    def update(self, target_rect):
        # Calculate the offset to keep the target (player) centered
        self.offset.x = target_rect.centerx - WIDTH // 2
        self.offset.y = target_rect.centery - HEIGHT // 2
        
    def apply(self, rect):
        # Return the adjusted position of any rect based on the camera offset
        return rect.move(-self.offset.x, -self.offset.y)
    
class WorldMap:
    def __init__(self):
        self.background_tiles = self.load_background_tiles()
        self.tile_grid = {}

    def load_background_tiles(self):
        background_tiles = []
        for i in range(1,TOTAL_BG+1):
            image = pygame.image.load(f'images/backgrounds/bg-{i}.png').convert()
            image = pygame.transform.scale(image, (WIDTH, HEIGHT))
            background_tiles.append(image)
        return background_tiles
        
    def select_tile_index(self):
        #Selects random tile based on weights
        tiles = list(range(TOTAL_BG))  # Tile indices from 0 to 9
        return random.choices(tiles, weights=BG_CHANCE, k=1)[0]
    
    def get_background_tiles(self, target_rect, camera_offset):
        # Calculate visible tiles based on the player's position and camera offset
        tiles = []

        start_x = int(target_rect.centerx //WIDTH) * WIDTH
        start_y = int(target_rect.centery //HEIGHT) * HEIGHT

        for x in range(start_x - WIDTH, start_x + 2 * WIDTH, WIDTH):
            for y in range(start_y - HEIGHT, start_y + 2 * HEIGHT, HEIGHT):
                grid_x, grid_y = x // WIDTH, y // HEIGHT

                # If tile at (grid_x, grid_y) isn't generated, add it
                if (grid_x, grid_y) not in self.tile_grid:
                    tile_index = self.select_tile_index()
                    self.tile_grid[(grid_x, grid_y)] = tile_index

                tiles.append((x, y, self.tile_grid[(grid_x, grid_y)]))

        return tiles

    def render(self, screen, tiles, camera_offset):
        for tile in tiles:
            x, y, tile_index = tile
            screen_position = pygame.Vector2(x,y) - camera_offset
            screen.blit(self.background_tiles[tile_index], screen_position)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, damage, projectile_type):
        super().__init__()
        self.scale = PLAYER_SCALE//2
        self.projectile_type = projectile_type
        self.projectile_sheet = self.load_projectile_sheet(self.projectile_type,self.scale)
        self.images = self.create_projectile_actions(self.projectile_sheet,self.scale)
        self.animations = {
            'shoot down' : Animation(self.images['shoot down'],COOLDOWNS['shoot']),
            'shoot left' : Animation(self.images['shoot left'],COOLDOWNS['shoot']),
            'shoot right' : Animation(self.images['shoot right'],COOLDOWNS['shoot']),
            'shoot up' : Animation(self.images['shoot up'],COOLDOWNS['shoot']),
        }
        self.current_animation = self.animations[f'shoot {direction}']
        self.image = self.current_animation.get_current_frame()
        self.rect = self.image.get_rect(center=(x, y))

        # Set initial position and movement
        self.pos = pygame.Vector2(x, y)
        self.direction = direction
        self.speed = PROJECILE_SPEED
        self.set_velocity(direction)
        
        self.damage = damage
        self.lifespan = 2000  # in milliseconds
        self.spawn_time = pygame.time.get_ticks()

    def set_velocity(self, direction):
        if direction == 'up':
            self.velocity = pygame.Vector2(0, -self.speed)
        elif direction == 'down':
            self.velocity = pygame.Vector2(0, self.speed)
        elif direction == 'left':
            self.velocity = pygame.Vector2(-self.speed, 0)
        elif direction == 'right':
            self.velocity = pygame.Vector2(self.speed, 0)

    def load_projectile_sheet(self,projectile_type,scale):
        projectile_sheet = pygame.image.load(PROJECTILE_IMAGES[projectile_type]).convert_alpha()

        if scale !=1:
            projectile_width, projectile_height = projectile_sheet.get_size()
            # int is used to negate the appearance of floats
            scaled_size = (int(projectile_width*scale), int(projectile_height*scale))
            projectile_sheet = pygame.transform.scale(projectile_sheet, scaled_size)
        return projectile_sheet

    def create_projectile_actions(self,projectile_sheet,scale):
        projectile_actions = {}
        projectile_mapping = {
            'shoot down' : 0,
            'shoot left' : 1,
            'shoot right' : 2,
            'shoot up' : 3
        }
        frame_width = 48 * scale
        frame_height = 48 * scale
        for action, row in projectile_mapping.items():  # Unpack the dictionary correctly
            action_frames = []
            for i in range(6):  # Each action will have 6 frames
                x = i * frame_width  # Which frame is being copied
                y = row * frame_height  # Row based on action index
                frame = projectile_sheet.subsurface((x, y, frame_width, frame_height))  # Use the variables correctly
                action_frames.append(frame)
            projectile_actions[action] = action_frames
        return projectile_actions

    def update(self):
        # Update position
        self.pos += self.velocity
        self.rect.center = self.pos
        self.image = self.current_animation.get_current_frame()
        self.current_animation = self.animations[f'shoot {self.direction}']
        # Check lifespan
        if pygame.time.get_ticks() - self.spawn_time > self.lifespan:
            self.kill()  # Remove projectile from all sprite groups

        # Add collision checks here if necessary
