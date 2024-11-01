import pygame
import random
from static_variables import *

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

        # start_x = target_rect.centerx + WIDTH // 2 - int(camera_offset.x)
        # start_y = target_rect.centery + HEIGHT // 2 - int(camera_offset.y)
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
        # Renders each tile on the screen
        # for x, y, tile_index in tiles:
        #     screen_position = pygame.Vector2(x,y) - camera_offset
        #     screen.blit(self.background_tiles[tile_index], screen_position)
        for tile in tiles:
            x, y, tile_index = tile
            screen_position = pygame.Vector2(x,y) - camera_offset
            screen.blit(self.background_tiles[tile_index], screen_position)