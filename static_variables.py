import pygame
import json
import os

CLOCK = pygame.time.Clock()
FPS = 60 # Framerate value for game
#WIN = pygame.display.set_mode((WIDTH,HEIGHT)) # idk if it is needed prolly not
RECT_MODE = False # lets one see rects(hitboxes)
MIN_WIDTH = 800
MIN_HEIGHT = 600
############MAP_DATA############
TILE_WIDTH = 800
TILE_HEIGHT = 600
TOTAL_BG = 10 # The total number of background images 
BG_CHANCE = [40] + [10] * 4 + [7] * 2 + [3] * 3 # Change probabilities for each image if needed!
################################

#############ENEMY#############
ENEMY_SPAWN_AREA = 200 # Density - distance between inner spawn circle and outer spawn circe 
ENEMY_SPAWN_DISTANCE = 250 # How far does the enemy spawn form the player
ENEMY_SPEED_LINEAR = 2
ENEMY_SPAWN_COOLDOWN = 500
ENEMY_SPEED_DIAGONAL = 1.414
ENEMY_DATA = {
    1: {'image':'images/players/player1.png','sprite':48,'hitbox_width':16,'hitbox_height':28,'class':1,'health':20,'damage':10,'shoot dist':300},
    2: {'image':'images/players/player2.png','sprite':64,'hitbox_width':10,'hitbox_height':20,'class':2,'health':20,'damage':10,'attack dist':40,'range':20}
}
ENEMY_PROJECTILE_COOLDOWN = 1000
################################

#############PLAYER#############
SPEED_LINEAR = 4
SPEED_DIAGONAL = 2.828 # Coefficient 0.707 in regards to linear SPEEDSPEED = 4
PLAYER_SCALE = 2 # Scale player
XP_SCALE = 1.25
STARTING_XP = 4
PLAYER_DATA = {
    1: {'image':'images/players/player1.png','sprite':48,'hitbox_width':16,'hitbox_height':28,'class':1,'health':100,'damage':100},
    2: {'image':'images/players/player2.png','sprite':64,'hitbox_width':10,'hitbox_height':20,'class':2,'health':100,'damage':100,'range':20},
    3: ''
}
COOLDOWNS = {'movement':100,'shoot animation':100,'damage':500}
PROJECTILE_COOLDOWN = 300
MELEE_COOLDOWN = COOLDOWNS['shoot animation'] *5 #500


##########ATTACKS##############
PROJECTILE_DATA = {
    1:{'image':'images/projectiles/iron arrow single.png','hitbox_width':2,'hitbox_height':10},
    2:''
}
PROJECTILE_SPEED = 5
###############################

##########BUTTONS##############
BUTTON_DATA = {
    'start' : {'x':0,'y':0,'width':64,'height':32},
    'play' : {'x':0,'y':32,'width':64,'height':32},
    'pause' : {'x':0,'y':64,'width':64,'height':32},
    'menu' : {'x':0,'y':96,'width':64,'height':32},
    'save' : {'x':0,'y':128,'width':64,'height':32},
    'load' : {'x':0,'y':160,'width':64,'height':32},
    'quit' : {'x':0,'y':192,'width':64,'height':32},
    'shop' : {'x':0,'y':224,'width':64,'height':32},
    'rate' : {'x':0,'y':256,'width':64,'height':32},
    'next' : {'x':0,'y':288,'width':64,'height':32},
    'back' : {'x':0,'y':320,'width':64,'height':32},
    'sell' : {'x':0,'y':354,'width':64,'height':32},
    'buy' : {'x':0,'y':384,'width':64,'height':32},

    'no' : {'x':192,'y':0,'width':64,'height':32},
    'yes' : {'x':192,'y':32,'width':64,'height':32},
    'get' : {'x':192,'y':64,'width':64,'height':32},
    'new' : {'x':192,'y':96,'width':64,'height':32},
    'more' : {'x':192,'y':128,'width':64,'height':32},
    'mute' : {'x':192,'y':160,'width':64,'height':32},
    'info' : {'x':192,'y':192,'width':64,'height':32},
    'close' : {'x':192,'y':224,'width':64,'height':32},
    'level' : {'x':192,'y':256,'width':64,'height':32},
    'power' : {'x':192,'y':288,'width':64,'height':32},
    'score' : {'x':192,'y':320,'width':64,'height':32},
    'music' : {'x':192,'y':354,'width':64,'height':32},
    'high' : {'x':192,'y':374,'width':64,'height':32},

    'credits' : {'x':384,'y':0,'width':80,'height':32},
    'restart' : {'x':384,'y':32,'width':80,'height':32},
    'option' : {'x':384,'y':64,'width':80,'height':32},
    'cancel' : {'x':384,'y':96,'width':80,'height':32},
    'continue' : {'x':384,'y':128,'width':96,'height':32},
    'gameover' : {'x':384,'y':160,'width':96,'height':32},
    'mainmenu' : {'x':384,'y':192,'width':96,'height':32},
    'inventory' : {'x':384,'y':224,'width':96,'height':32},
    'equipment' : {'x':384,'y':256,'width':96,'height':32},
    'completed' : {'x':384,'y':288,'width':96,'height':32},
    'collection' : {'x':384,'y':320,'width':112,'height':32},
    'achievement' : {'x':384,'y':354,'width':128,'height':32},
    'leaderboards' : {'x':384,'y':374,'width':128,'height':32},
}

KNOPKAS_DATA = {
    '1': {'x':192,'y':160,'width':32,'height':32},
}

###########SOME#COLOURS###########
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
MAGENTA, YELLOW = (255, 0, 255), (255, 255, 0)