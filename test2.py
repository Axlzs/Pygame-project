import pygame

def enemy_actions(self):

    self.motion = False
    
    dx = self.player.rect.centerx - self.rect.centerx # Distance between player.x and enemy.x
    dy = self.player.rect.centery - self.rect.centery # Distance between player.y and enemy.y
    dist = (dx**2 + dy**2) ** 0.5 # Basically pythagoream theorem, straightest path between enemy and player

    # Adjust SPEED based on linear or diagonal movement
    if dx != 0 and dy != 0:
        SPEED = SPEED_DIAGONAL  # Set speed to diagonal speed if moving diagonally
    else:
        SPEED = SPEED_LINEAR  # Use linear speed for straight movements

    # Understanding which way should the enemy face
    if dy < 0:
        self.motion = True
        self.direction = 'up'
    else:
        self.motion = True
        self.direction = 'down'
    if dx < 0:
        self.motion = True
        self.direction = 'left'
    else:
        self.motion = True
        self.direction = 'right'

    # Handling movement - moving enemy
    if dist > 0:
        dx, dy = dx / dist, dy / dist
        self.rect.x += dx * SPEED
        self.rect.y += dy * SPEED

    # Calling animations 
    if self.shooting:
        self.start_animation = self.animations[f'shoot {self.direction}']
    elif self.motion:
        self.start_animation = self.animations[f'walk {self.direction}']
    else:
        self.start_animation = self.animations[f'stand {self.direction}']