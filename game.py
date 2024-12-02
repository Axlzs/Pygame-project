import pygame
from static_variables import *
from static_classes import *
from playerFile import Player
from enemyFile import Enemy
from game_manager import game_manager

game_manager.screen = game_manager.apply_settings()
WIDTH, HEIGHT = game_manager.update_dimensions()
BUTTON_SPRITE_SHEET = pygame.image.load("images/UI_elements/Metal Buttons Text.png").convert_alpha()
def load_game_over_assets():
    global WIDTH,HEIGHT
    """
    Load images and sounds for the game over game_manager.screen.
    """

    global background1,background2,background3,background4, mainmenu_imgs, restart_imgs, backquit_sound, start_sound
    background1 = pygame.image.load("images/UI_elements/Backgrounds/Game_over/1.png").convert()
    background2 = pygame.image.load("images/UI_elements/Backgrounds/Game_over/2.png").convert_alpha()
    background3 = pygame.image.load("images/UI_elements/Backgrounds/Game_over/3.png").convert_alpha()
    background4 = pygame.image.load("images/UI_elements/Backgrounds/Game_over/4.png").convert_alpha()

    # Scale the background image to match the game_manager.screen size
    background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
    background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
    background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
    background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))

    # Load button images and rescale them
    mainmenu_imgs = [pygame.transform.scale(pygame.image.load(f'images/mainmenu-{i}.png'), (300, 100)) for i in range(1, 4)]
    restart_imgs = [pygame.transform.scale(pygame.image.load(f'images/restart-{i}.png'), (250, 100)) for i in range(1, 4)]

    backquit_sound = pygame.mixer.Sound('sounds/backquit.ogg')
    start_sound = pygame.mixer.Sound('sounds/start.ogg')

    start_sound.set_volume(0.1)
    backquit_sound.set_volume(0.1)


def initialize_game():
    global font,spawned_enemies
    pygame.init()
    
    pygame.display.set_caption("Roguelike Game")

    font = pygame.font.Font("font/Minecraft.ttf", 20)
    
    load_game_over_assets()

def game_over_screen(player_type):
    """
    Displays the game over game_manager.screen with interactive buttons.
    """

    main_menu = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "mainmenu", (WIDTH // 2 + 32*PLAYER_SCALE, HEIGHT // 2 + 280))
    restart = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "restart", (WIDTH // 2 - 128*PLAYER_SCALE, HEIGHT // 2 + 280))

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate offsets for each layer based on mouse position
        offset_2 = (mouse_x * 0.01, mouse_y * 0.01)
        offset_3 = (mouse_x * 0.02, mouse_y * 0.02)
        offset_4 = (mouse_x * 0.03, mouse_y * 0.03)  # Most movement

        # Draw layers with parallax effect
        game_manager.screen.blit(background1, (0,0))
        game_manager.screen.blit(background2, (-offset_2[0], -offset_2[1]))
        game_manager.screen.blit(background3, (-offset_3[0], -offset_3[1]))
        game_manager.screen.blit(background4, (-offset_4[0], -offset_4[1]))

        main_menu.draw()
        restart.draw()

        font = pygame.font.Font("font/Minecraft.ttf", 30*PLAYER_SCALE)
        game_over_font = pygame.font.Font("font/Minecraft.ttf", 50*PLAYER_SCALE)

        score_text = font.render(f"ENEMIES KILLED: {int(player.total_enemies_killed)}", True, WHITE)
        game_over_text = game_over_font.render("GAME OVER", True, WHITE)

        game_manager.screen.blit(score_text, ((WIDTH - 285*PLAYER_SCALE) //2, HEIGHT // 2))
        game_manager.screen.blit(game_over_text, ((WIDTH - 285*PLAYER_SCALE) //2, (HEIGHT // 2) - 64*PLAYER_SCALE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Handle button events
            if main_menu.handle_event(event):
                pygame.time.delay(100)
                import start
                start.main_menu()
            if restart.handle_event(event):
                pygame.time.delay(100)
                start_game(player_type)

        pygame.display.update()
        CLOCK.tick(FPS)

def draw_fps_counter():
    """
    Renders the current frames per second (FPS) on the game_manager.screen using
    the specified font and displays it at the top-left corner of the game screendow.
    """
    fps_text = font.render(f"FPS: {int(CLOCK.get_fps())}", True, WHITE)
    game_manager.screen.blit(fps_text, (WIDTH-100, 10))
def draw_entities():
    #map stuff
    # visible_tiles = map.get_background_tiles(player.rect, camera.offset)
    # map.render(game_manager.screen, visible_tiles, camera.offset)

    tiles = map.get_background_tiles(player.rect, camera.offset, WIDTH, HEIGHT)
    map.render(game_manager.screen, tiles, camera.offset)
    
    game_manager.screen.blit(player.image, camera.apply(player.rect))
    #player hitbox
    if RECT_MODE:
        pygame.draw.rect(game_manager.screen, (0, 255, 0), player.hitbox,2)
    
    #projectile stuff
    for projectile in projectile_group:
        offset_rect = camera.apply(projectile.rect)
        game_manager.screen.blit(projectile.image, offset_rect)
        #arrow hitbox
        if RECT_MODE:
            pygame.draw.rect(game_manager.screen, (255,0,0), offset_rect,2)

    for projectile in enemy_projectile_group:
        offset_rect = camera.apply(projectile.rect)
        game_manager.screen.blit(projectile.image, offset_rect)
        #arrow hitbox
        if RECT_MODE:
            pygame.draw.rect(game_manager.screen, (0,255,0), offset_rect,2)

    for enemy in enemies:

        offset_rect = camera.apply(enemy.rect)
        game_manager.screen.blit(enemy.image, offset_rect)
        #enemy hitboxes
        if RECT_MODE:
            melee_hitbox = enemy.get_melee_hitbox()
            if enemy.type ==2:
                pygame.draw.rect(game_manager.screen, (255, 0, 0), camera.apply(enemy.hitbox), 2)
                pygame.draw.rect(game_manager.screen, (255, 0, 0), camera.apply(melee_hitbox), 2)
            else:
                pygame.draw.rect(game_manager.screen, (255, 0, 0), camera.apply(enemy.hitbox), 2)
    
    #mele hitbox
    if RECT_MODE:
        if player.type==2:
            melee_hitbox = player.get_melee_hitbox()
            pygame.draw.rect(game_manager.screen, (255, 0, 0), camera.apply(melee_hitbox), 2)

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

    pygame.draw.rect(game_manager.screen,transition_colour,transition_bar_rect)
    pygame.draw.rect(game_manager.screen,(255,0,0),health_bar_rect)
    pygame.draw.rect(game_manager.screen,(255,255,255),(10,10,player.health_bar_length,10),2)

def xp_bar(player):
    pygame.draw.rect(game_manager.screen, (0,0,255),(10,21,player.enemies_killed_for_lvl/player.xp_bar_ratio,10))
    pygame.draw.rect(game_manager.screen, (255,255,255),(10,21,player.xp_bar_length,10),2)
    lvl_text = font.render(f"LEVEL: {player.level}", True, WHITE)
    game_manager.screen.blit(lvl_text, (12, 40))


def enemy_healthbar_activate(enemy):
    offset_rect = camera.apply(enemy.hitbox)
    if enemy.type ==1:
        pygame.draw.rect(game_manager.screen, (255,0,0),(offset_rect.x,offset_rect.midbottom[1],enemy.health/enemy.health_ratio,10))
        pygame.draw.rect(game_manager.screen, (255,255,255),(offset_rect.x,offset_rect.midbottom[1],enemy.health_bar_length,10),1)

    if enemy.type ==2:
        pygame.draw.rect(game_manager.screen, (255,0,0),(offset_rect.x,offset_rect.midbottom[1],enemy.health/enemy.health_ratio,10))
        pygame.draw.rect(game_manager.screen, (255,255,255),(offset_rect.x,offset_rect.midbottom[1],enemy.health_bar_length,10),1)

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

def upgrade_screen(player_type):
    BUTTON_SPRITE_SHEET = pygame.image.load("images/UI_elements/Debuff buttons.png").convert_alpha()
    health_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "health", (100, HEIGHT//2))
    strength_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "strengthen", (200, HEIGHT//2))
    attack_speed_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "swing", (300, HEIGHT//2))
    speed_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "levelup", (400, HEIGHT//2))

    font = pygame.font.Font("font/Minecraft.ttf", 15*PLAYER_SCALE)
    text = font.render("Choose upgrades", True, WHITE)
    game_manager.screen.blit(text, (WIDTH//2-100*PLAYER_SCALE, HEIGHT//2))

    running = True
    while running:

        health_uppgrade.draw()
        strength_uppgrade.draw()
        attack_speed_uppgrade.draw()
        speed_uppgrade.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_manager.save_settings()
                exit()
            if health_uppgrade.handle_event(event):
                pygame.time.delay(100)
                player.maxhealth += 20
                running = False
            if strength_uppgrade.handle_event(event):
                pygame.time.delay(100)
                PLAYER_DATA[player_type]['damage'] += 10
                running = False
            if attack_speed_uppgrade.handle_event(event):
                pygame.time.delay(100)
                if player.shoot_cooldown > 10 and player_type ==1:
                    player.shoot_cooldown - 50
                    running = False

                if player.melee_cooldown > 10 and player_type ==2:
                    player.melee_cooldown - 50
                    running = False
            if speed_uppgrade.handle_event(event):
                pygame.time.delay(100)
                SPEED_DIAGONAL *1.5
                SPEED_LINEAR * 1.5
                running = False
            

def main_loop(chosen_player):
    global projectile_group, enemy_projectile_group,enemies,player,camera,map,last_enemy_spawn,enemy_count,spawned_enemies,WIDTH,HEIGHT,SPEED_DIAGONAL, SPEED_LINEAR

    #setting up game
    last_enemy_spawn = 0
    projectile_group = pygame.sprite.Group()
    enemy_projectile_group = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player_type=chosen_player
    player = Player(player_type, projectile_group, enemy_projectile_group, enemies)  # Pass the appropriate player type here
    camera = Camera()
    map = WorldMap(TILE_WIDTH, TILE_HEIGHT)

    current_level = player.level
    spawned_enemies = 0
    enemy_count = 0
    upgrade_due = False

    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                player.level +=1
    
        enemy_count = spawned_enemies - player.total_enemies_killed
    ##############FUNCTIONS##############
        if paused:
            for enemy in enemies:
                enemy.motion = False
                enemy.shooting = False
            player.motion = False
            
            font = pygame.font.Font("font/Minecraft.ttf", 15*PLAYER_SCALE)
            text = font.render("Paused - Press 'ESCAPE' to Resume", True, WHITE)
            game_manager.screen.blit(text, (WIDTH//2-100*PLAYER_SCALE, HEIGHT//2))
        elif upgrade_due:

            BUTTON_SPRITE_SHEET = pygame.image.load("images/UI_elements/Debuff buttons.png").convert_alpha()
            health_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "health", (100, HEIGHT//2))
            strength_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "strengthen", (200, HEIGHT//2))
            attack_speed_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "swing", (300, HEIGHT//2))
            speed_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "levelup", (400, HEIGHT//2))

            font = pygame.font.Font("font/Minecraft.ttf", 15*PLAYER_SCALE)
            text = font.render("Choose upgrades", True, WHITE)
            game_manager.screen.blit(text, (WIDTH//2-100*PLAYER_SCALE, HEIGHT//2))

            running_upgrade = True
            while running_upgrade:
                pygame.display.flip()
                health_uppgrade.draw()
                strength_uppgrade.draw()
                attack_speed_uppgrade.draw()
                speed_uppgrade.draw()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_manager.save_settings()
                        exit()
                    if health_uppgrade.handle_event(event):
                        pygame.time.delay(100)
                        player.maxhealth += 20
                        running_upgrade = False
                    if strength_uppgrade.handle_event(event):
                        pygame.time.delay(100)
                        PLAYER_DATA[player_type]['damage'] += 5
                        running_upgrade = False
                    if attack_speed_uppgrade.handle_event(event):
                        pygame.time.delay(100)
                        if player_type ==1:
                            COOLDOWNS['shoot animation'] = 10
                            player.shoot_cooldown = 10
                            running_upgrade = False

                        if player.melee_cooldown > 10 and player_type ==2:
                            player.melee_cooldown - 50
                            running_upgrade = False

                    if speed_uppgrade.handle_event(event):
                        pygame.time.delay(100)
                        new_speed = SPEED_LINEAR * 10 
                        SPEED_LINEAR = new_speed
                        running_upgrade = False
            current_level = player.level
            upgrade_due = False

        else:
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

            if player.level>current_level:
                upgrade_due  = True
            if player.officially_dead:
                print(PLAYER_DATA[player_type]['damage'])
                game_over_screen(player_type)

 
        pygame.display.flip()
        CLOCK.tick(FPS)
    pygame.quit()
    exit()

def start_game(chosen_player):
    global WIDTH,HEIGHT
    """
    Starts the main game initialization.
    """
    game_manager.screen = game_manager.apply_settings()
    WIDTH, HEIGHT = game_manager.update_dimensions()
    initialize_game()
    main_loop(chosen_player)

# Check if this script is being run directly (not imported as a module)
if __name__ == "__main__":
    start_game(1)
    #start_game(chosen_player)