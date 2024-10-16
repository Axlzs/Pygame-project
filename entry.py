import pygame
import random
import spritesheet

from static_variables import *
from enemyFile import Enemy
from playerFile import *

def set_basic_settings():
    """
    Initializes basic settings for the game.

    Global variables:
        screen: Pygame display surface
        background_surface: Pygame surface for background
        icon: Pygame surface for the game icon
        clock: Pygame clock for controlling the frame rate
        font: Font for the FPS counter
        running: Game status variable (True if the game is running, False if it's not)
        icon_x, icon_y: Initial coordinates of the player icon
    """
    global screen, background_surface, icon, clock, font, running, icon_x, icon_y
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background_surface = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("IKONIKS -- SPĒLES REŽĪMS!")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    running = True
    icon_x, icon_y = (screen.get_width() - PLAYER_WIDTH) / 2, (screen.get_height() - PLAYER_HEIGHT) / 2 

def load_images():
    """
    Load and initialize game images (temporary black background, etc.).

    Global variables:
        black_background: Surface for black background (temporary)
    """
    global iron_arrow_R, iron_arrow_L, iron_arrow_UP, iron_arrow_DOWN
    global health_pickup_image

    iron_arrow_R = pygame.image.load('images/iron arrow R.png')
    iron_arrow_L = pygame.image.load('images/iron arrow L.png')
    iron_arrow_UP = pygame.image.load('images/iron arrow UP.png')
    iron_arrow_DOWN = pygame.image.load('images/iron arrow DOWN.png')


    health_pickup_image = pygame.image.load('images/Item_Black1.png').convert_alpha()
    health_pickup_image = pygame.transform.scale(health_pickup_image, (48, 48))


def load_sound_effects():
    """
    Load and initialize sound effects for the game mode.
    """
    global arrow_shoot, death, enemy_hit, take_potion, level_up
    arrow_shoot = pygame.mixer.Sound('sounds/arrow_shoot.wav')
    death = pygame.mixer.Sound('sounds/death.wav')
    enemy_hit = pygame.mixer.Sound('sounds/enemy_hit.wav')
    take_potion = pygame.mixer.Sound('sounds/take_potion.wav')
    level_up = pygame.mixer.Sound('sounds/level_up.wav')

    take_potion.set_volume(0.3)
    arrow_shoot.set_volume(0.3)
    death.set_volume(0.5)
    enemy_hit.set_volume(0.3)
    level_up.set_volume(0.3)


def load_background_tiles():
    """
    Loads and scales all background tile images from the 'images' directory.
    Populates the global 'background_tiles' list with each tile image.
    Images 'bg-1.png' to 'bg-10.png' are loaded in that order.

    Global variables:
        background_tiles: List of loaded background tile images.
    """
    global background_tiles
    background_tiles = []
    for i in range(1, 11):
        image = pygame.image.load(f'images/bg-{i}.png').convert()
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        background_tiles.append(image)

def select_tile_index():
    """
    Randomly selects an index for a background tile based on predefined probabilities.
    Uses weighted random selection to choose an index, corresponding to a specific background tile.

    Returns:
        integer: The selected tile index.
    """
    chances = [40] + [10] * 4 + [7] * 2 + [3] * 3 # Change probabilities for each image if needed!
    tiles = list(range(10))  # Tile indices from 0 to 9
    return random.choices(tiles, weights=chances, k=1)[0]

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

def game_over_screen():
    """
    Displays the game over screen with interactive buttons.
    """
    global running, score
    mainmenu_rect = pygame.Rect((WIDTH // 2 + 50, HEIGHT // 2 + 280), (300, 100))
    restart_rect = pygame.Rect((WIDTH // 2 - 350, HEIGHT // 2 + 280), (250, 100))

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

def initialize_game():
    """
    Initializes important game functions.
    """
    global tile_grid
    tile_grid = {}  # Dictionary to keep track of which tiles are loaded
    pygame.init()
    # set_static_variables()
    # set_color_codes()
    set_basic_settings()
    load_images()
    load_sound_effects()
    load_background_tiles()
    load_game_over_assets()

# Global dictionary to store enemy damage events
PLAYER_MELE_HIT = {}

# Function to initialize enemy damage events
def init_enemy_damage_events(enemies):
    global BASE_ENEMY_EVENT_ID
    for enemy in enemies:
        PLAYER_MELE_HIT[enemy.id] = BASE_ENEMY_EVENT_ID
        BASE_ENEMY_EVENT_ID += 1

def handle_events():
    """
    Iterates through all Pygame events, such as key presses or closing the game window,
    and updates global variables. 
    
    Handles the QUIT event and KEYUP (last key lifted) event.

    Global variables:
        running: Game status
        last_lift_up: The last key that was released
    """
    global running, last_lift_up, player_health, last_shot_time, current_time, action, frame, score, enemy_count, player_type
    global modifier, player_type

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        elif event.type == pygame.KEYUP:
            last_lift_up = event.key
        elif event.type in ENEMY_HIT_EVENTS.values():
            enemy_type = [enemy_type for enemy_type, event_type in ENEMY_HIT_EVENTS.items() if event_type == event.type][0]
            player_health -= ENEMY_DAMAGE[enemy_type]

        elif event.type in PLAYER_HIT_EVENTS.values():
            # Find the enemy ID associated with the event
            enemy_id = [enemy_id for enemy_id, event_id in PLAYER_HIT_EVENTS.items() if event_id == event.type][0]
            # Find the enemy instance with the corresponding ID
            damaged_enemy = next((enemy for enemy in enemies if enemy.id == enemy_id), None)
            if damaged_enemy:
                # Decrement the health of the damaged enemy
                damaged_enemy.health -= 30
                #damaged_enemy.health -= player.health
                # Optionally, handle enemy destruction or other effects here
                if damaged_enemy.health <=0:
                    enemies.remove(damaged_enemy)
                    score+=1
                    enemy_count-=1  
        if event.type == pygame.KEYDOWN and current_time - last_shot_time >= 400:
            if event.key == pygame.K_SPACE and len(player_arrows_R) < MAX_ARROWS:
                pygame.mixer.Channel(1).play(arrow_shoot)
                arrow_R = pygame.Rect(player.x, player.y + player.height//2 - 2, 10, 5)
                player_arrows_R.append(arrow_R)
                last_shot_time = current_time
            if event.key == pygame.K_SPACE and len(player_arrows_L) < MAX_ARROWS:
                arrow_L = pygame.Rect(player.x, player.y + player.height//2 - 2, 10, 5)
                last_shot_time = current_time
                player_arrows_L.append(arrow_L)
            if event.key == pygame.K_SPACE and len(player_arrows_UP) < MAX_ARROWS:
                arrow_UP = pygame.Rect(player.x + 18, player.y + player.height//2 - 2, 10, 5)
                player_arrows_UP.append(arrow_UP)
                last_shot_time = current_time
            if event.key == pygame.K_SPACE and len(player_arrows_DOWN) < MAX_ARROWS:
                arrow_DOWN = pygame.Rect(player.x + 20, player.y + player.height//2 - 2, 10, 5)
                player_arrows_DOWN.append(arrow_DOWN)
                last_shot_time = current_time
            # if event.key == pygame.K_l: #possibility to end game at any time
            #     print("Death triggered")
            #     frame = 0
            #     action = 12

def move_icon():
    """
    Moves the player based on keyboard inputs.
    Adjusts animations based on keyboard inputs.

    Updates the player's position based on the keys pressed,
    adjusting the speed for diagonal or linear movement. 
    Determines the appropriate animation sequence to use based on the direction of movement.
    """
    global icon_x, icon_y, player, action, frame, animation_completed, last_shot_time, dead, player_health
    keys = pygame.key.get_pressed()

    # Adjust speed based on linear or diagonal movement
    if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
        speed = speed_diagonal  # Reduce speed for diagonal movement
    else:
        speed = speed_linear  # Adjust speed for non-diagonal movement

    # Move the icon based on the pressed keys and use appropriate animations
    if dead == False:
        if keys[pygame.K_s]:
            player.y += speed
            action = 0
            animation_completed = False
        if keys[pygame.K_d]:
            player.x += speed
            action = 2
            animation_completed = False
        if keys[pygame.K_a]:
            player.x -= speed
            action = 1
            animation_completed = False
        if keys[pygame.K_w]:
            player.y -= speed
            action = 3
            animation_completed = False

    if sum(keys) == 0 and last_lift_up != pygame.K_SPACE and dead == False:
        animation_completed = False
        if player_health<100:
            player_health += 0.05 # Player healing while idle
        if last_lift_up == pygame.K_w:
            action = 7
        elif last_lift_up == pygame.K_s:
            action = 4
        elif last_lift_up == pygame.K_a:
            action = 5
        elif last_lift_up == pygame.K_d:
            action = 6

    if keys[pygame.K_SPACE] and not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d] and dead == False:
        animation_completed = False
        if last_lift_up == pygame.K_w:
            action = 11
        elif last_lift_up == pygame.K_s:
            action = 8
        elif last_lift_up == pygame.K_a:
            action = 9
        elif last_lift_up == pygame.K_d:
            action = 10

    if player_health <= 0 and dead == False:
        pygame.mixer.Channel(2).play(death)
        frame = 0 
        action = 12
        dead = True
        print("Player dies")
    
def get_background_tiles():
    """
    Calculates which background tiles are needed based on the player's position.
    The function creates a list of tiles to be drawn, each with its position and
    randomly selected index.
    Ensures that the same tile is not redrawn and maintains a grid of loaded tiles.

    Global variables:
        tile_grid: Dictionary tracking the loaded tiles on the grid.

    Returns:
        list: List of tuples, where each tuple contains the x and y coordinates of the tile
        and the index of the tile image to be used.
    """
    global tile_grid
    tiles = []
    start_x = int(player.x // WIDTH) * WIDTH
    start_y = int(player.y // HEIGHT) * HEIGHT

    for x in range(start_x - WIDTH, start_x + 2 * WIDTH, WIDTH):
        for y in range(start_y - HEIGHT, start_y + 2 * HEIGHT, HEIGHT):
            grid_x, grid_y = x // WIDTH, y // HEIGHT

            # If the tile is not already in the grid, select a new tile
            if (grid_x, grid_y) not in tile_grid:
                tile_index = select_tile_index()
                tile_grid[(grid_x, grid_y)] = tile_index

            tiles.append((x, y, tile_grid[(grid_x, grid_y)]))

    return tiles

def calculate_camera_offset():
    """
    Moves the camera by adjusting coordinates each frame.
    Updates global variables `camera_x` and `camera_y` to determine
    the offset needed for the camera to follow the player while staying centered.
    """
    global camera_x, camera_y
    camera_x = player.x - (WIDTH / 2) + (PLAYER_WIDTH / 3) - 26
    camera_y = player.y - (HEIGHT / 2) + (PLAYER_HEIGHT / 3) - 26

def draw_elements(player_arrows_R, player_arrows_L, player_arrows_UP, player_arrows_DOWN, enemies):

    """
    Draws the necessary background tiles and the player icon on the screen.
    Fetches the required tiles from 'get_background_tiles' and
    then draws them on the screen. 
    It also places the player icon at its current position.

    Global variables:
        background_tiles: List of loaded background tile images.
        animation_list: List of player animation frames.
        action: Current action (animation) for player.
        frame: Current frame for the player animation.
        icon_x, icon_y: Current x and y coordinates of the player.
        camera_x, camera_y: Current x and y coordinates of the camera.
    """

    tiles = get_background_tiles()
    for tile in tiles:
        x, y, tile_index = tile
        screen.blit(background_tiles[tile_index], (x - camera_x, y - camera_y))
    # Update and draw enemies
    for enemy in enemies:
        enemy.animate()
        enemy_screen_x = enemy.rect.x - camera_x
        enemy_screen_y = enemy.rect.y - camera_y
        screen.blit(enemy.image, (enemy_screen_x, enemy_screen_y))
        #ENEMY HITBOX DEBUGGING 
        #pygame.draw.rect(screen, (255, 255, 0), (enemy_screen_x, enemy_screen_y, ENEMY_SIZE[0], ENEMY_SIZE[1]), 2)
    
    # Arrow image drawing
    for arrow_R in player_arrows_R:
        screen.blit(iron_arrow_R, (arrow_R.x - camera_x -25, arrow_R.y - camera_y -27))
    for arrow_L in player_arrows_L:
        screen.blit(iron_arrow_L, (arrow_L.x - camera_x -25, arrow_L.y - camera_y -27))
    for arrow_UP in player_arrows_UP:
        screen.blit(iron_arrow_UP, (arrow_UP.x - camera_x -25, arrow_UP.y - camera_y - 27))
    for arrow_DOWN in player_arrows_DOWN:
        screen.blit(iron_arrow_DOWN, (arrow_DOWN.x - camera_x -29, arrow_DOWN.y - camera_y -27))
    health_bar.draw(screen)

    # ARROW HITBOX DEBUGGING
    # for arrow_R in player_arrows_R:
        # #RIGHT ARROW
        # pygame.draw.rect(screen, (0, 255, 255), (arrow_R.x - camera_x, arrow_R.y - camera_y, arrow_R.width, arrow_R.height), 2) # Blue
    # for arrow_L in player_arrows_L:
        # #LEFT ARROW
        # pygame.draw.rect(screen, (125, 125, 255), (arrow_L.x - camera_x, arrow_L.y - camera_y, arrow_L.width, arrow_L.height), 2) # Blue
    # for arrow_UP in player_arrows_UP:
        # #UP ARROW
        # pygame.draw.rect(screen, (255, 255, 120), (arrow_UP.x - camera_x, arrow_UP.y - camera_y, arrow_UP.width, arrow_UP.height), 2) # Blue
    # for arrow_DOWN in player_arrows_DOWN:
        # #DOWN ARROW
        # pygame.draw.rect(screen, (255, 0, 255), (arrow_DOWN.x - camera_x, arrow_DOWN.y - camera_y, arrow_DOWN.width, arrow_DOWN.height), 2) # Blue


    #DEBUGGING PLAYER HITBOX
    #pygame.draw.rect(screen, (0, 255, 0), (player.x - camera_x, player.y - camera_y, player.width, player.height), 2)

    for pickup in health_pickups:
        screen.blit(health_pickup_image, (pickup.x - camera_x, pickup.y - camera_y -10))
        #DEBUGGING PICKUP HITBOXES
        #pygame.draw.rect(screen, (255, 0, 0), (pickup.x - camera_x, pickup.y - camera_y, pickup.width, pickup.height), 2)


def generate_health_pickup(x, y):
    """
    Generates a health pickup at the specified coordinates.
    """
    health_pickup = pygame.Rect(x + PLAYER_WIDTH/2 - 60, y + PLAYER_HEIGHT/2 - 60, 48, 40)
    health_pickups.append(health_pickup)

def handle_health_pickups():
    """
    Handles the health pickups, ensuring that player health doesn't go above 100.
    """
    global player_health, take_potion, dead
    if dead == True:
        return
    player_health = min(player_health + 50, 100) if any(player.colliderect(pickup) for pickup in health_pickups) else player_health
    for pickup in health_pickups[:]:
        if player.colliderect(pickup):
            pygame.mixer.Channel(3).play(take_potion)
            health_pickups.remove(pickup)

def draw_fading_text(surface, text, position, start_time, duration, color, font):
    """
    Renders faded text based on predefined fadeout time.
    Used for 'Enemy Level-Up' popup.
    """
    current_time = pygame.time.get_ticks()
    time_passed = current_time - start_time

    if time_passed <= duration:
        # Calculate transparency based on time passed
        alpha = max(255 - (255 * time_passed // duration), 0)

        # Render the text
        text_surface = font.render(text, True, color)
        text_surface.set_alpha(alpha)

        # Create a temporary surface with alpha
        temp_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
        temp_surface.blit(text_surface, (0, 0))

        # Blit the temporary surface onto the main surface
        surface.blit(temp_surface, position)


def draw_fps_counter():
    """
    Renders the current frames per second (FPS) on the screen using
    the specified font and displays it at the top-left corner of the game window.
    """
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(fps_text, (10, 10))
    screen.blit(score_text, (10, 45))

def innit_enemy_pathfinding(enemy_x, enemy_y, player, speed_linear, speed_diagonal):
    # Adjust speed based on linear or diagonal movement
    if ((enemy_x > player.x) or (enemy_x < player.x)) and ((enemy_y > player.y) or (enemy_y < player.y)):
        speed = speed_diagonal # Reduce speed for diagonal movement
        
    else:
        speed = speed_linear

    if player.x > enemy_x:
        enemy_x += speed / 2
    if player.x < enemy_x:
        enemy_x -= speed / 2
    if player.y > enemy_y:
        enemy_y += speed / 2 
    if player.y < enemy_y:
        enemy_y -= speed / 2
    
    return enemy_x, enemy_y

def find_player(enemies, player, speed_linear, speed_diagonal):
    for enemy in enemies:
        enemy.rect.x, enemy.rect.y = innit_enemy_pathfinding(enemy.rect.x, enemy.rect.y, player, speed_linear, speed_diagonal)

def player_recieved_damage(player, enemies):
    for enemy in enemies:
        if player.colliderect(enemy.rect):
            pygame.event.post(pygame.event.Event(ENEMY_HIT_EVENTS[enemy.type]))

def player_dealt_damage(player, enemies):
    for enemy in enemies:
        if player.colliderect(enemy.rect):
            # Post the event corresponding to the enemy's ID
            pygame.event.post(pygame.event.Event(PLAYER_MELE_HIT[enemy.id]))

def alive_enemies(enemies):
    alive_count = 0
    for enemy in enemies:
        if enemy.health > 0:
            alive_count += 1
    return alive_count

def add_Random_Enemies(count):
    global enemy_count
    for _ in range(count):
                enemy_type = random.choice(list(ENEMY_IMAGES.keys()))
                enemy_count +=1
                enemy = Enemy(enemy_type, player, enemy_count)
                enemies.add(enemy)
       
def add_Enemies(count, enemytype):
        global enemy_count
        for _ in range(count):
            enemy_type = enemytype
            enemy_count +=1
            enemy = Enemy(enemy_type, player, enemy_count)
            enemies.add(enemy)

def handle_Enemy_Collisions(enemies):
    for enemy in enemies:
        collided_enemies = pygame.sprite.spritecollide(enemy, enemies, False)
        for collided_enemy in collided_enemies:
            if collided_enemy != enemy:  # only if enemy is not itself 
                #move apart when collided 
                if enemy.rect.x < collided_enemy.rect.x:
                    enemy.rect.x -= 1  # Move left
                else:
                    enemy.rect.x += 1  # Move right
                
                if enemy.rect.y < collided_enemy.rect.y:
                    enemy.rect.y -= 1  # Move up
                else:
                    enemy.rect.y += 1  # Move down

def handle_arrows_R(player_arrows_R, action):
    global arrow_R 
    for arrow_R in player_arrows_R[:]:  # Iterate over a copy of the list
        if action == 6 or action == 10 or arrow_R.x > player.x:
            arrow_R.x += ARROW_SPEED
            for enemy in enemies:
                if arrow_R.colliderect(enemy.rect):
                    # Post the event corresponding to the enemy's ID
                    pygame.event.post(pygame.event.Event(PLAYER_MELE_HIT[enemy.id]))
                    try:
                        player_arrows_R.remove(arrow_R)
                    except ValueError:
                        pass
            if arrow_R.x > player.x + 700 or arrow_R.x < player.x - 700:
                try:
                    player_arrows_R.remove(arrow_R)
                except ValueError:
                    pass
        else:
            try:
                player_arrows_R.remove(arrow_R)
            except ValueError:
                pass

def handle_arrows_L(player_arrows_L, action):
    global arrow_L
    for arrow_L in player_arrows_L[:]:
        if action == 5 or action == 9 or arrow_L.x < player.x:
            arrow_L.x -= ARROW_SPEED
            for enemy in enemies:
                if arrow_L.colliderect(enemy.rect):
                    # Post the event corresponding to the enemy's ID
                    pygame.event.post(pygame.event.Event(PLAYER_MELE_HIT[enemy.id]))
                    try:
                        player_arrows_L.remove(arrow_L)
                    except ValueError:
                        pass
            if arrow_L.x > player.x + 700 or arrow_L.x < player.x - 700:
                try:
                    player_arrows_L.remove(arrow_L)
                except ValueError:
                    pass
        else:
            try:
                player_arrows_L.remove(arrow_L)
            except ValueError:
                pass

def handle_arrows_UP(player_arrows_UP, action):
    global arrow_UP
    for arrow_UP in player_arrows_UP[:]:
        if action == 7 or action == 11 or arrow_UP.y < player.y:
            arrow_UP.y -= ARROW_SPEED
            for enemy in enemies:
                if arrow_UP.colliderect(enemy.rect):
                    # Post the event corresponding to the enemy's ID
                    pygame.event.post(pygame.event.Event(PLAYER_MELE_HIT[enemy.id]))
                    try:
                        player_arrows_UP.remove(arrow_UP)
                    except ValueError:
                        pass
            if arrow_UP.y > player.y + 700 or arrow_UP.y < player.y - 700:
                try:
                    player_arrows_UP.remove(arrow_UP)
                except ValueError:
                    pass
        else:
            try:
                player_arrows_UP.remove(arrow_UP)
            except ValueError:
                pass

def handle_arrows_DOWN(player_arrows_DOWN, action):
    global arrow_DOWN
    for arrow_DOWN in player_arrows_DOWN[:]:
        if action == 4 or action == 8 or arrow_DOWN.y > player.y + 40:
            arrow_DOWN.y += ARROW_SPEED
            for enemy in enemies:
                if arrow_DOWN.colliderect(enemy.rect):
                    # Post the event corresponding to the enemy's ID
                    pygame.event.post(pygame.event.Event(PLAYER_MELE_HIT[enemy.id]))
                    try:
                        player_arrows_DOWN.remove(arrow_DOWN)
                    except ValueError:
                        pass
                if arrow_DOWN.y > player.y + 700 or arrow_DOWN.y < player.y - 700:
                    try:
                        player_arrows_DOWN.remove(arrow_DOWN)
                    except ValueError:
                        pass
        else:
            try:
                player_arrows_DOWN.remove(arrow_DOWN)
            except ValueError:
                pass

def handle_arrows_all(player_arrows_R, player_arrows_L, player_arrows_UP, action):
    handle_arrows_R(player_arrows_R, action)
    handle_arrows_L(player_arrows_L, action)
    handle_arrows_UP(player_arrows_UP, action)
    handle_arrows_DOWN(player_arrows_DOWN, action)

class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x 
        self.y = y
        self.w = w 
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, RED, (WIDTH/2 - 23, HEIGHT/2 - 60, 50, 10))
        pygame.draw.rect(screen, GREEN, (WIDTH/2 - 23, HEIGHT/2 - 60, 50 * ratio, 10))
   
def main_loop():
    """
    Runs the main game loop and processes game events.
    The loop continues until the global variable `running` becomes False, and then quits the game.
    """
    global running,player_health, player, health_bar, player_arrows_R, player_arrows_L, player_arrows_UP, player_arrows_DOWN, current_time, dead, frame, action, score
    global enemies
    global health_pickups
    global modifier
    global enemy_speed_linear, enemy_speed_diagonal
    global level_up
    global enemy_count

    health_pickups = []
    health_bar = HealthBar(250, 250, 300, 40, 100)
    player_arrows_R = []
    player_arrows_L = []
    player_arrows_UP = []
    player_arrows_DOWN = []
    # Create player
    player_count = 1
    player_type = 1
    player = Player(player_type, player_count)
    player.create_animation_list()
    
    # Create enemies
    enemies = pygame.sprite.Group()
    enemy_count=0
    for _ in range(300):
        enemy_type = random.choice(list(ENEMY_IMAGES.keys()))
        enemy_count +=1
        enemy = Enemy(enemy_type, player, enemy_count)
        enemies.add(enemy)

    init_enemy_damage_events(enemies)
    score = 0
    modifier = 1

    dead = False

    # Variables for fade-out effect
    start_time = None
    fade_text = ""
    fade_duration = 3000  # Duration of the fade effect in milliseconds (2000 ms = 2 seconds)


    while running:
        current_time = pygame.time.get_ticks()
        # death animation execution
        if frame == 6 and action == 12:
            print("Game over")
            game_over_screen()
            break
        health_bar.hp = player_health

        #spawn more enemies during game
        if enemy_count<100:
            add_Random_Enemies(100)
        handle_events()
        handle_Enemy_Collisions(enemies)
        handle_arrows_all(player_arrows_R, player_arrows_L, player_arrows_UP, action)
        player.update_animation()
        find_player(enemies, player, speed_linear, speed_diagonal)
        move_icon()
        handle_health_pickups()
        calculate_camera_offset()
        player_recieved_damage(player, enemies)
        player_dealt_damage(player, enemies)

        draw_elements(player_arrows_R, player_arrows_L, player_arrows_UP, player_arrows_DOWN, enemies)
        draw_fps_counter()
        
        # Draw fading text if needed
        if start_time is not None:
            draw_fading_text(screen, fade_text, (326, 50), start_time, fade_duration, WHITE, font)
            if current_time - start_time > fade_duration:
                start_time = None  # Reset fade_start_time after the text has faded out

        pygame.display.update()
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