import pygame
from static_variables import Static_variables
from static_classes import *
from playerFile import Player
from enemyFile import Enemy, LesserEnemy
from game_manager import game_manager

game_manager.load_settings()
game_manager.apply_settings()
WIDTH,HEIGHT = game_manager.update_dimensions()

BUTTON_SPRITE_SHEET = pygame.image.load("images/UI_elements/Metal Buttons Text.png").convert_alpha()
def load_game_over_assets():
    global WIDTH,HEIGHT
    """
    Load images and sounds for the game over game_manager.screen.
    """

    global background1,background2,background3,background4, backquit_sound, start_sound
    background1 = pygame.image.load("images/UI_elements/Backgrounds/Game_over/1.png").convert()
    background2 = pygame.image.load("images/UI_elements/Backgrounds/Game_over/2.png").convert_alpha()
    background3 = pygame.image.load("images/UI_elements/Backgrounds/Game_over/3.png").convert_alpha()
    background4 = pygame.image.load("images/UI_elements/Backgrounds/Game_over/4.png").convert_alpha()

    # Scale the background image to match the game_manager.screen size
    background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
    background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
    background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
    background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))

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

def pause_screen():

    main_menu = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "mainmenu", (WIDTH // 2 + 32*Static_variables.PLAYER_SCALE, HEIGHT // 2 + 280))
    restart = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "restart", (WIDTH // 2 - 128*Static_variables.PLAYER_SCALE, HEIGHT // 2 + 280))

    font = pygame.font.Font("font/Minecraft.ttf", 15*Static_variables.PLAYER_SCALE)
    text = font.render("Paused - Press 'ESCAPE' to Resume", True, Static_variables.WHITE)
    game_manager.screen.blit(text, (WIDTH//2-128*Static_variables.PLAYER_SCALE, HEIGHT//2))

    running = True
    while running:

        main_menu.draw()
        restart.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running  = False
            # Handle button events
            if main_menu.handle_event(event):
                pygame.time.delay(100)
                game_manager.apply_settings()
                import start
                start.main_menu()
            if restart.handle_event(event):
                pygame.time.delay(100)
                start_game(player.type)

        pygame.display.update()
        Static_variables.CLOCK.tick(Static_variables.FPS)

def game_over_screen():
    """
    Displays the game over game_manager.screen with interactive buttons.
    """

    main_menu = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "mainmenu", (WIDTH // 2 + 32*Static_variables.PLAYER_SCALE, HEIGHT // 2 + 280))
    restart = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "restart", (WIDTH // 2 - 128*Static_variables.PLAYER_SCALE, HEIGHT // 2 + 280))

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

        font = pygame.font.Font("font/Minecraft.ttf", 30*Static_variables.PLAYER_SCALE)
        game_over_font = pygame.font.Font("font/Minecraft.ttf", 50*Static_variables.PLAYER_SCALE)

        total_enemies_killed = player.total_enemies_killed+player.total_lessers_killed
        score_text = font.render(f"TOTAL ENEMIES KILLED: {int(total_enemies_killed)}", True, Static_variables.WHITE)
        game_over_text = game_over_font.render("GAME OVER", True, Static_variables.WHITE)

        game_manager.screen.blit(score_text, ((WIDTH - 400*Static_variables.PLAYER_SCALE) //2, HEIGHT // 2))
        game_manager.screen.blit(game_over_text, ((WIDTH - 285*Static_variables.PLAYER_SCALE) //2, (HEIGHT // 2) - 64*Static_variables.PLAYER_SCALE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Handle button events
            if main_menu.handle_event(event):
                pygame.time.delay(100)
                game_manager.apply_settings()
                import start
                start.main_menu()
            if restart.handle_event(event):
                pygame.time.delay(100)
                player.restart()
                Static_variables.CURRENT_MAX_ENEMIES = Static_variables.DEFAULT_ENEMY_SPAWN
                start_game(player.type)

        pygame.display.update()
        Static_variables.CLOCK.tick(Static_variables.FPS)

def draw_fps_counter():
    """
    Renders the current frames per second (FPS) on the game_manager.screen using
    the specified font and displays it at the top-left corner of the game screendow.
    """
    fps_text = font.render(f"FPS: {int(Static_variables.CLOCK.get_fps())}", True, Static_variables.WHITE)
    game_manager.screen.blit(fps_text, (WIDTH-100, 10)) 
def draw_entities():
    #map stuff
    # visible_tiles = map.get_background_tiles(player.rect, camera.offset)
    # map.render(game_manager.screen, visible_tiles, camera.offset)

    tiles = map.get_background_tiles(player.rect, camera.offset, WIDTH, HEIGHT)
    map.render(game_manager.screen, tiles, camera.offset)
    
    game_manager.screen.blit(player.image, camera.apply(player.rect))
    #player hitbox
    if Static_variables.RECT_MODE:
        player_hitbox = camera.apply(player.hitbox)
        pygame.draw.rect(game_manager.screen, (0, 255, 0), player_hitbox,2)
    
    #projectile stuff 
    for projectile in projectile_group: 
        offset_rect = camera.apply(projectile.rect)
        game_manager.screen.blit(projectile.image, offset_rect)
        #arrow hitbox
        if Static_variables.RECT_MODE:
            pygame.draw.rect(game_manager.screen, (255,0,0), offset_rect,2)
 
    for projectile in enemy_projectile_group:
        offset_rect = camera.apply(projectile.rect)
        game_manager.screen.blit(projectile.image, offset_rect)
        #arrow hitbox
        if Static_variables.RECT_MODE:
            pygame.draw.rect(game_manager.screen, (0,255,0), offset_rect,2)

    for drop in droppable_group:
        offset_rect = camera.apply(drop.rect)
        game_manager.screen.blit(drop.image, offset_rect)
        if Static_variables.RECT_MODE:
            pygame.draw.rect(game_manager.screen, (255, 0, 0), offset_rect, 2)

    for enemy in all_enemies:
        offset_rect = camera.apply(enemy.rect)
        game_manager.screen.blit(enemy.image, offset_rect)

        #mele hitbox
        if Static_variables.RECT_MODE:
            if player.type!=1:
                melee_hitbox = player.get_melee_hitbox()
                pygame.draw.rect(game_manager.screen, (255, 0, 0), camera.apply(enemy.hitbox), 2)
                pygame.draw.rect(game_manager.screen, (255, 0, 0), camera.apply(melee_hitbox), 2)
            else:
                pygame.draw.rect(game_manager.screen, (255, 0, 0), camera.apply(enemy.hitbox), 2)


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

    health_font = pygame.font.Font("font/Minecraft.ttf", 12)
    health_text = health_font.render(str(player.health)+"/"+str(player.maxhealth), True, Static_variables.WHITE)

    health_bar_rect = pygame.Rect(10,10,player.health/player.health_ratio,20)
    transition_bar_rect = pygame.Rect(health_bar_rect.right,10,transition_width,20)

    pygame.draw.rect(game_manager.screen,transition_colour,transition_bar_rect)
    pygame.draw.rect(game_manager.screen,(255,0,0),health_bar_rect)
    pygame.draw.rect(game_manager.screen,(255,255,255),(10,10,player.health_bar_length,20),2)
    game_manager.screen.blit(health_text, (50,15))

def xp_bar(player):
    pygame.draw.rect(game_manager.screen, (0,0,255),(10,31,player.xp/player.xp_bar_ratio,10))
    pygame.draw.rect(game_manager.screen, (255,255,255),(10,31,player.xp_bar_length,10),2)
    lvl_text = font.render(f"LEVEL: {player.level}", True, Static_variables.WHITE)
    game_manager.screen.blit(lvl_text, (12, 45))

def enemy_healthbar_activate(enemy):
    offset_rect = camera.apply(enemy.hitbox)
    pygame.draw.rect(game_manager.screen, (255,0,0),(offset_rect.x,offset_rect.midbottom[1],enemy.health/enemy.health_ratio,5))
    pygame.draw.rect(game_manager.screen, (255,255,255),(offset_rect.x,offset_rect.midbottom[1],enemy.health_bar_length,5),1)

def manual_enemy_spawn(spawned_enemies,player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]: # Manualy spawn enemies 
        enemy_type = random.choice(list(Static_variables.ENEMY_DATA.keys()))
        spawned_enemies +=1
        enemy = Enemy(enemy_type, enemy_projectile_group, player, droppable_group,enemy_projectile_group)
        enemies.add(enemy)
        all_enemies.add(enemy)
    elif keys[pygame.K_k]: # Kill all enemies 
        enemies.empty()
    return spawned_enemies

def enemy_spawn(spawned_enemies,player):
    while spawned_enemies < Static_variables.CURRENT_MAX_ENEMIES:
        spawned_enemies +=1
        enemy_type = random.choice(list(Static_variables.ENEMY_DATA.keys()))
        enemy = Enemy(enemy_type, enemy_projectile_group, player, droppable_group,enemy_projectile_group)
        enemies.add(enemy)
        all_enemies.add(enemy)
    return spawned_enemies

def spawn_horde(all_enemies ,lessers, spawned_lessers, lesser_count, player):
    if lesser_count<100:
        #sqare around the screen - marks the closest position a lesser can spawn
        square_top_left_x = player.hitbox.x - (HEIGHT - Static_variables.LESSER_SPAWN_DISTANCE)
        square_top_left_y = player.hitbox.y - (WIDTH - Static_variables.LESSER_SPAWN_DISTANCE)
        square_bottom_right_x = player.hitbox.x + (HEIGHT + Static_variables.LESSER_SPAWN_DISTANCE)
        square_bottom_right_y = player.hitbox.y + (WIDTH + Static_variables.LESSER_SPAWN_DISTANCE)
        while True:
            # Generate random x and y coordinates on the outside of the square
            center_x = random.uniform(square_top_left_x - Static_variables.ENEMY_SPAWN_AREA, square_bottom_right_x + Static_variables.ENEMY_SPAWN_AREA)
            center_y = random.uniform(square_top_left_y - Static_variables.ENEMY_SPAWN_AREA, square_bottom_right_y + Static_variables.ENEMY_SPAWN_AREA)

            # Check if the generated point is outside the square
            if center_x < square_top_left_x or center_x > square_bottom_right_x or center_y < square_top_left_y or center_y > square_bottom_right_y:
                #return (center_x, center_y)
                break
    
        new_lessers = random.randint(Static_variables.MIN_HORDE_SPAWN,Static_variables.MIN_HORDE_SPAWN)
        spawned_lessers += new_lessers
        enemy_type = random.choice(list(Static_variables.LESSER_ENEMIES.keys()))
        for _ in range(new_lessers):
            x = random.uniform(center_x - Static_variables.ENEMY_SPAWN_AREA//2, center_x + Static_variables.ENEMY_SPAWN_AREA//2)
            y = random.uniform(center_y - Static_variables.ENEMY_SPAWN_AREA//2, center_y + Static_variables.ENEMY_SPAWN_AREA//2)
            enemy = LesserEnemy(enemy_type,player,droppable_group,x,y)
            lessers.add(enemy)
            all_enemies.add(enemy)
    return spawned_lessers, lesser_count,spawned_lessers

def upgrade_screen(player_type):
    BUTTON_SPRITE_SHEET = pygame.image.load("images/UI_elements/Debuff buttons.png").convert_alpha()
    health_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "health", (WIDTH//2-57*Static_variables.PLAYER_SCALE, HEIGHT//2 +98*Static_variables.PLAYER_SCALE))
    strength_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "strengthen", (WIDTH//2-57*Static_variables.PLAYER_SCALE, HEIGHT//2 +49*Static_variables.PLAYER_SCALE))
    attack_speed_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "swing", (WIDTH//2-57*Static_variables.PLAYER_SCALE, HEIGHT//2))
    speed_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "levelup", (WIDTH//2-57*Static_variables.PLAYER_SCALE, HEIGHT//2 -49*Static_variables.PLAYER_SCALE))

    upgrade_font = pygame.font.Font("font/Minecraft.ttf", 15*Static_variables.PLAYER_SCALE)
    icon_font = pygame.font.Font("font/Minecraft.ttf", 19*Static_variables.PLAYER_SCALE)
    upgrade_text = upgrade_font.render("Choose upgrades", True, Static_variables.WHITE)
    health_text = icon_font.render("Health upgrade", True, Static_variables.WHITE)
    strength_text = icon_font.render("Damage upgrade", True, Static_variables.WHITE)
    attack_speed_text = icon_font.render("Increase attack speed", True, Static_variables.WHITE)
    speed_text = icon_font.render("Increase Movement speed ", True, Static_variables.WHITE)

    game_manager.screen.blit(upgrade_text, (WIDTH//2-75*Static_variables.PLAYER_SCALE, HEIGHT//2 -100*Static_variables.PLAYER_SCALE))
    game_manager.screen.blit(health_text, (WIDTH//2-19*Static_variables.PLAYER_SCALE, HEIGHT//2 +107*Static_variables.PLAYER_SCALE))
    game_manager.screen.blit(strength_text, (WIDTH//2-19*Static_variables.PLAYER_SCALE, HEIGHT//2 +58*Static_variables.PLAYER_SCALE))
    game_manager.screen.blit(attack_speed_text, (WIDTH//2-19*Static_variables.PLAYER_SCALE, HEIGHT//2+9*Static_variables.PLAYER_SCALE))
    game_manager.screen.blit(speed_text, (WIDTH//2-19*Static_variables.PLAYER_SCALE, HEIGHT//2 -40*Static_variables.PLAYER_SCALE))
    

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

            #Health and regen upgrade
            if health_uppgrade.handle_event(event):
                pygame.time.delay(100)
                player.maxhealth += 5
                player.heal(5)
                player.health_ratio = player.maxhealth/player.health_bar_length
                if player.type ==2:
                    player.heal_factor+=3
                running = False

            #Strength upgrade
            if strength_uppgrade.handle_event(event):
                pygame.time.delay(100)
                player.dealing_damage += 5
                running = False

            #Attack speed upgrade
            if attack_speed_uppgrade.handle_event(event):
                pygame.time.delay(100)
                if player_type ==1 and player.shoot_cooldown > 30:
                    player.shoot_cooldown = 10

                if player_type ==2 and player.melee_cooldown > 10:
                    player.melee_cooldown = 10
                
                player.upgrade_attack_speed(1.2)
                running = False
            #Running speed upgrade
            if speed_uppgrade.handle_event(event):
                pygame.time.delay(100)
                player.speed_linear *= 1.2
                player.speed_diagonal *= 1.2
                player.upgrade_movement_speed(1.2)



                running = False
            player.heal(5)
        pygame.display.update()
        Static_variables.CLOCK.tick(Static_variables.FPS)

#################################ENEMY#COLLISION#REPULSION#############################################     
def assign_to_grid(all_enemies):
    grid = {}
    for enemy in all_enemies:
        # make a grid for each enemy 
        cell_x = enemy.rect.centerx // Static_variables.GRID_SIZE
        cell_y = enemy.rect.centery // Static_variables.GRID_SIZE
        cell = (cell_x, cell_y)

        if cell not in grid:
            grid[cell] = []
        grid[cell].append(enemy)

    return grid

def handle_repulsion_with_grid(all_enemies):
    grid = assign_to_grid(all_enemies)

    # Iterate over each grid cell and its neighbors
    for cell, enemies in grid.items():
        neighbors = [
            (cell[0] + dx, cell[1] + dy)
            for dx in range(-1, 2)  # Neighbor cells in x
            for dy in range(-1, 2)  # Neighbor cells in y
        ]

        if Static_variables.RECT_MODE:
            if enemies:  # If the cell has enemies
                # Calculate cell top-left corner
                cell_xx = cell[0] * Static_variables.GRID_SIZE
                cell_yy = cell[1] * Static_variables.GRID_SIZE
                cell_x,cell_y = camera.apply_tuple((cell_xx,cell_yy))

                # Draw a semi-transparent rectangle
                highlight_color = (255, 0, 0, 100)  # Red with transparency
                s = pygame.Surface((Static_variables.GRID_SIZE, Static_variables.GRID_SIZE), pygame.SRCALPHA)  # Create a transparent surface
                s.fill(highlight_color)
                game_manager.screen.blit(s, (cell_x, cell_y))

        # Combine enemies from current cell and neighbors
        nearby_enemies = []
        for neighbor in neighbors:
            if neighbor in grid:
                nearby_enemies.extend(grid[neighbor])

        # Repulsion logic for enemies in the current cell and nearby cells
        for i, enemy in enumerate(enemies):
            for j in range(i + 1, len(nearby_enemies)):
                other = nearby_enemies[j]
                if enemy is other:
                    continue

                # Calculate repulsion force (same as before)
                dx = other.rect.centerx - enemy.rect.centerx
                dy = other.rect.centery - enemy.rect.centery
                dist = (dx**2 + dy**2) ** 0.5

                if dist < Static_variables.REPULSION_RADIUS and dist > 0:
                    force = Static_variables.REPULSION_FORCE / dist
                    repulsion_dx = dx * force
                    repulsion_dy = dy * force

                    enemy.rect.x -= repulsion_dx
                    enemy.rect.y -= repulsion_dy
                    other.rect.x += repulsion_dx
                    other.rect.y += repulsion_dy
##############################################################################     

def main_loop(chosen_player):
    global projectile_group, enemy_projectile_group, droppable_group
    global enemies,lessers,all_enemies
    global player,camera,map
    global last_enemy_spawn,spawned_enemies,lesser_count,spawned_lessers
    global player_type
    #WIDTH, HEIGHT = game_manager.update_dimensions()
    #setting up game
    last_enemy_spawn = 0
    projectile_group = pygame.sprite.Group()
    droppable_group = pygame.sprite.Group()
    enemy_projectile_group = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    lessers = pygame.sprite.Group()  # lesser enemies
    all_enemies = pygame.sprite.Group()
    player_type=chosen_player 
    player = Player(player_type, projectile_group, enemy_projectile_group, all_enemies, droppable_group)  # Pass the appropriate player type here
    
    camera = Camera()
    map = WorldMap(Static_variables.TILE_WIDTH, Static_variables.TILE_HEIGHT)

    current_level = player.level
    spawned_enemies = 0 # all spawned enemies 
    spawned_enemies = enemy_spawn(spawned_enemies, player)

    spawned_lessers = 0
    lesser_count = 0
    upgrade_due = False

    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:   # Esc - pause game 
                paused = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:       # ↑ - level up player 
                player.level +=1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:    # → - heal player 10 hp
                player.heal(10)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:     # ← - player takes 25 hp damage  
                player.take_damage(25)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:        # L - die
                player.start_death_sequence()
                player.health = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:        # R - see all of the hitboxes 
                Static_variables.RECT_MODE = not Static_variables.RECT_MODE 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:        # 1 - see some enemy data
                print('regular enemies:', spawned_enemies,'spawned lesser enemies:',spawned_lessers, 'max enemies:', Static_variables.CURRENT_MAX_ENEMIES)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:        # 2 - spawn horde of lesser enemies ( stress test)
                spawned_lessers,lesser_count,spawned_lessers = spawn_horde(all_enemies,lessers,spawned_lessers,lesser_count,player)
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.handle_attack()
    
        lesser_count = spawned_lessers - player.total_lessers_killed
    ##############FUNCTIONS##############
        if paused:

            pause_screen()
            paused = False

        elif upgrade_due:

            upgrade_screen(player_type)
            current_level = player.level
            upgrade_due = False
            spawned_lessers,lesser_count,spawned_lessers = spawn_horde(all_enemies,lessers,spawned_lessers,lesser_count,player)
            Static_variables.CURRENT_MAX_ENEMIES = min(Static_variables.CURRENT_MAX_ENEMIES +2 , Static_variables.MAX_ENEMY_SPAWN)       
            spawned_enemies = enemy_spawn(spawned_enemies, player)
            
        else:

            player.update()
            enemies.update()
            lessers.update()
            camera.update(player.rect)
            projectile_group.update()
            enemy_projectile_group.update()
            droppable_group.update()
            draw_entities()
            draw_fps_counter() 
            spawned_enemies = manual_enemy_spawn(spawned_enemies,player)
            player_healthbar_activate(player)
            xp_bar(player)
            for enemy in enemies:
                enemy_healthbar_activate(enemy)   

            handle_repulsion_with_grid(all_enemies)
            if player.level>current_level:
                upgrade_due  = True
            if player.officially_dead:
                game_over_screen()
 
        pygame.display.flip()
        Static_variables.CLOCK.tick(Static_variables.FPS)
    pygame.quit()
    exit()

def start_game(chosen_player):
    global WIDTH,HEIGHT
    """
    Starts the main game initialization.
    """
    WIDTH, HEIGHT = game_manager.update_dimensions()
    initialize_game()
    main_loop(chosen_player)

# Basically if the game is run from this file, then this will be executed first(since there is no chosen_player in this situation, the player is hard coded)
if __name__ == "__main__":
    start_game(1)