COOLDOWNS = {'movement':1,'idle':1,'shoot animation': 1}

test = {
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
    # 'attack right2': {'row':15,'frames':6,'cooldown':COOLDOWNS['shoot animation']}
    # 'attack up3':    {'row':16,'frames':6,'cooldown':COOLDOWNS['shoot animation']},
    # 'attack left3':  {'row':171,'frames':6,'cooldown':COOLDOWNS['shoot animation']},
    # 'attack down3':  {'row':18,'frames':6,'cooldown':COOLDOWNS['shoot animation']},
    # 'attack right3': {'row':19,'frames':6,'cooldown':COOLDOWNS['shoot animation']}
    'death':        {'row':20,'frames':5,'cooldown':COOLDOWNS['idle']}
        
}
skaits = 0

for action in test.items():
    skaits+=1
    print(skaits)
    print(action)