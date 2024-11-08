import pygame
from static_variables import *
from static_classes import *
from playerFile import Player  # Assuming your Player class is in a file named player.py
from enemyFile import Enemy


# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roguelike Game")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 100)

def draw_fps_counter():
    """
    Renders the current frames per second (FPS) on the screen using
    the specified font and displays it at the top-left corner of the game screendow.
    """
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (10, 10))

def draw_entities():
    #map stuff
    visible_tiles = map.get_background_tiles(player.rect, camera.offset)
    map.render(screen, visible_tiles, camera.offset)
    
    screen.blit(player.image, camera.apply(player.rect))
    #player hitbox
    pygame.draw.rect(screen, (0, 255, 0), player.hitbox,2)
    
    #projectile stuff
    for projectile in projectile_group:
        offset_rect = camera.apply(projectile.rect)
        screen.blit(projectile.image, offset_rect)
        #arrow hitbox
        pygame.draw.rect(screen, (255,0,0), offset_rect,2)

    for enemy in enemies:
        offset_rect = camera.apply(enemy.rect)
        screen.blit(enemy.image, offset_rect)
    #mele hitbox 
    melee_hitbox = player.get_melee_hitbox()
    pygame.draw.rect(screen, (255, 0, 0), camera.apply(melee_hitbox), 2)

#setting up game
projectile_group = pygame.sprite.Group()
player_type=2
player = Player(player_type, projectile_group)  # Pass the appropriate player type here
camera = Camera()
map = WorldMap()

enemies = pygame.sprite.Group()
enemy_count = 0
for _ in range(30):
    enemy_type = random.choice(list(ENEMY_DATA.keys()))
    enemy_count +=1
    enemy = Enemy(enemy_type, projectile_group, player)
    enemies.add(enemy)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_fps_counter()
    player.update()
    enemies.update()
    camera.update(player.rect)
    projectile_group.update()
    draw_entities()
        
    pygame.display.flip()

    clock.tick(FPS)

# Quit Pygame
pygame.quit()