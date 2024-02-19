import pygame 

WIDTH, HEIGHT = 1000, 700
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 100, 100 # Black background size (UNUSED!!)
PLAYER_WIDTH, PLAYER_HEIGHT = 144, 144 # Attached to some settings in regards to player location on screen
FPS = 60 # Framerate value for game
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
MAX_ARROWS = 10 # Max arrows on screen at a time 
last_shot_time = 0 # Needed to time arrow shots
ARROW_SPEED = 7
speed = 4
speed_linear = 4
speed_diagonal = 2.828 # Coefficient 0.707 in regards to linear speed
enemy_speed_linear = 2
enemy_speed_diagonal = 1.414

############ENEMY############
ENEMY_SPAWN_RANGE = 200
ENEMY_HEALTH = {1: 50, 2: 100, 3: 150}  # Health for each enemy type
ENEMY_HIT_EVENTS = {1: pygame.USEREVENT + 2, 2: pygame.USEREVENT + 3, 3: pygame.USEREVENT + 4}# hit by enemy 
PLAYER_HIT_EVENTS = {1: pygame.USEREVENT + 5, 2: pygame.USEREVENT + 6, 3: pygame.USEREVENT + 7}# hit by player 
ENEMY_SIZE = (144, 144)
ENEMY_HITBOX = (70, 70)
ENEMY_IMAGES = {
    1: 'images/enemy1.png',
    2: 'images/doux_upgrade.png',
    3: 'images/enemy2.png'}
ENEMY_ANIMATION_SPEED = 100  # Milliseconds per frame

###########SOME#COLOURS###########
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
MAGENTA, YELLOW = (255, 0, 255), (255, 255, 0)