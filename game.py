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
    global screen,clock,font
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Roguelike Game")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    
    load_game_over_assets()

def game_over_screen():
    """
    Displays the game over screen with interactive buttons.
    """
    global running, score
    mainmenu_rect = pygame.Rect((WIDTH // 2 + 50, HEIGHT // 2 + 280), (300, 100))
    restart_rect = pygame.Rect((WIDTH // 2 - 350, HEIGHT // 2 + 280), (250, 100))
    score =1 
    while True:
        screen.blit(gameover_img, (0, 0))

        font = pygame.font.Font(None, 100)
        score_text = font.render(f"{int(score)}", True, WHITE)
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

def main_loop():
    global projectile_group, enemy_projectile_group,enemies,player,camera,map
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