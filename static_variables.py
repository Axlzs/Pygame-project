import pygame 

WIDTH, HEIGHT = 1000, 700
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 100, 100 # Black background size (UNUSED!!)
FPS = 60 # Framerate value for game
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

############MAP_DATA############
TOTAL_BG = 10 # The total number of background images 
BG_CHANCE = [40] + [10] * 4 + [7] * 2 + [3] * 3 # Change probabilities for each image if needed!
################################

#############ENEMY#############
ENEMY_SPAWN_AREA = 200 # Density - distance between inner spawn circle and outer spawn circe 
ENEMY_SPAWN_DISTANCE = 200 # How far does the enemy spawn form the player
ENEMY_SPEED_LINEAR = 2
ENEMY_SPEED_DIAGONAL = 1.414
ENEMY_DATA = {
    1: {'image':'images/players/player1.png','sprite':48,'hitbox_width':16,'hitbox_height':28,'class':1,'health':100,'damage':0,'shoot dist':300},
    2: {'image':'images/players/player2.png','sprite':64,'hitbox_width':10,'hitbox_height':20,'class':2,'health':100,'damage':0,'attack dist':40,'range':10}
}
################################

#############PLAYER#############
SPEED_LINEAR = 4
SPEED_DIAGONAL = 2.828 # Coefficient 0.707 in regards to linear SPEEDSPEED = 4
PLAYER_SCALE = 2 # Scale player
PLAYER_DATA = {
    1: {'image':'images/players/player1.png','sprite':48,'hitbox_width':16,'hitbox_height':28,'class':1,'health':100,'damage':100},
    2: {'image':'images/players/player2.png','sprite':64,'hitbox_width':10,'hitbox_height':20,'class':2,'health':100,'damage':100,'range':20},
    3: ''
}
COOLDOWNS = {'movement':100,'shoot animation':100,'damage':500}
PROJECTILE_COOLDOWN = COOLDOWNS['shoot animation'] *6
MELEE_COOLDOWN = COOLDOWNS['shoot animation'] *5

##########ATTACKS##############
PROJECTILE_DATA = {
    1:{'image':'images/projectiles/iron arrow single.png','hitbox_width':2,'hitbox_height':10},
    2:''
}
PROJECTILE_SPEED = 5
###############################

###########SOME#COLOURS###########
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
MAGENTA, YELLOW = (255, 0, 255), (255, 255, 0)