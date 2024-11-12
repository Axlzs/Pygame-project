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
font = pygame.font.Font(None, 50)

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

    for projectile in enemy_projectile_group:
        offset_rect = camera.apply(projectile.rect)
        screen.blit(projectile.image, offset_rect)
        #arrow hitbox
        pygame.draw.rect(screen, (0,255,0), offset_rect,2)

    for enemy in enemies:

        offset_rect = camera.apply(enemy.rect)
        screen.blit(enemy.image, offset_rect)
        melee_hitbox = enemy.get_melee_hitbox()
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(melee_hitbox), 2)
        pygame.draw.rect(screen, (255, 0, 0), camera.apply(enemy.hitbox), 2)
    
    #mele hitbox 
    melee_hitbox = player.get_melee_hitbox()
    pygame.draw.rect(screen, (255, 0, 0), camera.apply(melee_hitbox), 2)


def manual_enemy_spawn(enemy_count):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]: # Manualy spawn enemies 
        enemy_type = random.choice(list(ENEMY_DATA.keys()))
        enemy_count +=1
        enemy = Enemy(enemy_type, enemy_projectile_group, player)
        enemies.add(enemy)
    elif keys[pygame.K_k]: # Kill all enemies 
        enemies.empty()



#setting up game
projectile_group = pygame.sprite.Group()
enemy_projectile_group = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_type=2
player = Player(player_type, projectile_group, enemies)  # Pass the appropriate player type here
camera = Camera()
map = WorldMap()

enemy_count = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
##############FUNCTIONS##############
    player.update()
    enemies.update()
    camera.update(player.rect)
    projectile_group.update()
    enemy_projectile_group.update()             
    draw_entities()
    draw_fps_counter() 
    manual_enemy_spawn(enemy_count)
    
##############HANDLING#DAMAGE##############
    for projectile in enemy_projectile_group:
        projectile_hitbox=camera.apply(projectile.rect)
        if player.hitbox.colliderect(projectile_hitbox):
            player.take_damage(ENEMY_DATA[1]['damage'])

    for projectile in projectile_group:
        projectile_hitbox = camera.apply(projectile.rect)
        for enemy in enemies:
            enemy_hitbox = camera.apply(enemy.hitbox)
            if enemy_hitbox.colliderect(projectile_hitbox):
                enemy.take_damage(PLAYER_DATA[1]['damage'])        

    pygame.display.flip()

    clock.tick(FPS)

# Quit Pygame
pygame.quit()