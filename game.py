import pygame
from static_variables import *
from static_classes import *
from playerFile import Player
from enemyFile import Enemy

def load_game_over_assets():
    """
    Load images and sounds for the game over screen.
    """
    global gameover_img, mainmenu_imgs, restart_imgs, backquit_sound, start_sound
    gameover_img = pygame.image.load('images/gameover.png').convert_alpha()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    # Load button images and rescale them
    mainmenu_imgs = [pygame.transform.scale(pygame.image.load(f'images/mainmenu-{i}.png'), (300, 100)) for i in range(1, 4)]
    restart_imgs = [pygame.transform.scale(pygame.image.load(f'images/restart-{i}.png'), (250, 100)) for i in range(1, 4)]

    backquit_sound = pygame.mixer.Sound('sounds/backquit.ogg')
    start_sound = pygame.mixer.Sound('sounds/start.ogg')

    start_sound.set_volume(0.1)
    backquit_sound.set_volume(0.1)


def initialize_game():
    global screen,clock,font,spawned_enemies
    pygame.init()

    pygame.display.set_caption("Roguelike Game")

    clock = pygame.time.Clock()
    font = pygame.font.Font("font/Minecraft.ttf", 20)
    
    load_game_over_assets()

def game_over_screen():
    """
    Displays the game over screen with interactive buttons.
    """
    mainmenu_rect = pygame.Rect((WIDTH // 2 + 50, HEIGHT // 2 + 280), (300, 100))
    restart_rect = pygame.Rect((WIDTH // 2 - 350, HEIGHT // 2 + 280), (250, 100))
    while True:
        screen.blit(gameover_img, (0, 0))

        font = pygame.font.Font(None, 100)
        score_text = font.render(f"{int(player.total_enemies_killed)}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 + 40, HEIGHT // 2 + 135))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
            # Perform any necessary actions based on the enemy event
            # For example, you could handle different enemy events differently
        if mainmenu_rect.collidepoint(mouse_pos):
            screen.blit(mainmenu_imgs[1], mainmenu_rect.topleft)
            if mouse_click:
                screen.blit(mainmenu_imgs[2], mainmenu_rect.topleft)
                screen.blit(restart_imgs[0], restart_rect.topleft)
                pygame.display.update()
                pygame.mixer.Channel(5).play(backquit_sound)
                pygame.time.delay(100)  # Delay to see the 'clicking' image
                import start_here  # Import the script containing the main menu
                pygame.mixer.stop()
                start_here.main_menu()  # Call main_menu function from start_here
                break
        else:
            screen.blit(mainmenu_imgs[0], mainmenu_rect.topleft)

        if restart_rect.collidepoint(mouse_pos):
            screen.blit(restart_imgs[1], restart_rect.topleft)
            if mouse_click:
                screen.blit(restart_imgs[2], restart_rect.topleft)
                screen.blit(mainmenu_imgs[0], mainmenu_rect.topleft)
                pygame.display.update()
                pygame.mixer.Channel(4).play(start_sound)
                pygame.time.delay(100)
                start_game()  # Restart the game
                break
        else:
            screen.blit(restart_imgs[0], restart_rect.topleft)

        pygame.display.update()
        clock.tick(FPS)

def draw_fps_counter():
    """
    Renders the current frames per second (FPS) on the screen using
    the specified font and displays it at the top-left corner of the game screendow.
    """
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (WIDTH-100, 10))

def draw_entities():
    #map stuff
    visible_tiles = map.get_background_tiles(player.rect, camera.offset)
    map.render(screen, visible_tiles, camera.offset)
    
    screen.blit(player.image, camera.apply(player.rect))
    #player hitbox
    #pygame.draw.rect(screen, (0, 255, 0), player.hitbox,2)
    
    #projectile stuff
    for projectile in projectile_group:
        offset_rect = camera.apply(projectile.rect)
        screen.blit(projectile.image, offset_rect)
        #arrow hitbox
        #pygame.draw.rect(screen, (255,0,0), offset_rect,2)

    for projectile in enemy_projectile_group:
        offset_rect = camera.apply(projectile.rect)
        screen.blit(projectile.image, offset_rect)
        #arrow hitbox
        #pygame.draw.rect(screen, (0,255,0), offset_rect,2)

    for enemy in enemies:

        offset_rect = camera.apply(enemy.rect)
        screen.blit(enemy.image, offset_rect)
        #enemy hitboxes
        #melee_hitbox = enemy.get_melee_hitbox()
        #if enemy.type ==2:
        #    pygame.draw.rect(screen, (255, 0, 0), camera.apply(enemy.hitbox), 2)
        #    pygame.draw.rect(screen, (255, 0, 0), camera.apply(melee_hitbox), 2)
        #else:
        #    pygame.draw.rect(screen, (255, 0, 0), camera.apply(enemy.hitbox), 2)
    
    #mele hitbox
    #if player.type==2:
    #    melee_hitbox = player.get_melee_hitbox()
    #    pygame.draw.rect(screen, (255, 0, 0), camera.apply(melee_hitbox), 2)

def player_healthbar_activate(player):
    transition_width = 0 # This makes the bar initally invisible 
    transition_colour = (255,0,0)

    #healing
    if player.health < player.target_health:
        player.health += player.health_change_speed
        transition_width = int((player.target_health-player.health)/player.health_ratio)
        transition_colour = (0,255,0)

    #taking damage
    if player.health > player.target_health:
        player.health -= player.health_change_speed
        transition_width = int((player.target_health-player.health)/player.health_ratio)
        transition_colour = (255,255,0)

    health_bar_rect = pygame.Rect(10,10,player.health/player.health_ratio,10)
    transition_bar_rect = pygame.Rect(health_bar_rect.right,10,transition_width,10)

    pygame.draw.rect(screen,transition_colour,transition_bar_rect)
    pygame.draw.rect(screen,(255,0,0),health_bar_rect)
    pygame.draw.rect(screen,(255,255,255),(10,10,player.health_bar_length,10),2)

def xp_bar(player):
    pygame.draw.rect(screen, (0,0,255),(10,21,player.enemies_killed_for_lvl/player.xp_bar_ratio,10))
    pygame.draw.rect(screen, (255,255,255),(10,21,player.xp_bar_length,10),2)
    lvl_text = font.render(f"LEVEL: {player.level}", True, WHITE)
    screen.blit(lvl_text, (12, 40))


def enemy_healthbar_activate(enemy):
    offset_rect = camera.apply(enemy.hitbox)
    if enemy.type ==1:
        pygame.draw.rect(screen, (255,0,0),(offset_rect.x,offset_rect.midbottom[1],enemy.health/enemy.health_ratio,10))
        pygame.draw.rect(screen, (255,255,255),(offset_rect.x,offset_rect.midbottom[1],enemy.health_bar_length,10),1)

    if enemy.type ==2:
        pygame.draw.rect(screen, (255,0,0),(offset_rect.x,offset_rect.midbottom[1],enemy.health/enemy.health_ratio,10))
        pygame.draw.rect(screen, (255,255,255),(offset_rect.x,offset_rect.midbottom[1],enemy.health_bar_length,10),1)

def manual_enemy_spawn(spawned_enemies,player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]: # Manualy spawn enemies 
        enemy_type = random.choice(list(ENEMY_DATA.keys()))
        spawned_enemies +=1
        enemy = Enemy(enemy_type, enemy_projectile_group, player)
        enemies.add(enemy)
    elif keys[pygame.K_k]: # Kill all enemies 
        enemies.empty()

def enemy_spawn(enemy_count,spawned_enemies,player,last_enemy_spawn):
    current_time = pygame.time.get_ticks()
    if enemy_count <10 and current_time - last_enemy_spawn >= ENEMY_SPAWN_COOLDOWN:
        enemy_type = random.choice(list(ENEMY_DATA.keys()))
        spawned_enemies +=1
        enemy = Enemy(enemy_type, enemy_projectile_group, player)
        enemies.add(enemy)
        last_enemy_spawn = current_time
    return enemy_count,spawned_enemies,last_enemy_spawn

def main_loop():
    global projectile_group, enemy_projectile_group,enemies,player,camera,map,last_enemy_spawn,enemy_count,spawned_enemies
    #setting up game

    last_enemy_spawn = 0
    projectile_group = pygame.sprite.Group()
    enemy_projectile_group = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player_type=2
    player = Player(player_type, projectile_group, enemy_projectile_group, enemies)  # Pass the appropriate player type here
    camera = Camera()
    map = WorldMap()

    spawned_enemies = 0
    enemy_count = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        enemy_count = spawned_enemies - player.total_enemies_killed
    ##############FUNCTIONS##############
        player.update()
        enemies.update()
        camera.update(player.rect)
        projectile_group.update()
        enemy_projectile_group.update()             
        draw_entities()
        draw_fps_counter() 
        manual_enemy_spawn(spawned_enemies,player)
        enemy_count, spawned_enemies, last_enemy_spawn = enemy_spawn(enemy_count, spawned_enemies, player, last_enemy_spawn)
        player_healthbar_activate(player)
        xp_bar(player)
        for enemy in enemies:
            enemy_healthbar_activate(enemy)
    ##############HANDLING#DAMAGE##############
        for projectile in enemy_projectile_group:
            projectile_hitbox=camera.apply(projectile.rect)
            if player.hitbox.colliderect(projectile_hitbox):
                player.take_damage(ENEMY_DATA[1]['damage'])     

        if player.officially_dead:
            game_over_screen()

 
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    exit()

def start_game():
    """
    Starts the main game initialization.
    """
    initialize_game()
    main_loop()

# Check if this script is being run directly (not imported as a module)
if __name__ == "__main__":
    start_game()