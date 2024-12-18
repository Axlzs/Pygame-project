import pygame
import json
import os

class Static_variables:
    CLOCK = pygame.time.Clock()
    FPS = 60 # Framerate value for game
    #WIN = pygame.display.set_mode((WIDTH,HEIGHT)) # idk if it is needed prolly not
    RECT_MODE = False # lets one see rects(hitboxes)
    MIN_WIDTH = 800
    MIN_HEIGHT = 600
    ############MAP_DATA############
    TILE_WIDTH = 640
    TILE_HEIGHT = 640
    TOTAL_BG = 12 # The total number of background images 
    BG_CHANCE = [40, 10, 10, 10, 10, 5, 5, 3, 3, 2, 1, 1]
    #BG_CHANCE = [40] + [10] * 4 + [7] * 2 + [3] * 3 # Change probabilities for each image if needed!
    DROPPABLES = {
        'health': {'image':'images/BigHealthPotion.png','height':24,'width':24,'effect':10},
        'lesser_health': {'image':'images/SmallHealthPotion.png','height':24,'width':24,'effect':5},
        'xp'    : {'image':'images/xp.png','height':18,'width':18,'effect':1},
    }
    POPULATION = ['xp','health','lesser_health','nothing']
    DROPTABLE = [0.6,0.1,0,0.3] # 1:XP 2:HEALTH 3:NOTHING
    LESSER_DROPTABLE = [0.4,0,0.2,0.4]
    ################################

    #############ENEMY#############
    GRID_SIZE = 100 # this is for collision detection
    REPULSION_RADIUS = 20
    REPULSION_FORCE = 2
    ENEMY_SPAWN_AREA = 10 # Density - distance between inner spawn circle and outer spawn circe 
    ENEMY_SPAWN_DISTANCE = 50 # How far does the enemy spawn form the player vision
    LESSER_SPAWN_DISTANCE = 50 # How far does the lesser spawn form the player vision
    ENEMY_SPEED_LINEAR = 2
    ENEMY_SPEED_DIAGONAL = 1.414

    ENEMY_PROJECTILE_COOLDOWN = 1000
    ENEMY_COOLDOWNS = {'idle':100,'movement':100,'shoot animation':100,'damage':500} # animation speed 
    LESSER_ENEMY_COOLDOWNS = 100


    DEFAULT_ENEMY_SPAWN = 10 # Max spawned enemies at the start of the game
    MAX_ENEMY_SPAWN = 100 # Max spawned enemies at a time
    CURRENT_MAX_ENEMIES = DEFAULT_ENEMY_SPAWN # Max apwned enemies at the current game
    MAX_HORDE_SPAWN = 50 # Max enemies that a horde can have 
    MIN_HORDE_SPAWN = 100
    LESSER_ENEMIES = {
        1: {'image':'images/enemies/bat_temp.png','sprite':32,'hitbox_width':10,'hitbox_height':10,'scale':1.3,'class':1,'health':5,'damage':1,'speed':2.5}
    }
    LESSER_ENEMIES_ANIMATION = {
        1: {'move' :    {'row':0,'frames':3,'cooldown':LESSER_ENEMY_COOLDOWNS},
            'death' :   {'row':1,'frames':1,'cooldown':300}}
    }
    ENEMY_DATA = {
        1: {'image':'images/enemies/skeleton_archer.png','sprite':48,'hitbox_width':20,'scale':1,'hitbox_height':35,'class':1,'health':20,'damage':5,'attack_cooldown':1000,'speed':2,'shoot dist':300},
        2: {'image':'images/enemies/lizard_knight.png','sprite':192,'hitbox_width':25,'scale':1,'hitbox_height':50,'class':2,'health':50,'damage':25,'attack_cooldown':500,'speed':1.5,'attack dist':30,'range':15},
        3: {'image':'images/enemies/thief.png','sprite':192,'hitbox_width':20,'scale':0.5,'hitbox_height':35,'class':2,'health':20,'damage':10,'attack_cooldown':100,'speed':2.5,'attack dist':20,'range':10},
        4: {'image':'images/enemies/skeleton_grunt.png','sprite':48,'hitbox_width':20,'scale':1,'hitbox_height':35,'class':2,'health':30,'damage':15,'attack_cooldown':100,'speed':2,'attack dist':22,'range':12},
        5: {'image':'images/enemies/goblin_berserker.png','sprite':48,'hitbox_width':20,'scale':1,'hitbox_height':35,'class':2,'health':20,'damage':20,'attack_cooldown':100,'speed':3,'attack dist':20,'range':10},
    }
    ENEMY_ANIMATION_DATA = {
        1:{
            'walk up':      {'row':0,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk left':    {'row':1,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk down':    {'row':2,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk right':   {'row':3,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},

            'attack up':    {'row':8,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack left':  {'row':9,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack down':  {'row':10,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack right': {'row':11,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},

            'death':        {'row':12,'frames':6,'cooldown':ENEMY_COOLDOWNS['idle']}
        },
        2:{
            'walk up':      {'row':0,'frames':9,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk left':    {'row':1,'frames':9,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk down':    {'row':2,'frames':9,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk right':   {'row':3,'frames':9,'cooldown':ENEMY_COOLDOWNS['movement']},
            
            'attack up':    {'row':5,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack left':  {'row':6,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack down':  {'row':7,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack right': {'row':8,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},

            'death':        {'row':4,'frames':9,'cooldown':ENEMY_COOLDOWNS['idle']}
        },
        3:{
            'walk up':      {'row':0,'frames':9,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk left':    {'row':1,'frames':9,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk down':    {'row':2,'frames':9,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk right':   {'row':3,'frames':9,'cooldown':ENEMY_COOLDOWNS['movement']},
            
            'attack up':    {'row':4,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack left':  {'row':5,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack down':  {'row':6,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack right': {'row':7,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},

            'death':        {'row':8,'frames':9,'cooldown':ENEMY_COOLDOWNS['idle']}
        },
        4:{
            'walk up':      {'row':0,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk left':    {'row':1,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk down':    {'row':2,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk right':   {'row':3,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},

            'attack up':    {'row':8,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack left':  {'row':9,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack down':  {'row':10,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack right': {'row':11,'frames':6,'cooldown':ENEMY_COOLDOWNS['shoot animation']},

            'death':        {'row':12,'frames':6,'cooldown':ENEMY_COOLDOWNS['idle']}
        },
        5:{
            'walk up':      {'row':0,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk left':    {'row':1,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk down':    {'row':2,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},
            'walk right':   {'row':3,'frames':6,'cooldown':ENEMY_COOLDOWNS['movement']},

            'attack up':    {'row':8,'frames':8,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack left':  {'row':9,'frames':8,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack down':  {'row':10,'frames':8,'cooldown':ENEMY_COOLDOWNS['shoot animation']},
            'attack right': {'row':11,'frames':8,'cooldown':ENEMY_COOLDOWNS['shoot animation']},

            'death':        {'row':12,'frames':8,'cooldown':ENEMY_COOLDOWNS['idle']}
        }

        
    }


    ################################

    #############PLAYER#############
    PLAYER_DATA = {
        1: {'image':'images/players/sorceress.png','sprite':48,'hitbox_width':20,'hitbox_height':35,'scale':1,'class':1,'health':50,'damage':8,'default_speed_linear':4,'default_speed_diagonal':2.828},
        
        2: {'image':'images/players/warrior.png','sprite':48,'hitbox_width':15,'hitbox_height':30,'scale':1,'class':2,'health':100,'damage':20,'default_speed_linear':4,'default_speed_diagonal':2.828,'hit_range_width':15,'hit_range_height':15,'heal_factor':5},
        3: ''
    }
    SPEED_LINEAR = 4
    SPEED_DIAGONAL = 2.828 # Coefficient 0.707 in regards to linear SPEEDSPEED = 4
    PLAYER_SCALE = 2 # Scale player
    XP_SCALE = 1.25
    STARTING_XP = 4
    
    ARROW_LIFESPAN = 5000
    COOLDOWNS = {'idle':100,'movement':100,'shoot animation':100,'damage':500}
    PROJECTILE_COOLDOWN = 300
    MELEE_COOLDOWN = COOLDOWNS['shoot animation'] *5 #500
    
    PLAYER_ANIMATION_DATA = {
        1:{
            'walk up':      {'row':0,'frames':6,'cooldown':COOLDOWNS['movement']},
            'walk left':    {'row':1,'frames':6,'cooldown':COOLDOWNS['movement']},
            'walk down':    {'row':2,'frames':6,'cooldown':COOLDOWNS['movement']},
            'walk right':   {'row':3,'frames':6,'cooldown':COOLDOWNS['movement']},

            'stand up':     {'row': 4, 'frames': 6,'cooldown':COOLDOWNS['idle']},
            'stand left':   {'row': 5, 'frames': 6,'cooldown':COOLDOWNS['idle']},
            'stand down':   {'row': 6, 'frames': 6,'cooldown':COOLDOWNS['idle']},
            'stand right':  {'row': 7, 'frames': 6,'cooldown':COOLDOWNS['idle']},
            
            'attack up':    {'row':8,'frames':5,'cooldown':COOLDOWNS['shoot animation']},
            'attack left':  {'row':9,'frames':5,'cooldown':COOLDOWNS['shoot animation']},
            'attack down':  {'row':10,'frames':5,'cooldown':COOLDOWNS['shoot animation']},
            'attack right': {'row':11,'frames':5,'cooldown':COOLDOWNS['shoot animation']},

            'death':        {'row':16,'frames':6,'cooldown':COOLDOWNS['idle']}
        },
        2:{
            'walk up':      {'row':0,'frames':8,'cooldown':COOLDOWNS['movement']},
            'walk left':    {'row':1,'frames':8,'cooldown':COOLDOWNS['movement']},
            'walk down':    {'row':2,'frames':8,'cooldown':COOLDOWNS['movement']},
            'walk right':   {'row':3,'frames':8,'cooldown':COOLDOWNS['movement']},

            'stand up':     {'row': 4, 'frames': 5,'cooldown':COOLDOWNS['idle']},
            'stand left':   {'row': 5, 'frames': 5,'cooldown':COOLDOWNS['idle']},
            'stand down':   {'row': 6, 'frames': 5,'cooldown':COOLDOWNS['idle']},
            'stand right':  {'row': 7, 'frames': 5,'cooldown':COOLDOWNS['idle']},
            
            'attack up':    {'row':8,'frames':6,'cooldown':COOLDOWNS['shoot animation']},
            'attack left':  {'row':9,'frames':6,'cooldown':COOLDOWNS['shoot animation']},
            'attack down':  {'row':10,'frames':6,'cooldown':COOLDOWNS['shoot animation']},
            'attack right': {'row':11,'frames':6,'cooldown':COOLDOWNS['shoot animation']},

            # 'attack up2':    {'row':12,'frames':6,'cooldown':COOLDOWNS['shoot animation']},
            # 'attack left2':  {'row':13,'frames':6,'cooldown':COOLDOWNS['shoot animation']},
            # 'attack down2':  {'row':14,'frames':6,'cooldown':COOLDOWNS['shoot animation']},
            # 'attack right2': {'row':15,'frames':6,'cooldown':COOLDOWNS['shoot animation']},

            'death':        {'row':16,'frames':5,'cooldown':COOLDOWNS['idle']}
        }
    }

    ##########ATTACKS##############
    PROJECTILE_DATA = {
        1:{'image':'images/projectiles/iron arrow single.png','width':48,'height': 5,'hitbox_width':2,'hitbox_height':10},
        2:{'image':'images/projectiles/fire ball.png','width':16,'height': 6,'hitbox_width':2,'hitbox_height':10}
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

    #Debuff buttons
    LESSER_BUTTON_DATA = {
        'thirsty' : {'x':0,'y':0,'width':19,'height':19},
        'levelup' : {'x':38,'y':0,'width':19,'height':19},
        'fire' : {'x':76,'y':0,'width':19,'height':19},

        'health' : {'x':0,'y':19,'width':19,'height':19},
        'ice' : {'x':38,'y':19,'width':19,'height':19},
        'light' : {'x':76,'y':19,'width':19,'height':19},

        'lightning' : {'x':0,'y':38,'width':19,'height':19},
        'magic' : {'x':38,'y':38,'width':19,'height':19},
        'neuron' : {'x':76,'y':38,'width':19,'height':19},

        'poison' : {'x':0,'y':57,'width':19,'height':19},
        'shield' : {'x':38,'y':57,'width':19,'height':19},
        'stars' : {'x':76,'y':57,'width':19,'height':19},

        'strengthen' : {'x':0,'y':76,'width':19,'height':19},
        'sunmoon' : {'x':38,'y':76,'width':19,'height':19},
        'swing' : {'x':76,'y':76,'width':19,'height':19},

        'swirl' : {'x':0,'y':95,'width':19,'height':19},
        'teleport' : {'x':38,'y':95,'width':19,'height':19},
        'weaken' : {'x':76,'y':95,'width':19,'height':19},
    }

    KNOPKAS_DATA = {
        '1': {'x':192,'y':160,'width':32,'height':32},
    }

    ###########SOME#COLOURS###########
    BLACK, WHITE = (0, 0, 0), (255, 255, 255)
    RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
    MAGENTA, YELLOW = (255, 0, 255), (255, 255, 0)
