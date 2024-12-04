I am making a roguelike in pygame and i need some help with droppables. The idea is that some enemies may drop xp and lets say rarely drop health potions also perhaps other stuff in the future. I am not sure how to handle this best. 
The code i have written first uses random.choices to make a weighted decision, when enemy is killed:
#config file
 class Droppable:
    def __init__(self, item_type):
        self.player = Player()
        self.item_type = item_type
        self.screen = game_manager.screen
        self.scale = Static_variables.PLAYER_SCALE
        self.data = Static_variables.DROPPABLES[self.item_type]
        self.amount = self.data["effect"]
        self.position = (0, 0)      # Position where it will appear
        self.scaled_width = int(self.data["width"] * self.scale+30)
        self.scaled_height = int(self.data["height"] * self.scale+30)
        self.image = pygame.transform.scale(self.sprite, (self.scaled_width, self.scaled_height))
        self.rect = self.image.get_rect()

    def load_projectile_sheet(self, item_type, scale):
        projectile_sheet = pygame.image.load(self.data['image']).convert_alpha()
        
        if scale != 1:
            projectile_width, projectile_height = projectile_sheet.get_size()
            scaled_size = (int(projectile_width * scale), int(projectile_height * scale))
            projectile_sheet = pygame.transform.scale(projectile_sheet, scaled_size)
        return projectile_sheet

    def create_projectile_image(self, projectile_sheet):
        # Extract a single frame to use as the base image
        return projectile_sheet.subsurface((0, 0, self.scaled_height, self.scaled_height))

    def set_position(self, x, y):
        self.position = (x, y)

    def update(self):
        self.screen.blit(self.image, self.position)
        if self.player.rect.colliderect(self.rect):
            if self.item_type == "xp":
                self.player.gain_xp(self.amount)
            elif self.item_type == "health":
                self.player.heal(self.amount)
            self.kill
#inside Static_variable class
DROPPABLES = {
    'health': {'image':'images/health_potion.png','height':24,'width':24,'effect':10},
    'xp'    : {'image':'images/xp.png','height':18,'width':18,'effect':1},
}
POPULATION = ['xp','health','nothing']
DROPTABLE = [0.5,0.2,0.3] # 1:XP 2:HEALTH 3:NOTHING 
#inside enemy class (when enemy dies)
if self.is_dying:
    self.image = self.start_animation.play_once()
    if pygame.time.get_ticks() - self.death_start_time >= self.death_duration: #to allow death animation to play out
        self.kill()
        what_drop = random.choices(Static_variables.POPULATION, Static_variables.DROPTABLE)
        if what_drop != 'nothing':
            new_drop = Droppable(what_drop)
            new_drop.set_position(self.rect)