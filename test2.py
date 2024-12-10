if ((self.hitbox.x > self.player.hitbox.x) or (self.hitbox.x < self.player.hitbox.x)) and ((self.hitbox.x > self.player.hitbox.y) or (self.hitbox.x < self.player.hitbox.y)):
    speed = speed_diagonal # Reduce speed for diagonal movement
    
else:
    speed = speed_linear
if self.player.hitbox.x > self.hitbox.x:
    self.hitbox.x += speed
if self.player.hitbox.x < self.hitbox.x:
    self.hitbox.x -= speed
if self.player.hitbox.y > self.hitbox.x:
    self.hitbox.x += speed 
if self.player.hitbox.y < self.hitbox.x:
    self.hitbox.x -= speed\
    


dx = self.player.hitbox.centerx - self.rect.centerx # Distance between player.x and enemy.x
dy = self.player.hitbox.centery - self.rect.centery # Distance between player.y and enemy.y
dist = (dx**2 + dy**2) ** 0.5 # Basically pythagoream theorem, straightest path between enemy and player


# Adjust SPEED based on linear or diagonal movement
if dx != 0 and dy != 0:
    SPEED = Static_variables.ENEMY_SPEED_DIAGONAL  # Set speed to diagonal speed if moving diagonally
else:
    SPEED = Static_variables.ENEMY_SPEED_LINEAR  # Use linear speed for straight movements

dx, dy = dx / dist, dy / dist
self.rect.x += dx * SPEED
self.rect.y += dy * SPEED


def navigate_to_player(self, player):
    # Calculate distance to the player
    dx = player.hitbox.centerx - self.rect.centerx
    dy = player.hitbox.centery - self.rect.centery
    dist = (dx**2 + dy**2) ** 0.5

    # Avoid division by zero
    if dist > 0:
        dx, dy = dx / dist, dy / dist  # Normalize direction
    else:
        dx, dy = 0, 0

    # Move the enemy towards the player
    self.rect.x += dx * self.speed
    self.rect.y += dy * self.speed
