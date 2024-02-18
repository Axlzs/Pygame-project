import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Animation test')

sprite_sheet_image = pygame.image.load('images/player.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

animation_list = []
animation_steps = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
last_update = pygame.time.get_ticks() # Controls animation speed
animation_cooldown = 150
action = 4 # Animation that will be set as default when game starts
frame = 0
step_counter = 0 # Each step is one frame in the animation
animation_completed = False
last_lift_up = pygame.K_s

# Splits the spritesheet into frames
for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 48, 48, 3, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)

run = True
while run:
    
    screen.fill(BG)

    current_time = pygame.time.get_ticks()

    inputs_space = 0

    if current_time - last_update >= animation_cooldown:
        if not animation_completed:
            frame += 1
            last_update = current_time
            if frame >= len(animation_list[action]):
                frame = 0
                animation_completed = True

    screen.blit(animation_list[action][frame], (178, 178))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_s]:
        action = 0
        animation_completed = False
    if keys[pygame.K_d]:
        action = 2
        animation_completed = False
    if keys[pygame.K_a]:
        action = 1
        animation_completed = False
    if keys[pygame.K_w]:
        action = 3
        animation_completed = False
    
    if sum(keys) == 0 and last_lift_up != pygame.K_SPACE:
        animation_completed = False
        if last_lift_up == pygame.K_w:
            action = 7
        elif last_lift_up == pygame.K_s:
            action = 4
        elif last_lift_up == pygame.K_a:
            action = 5
        elif last_lift_up == pygame.K_d:
            action = 6

    if keys[pygame.K_SPACE] and not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d]:
        animation_completed = False
        if last_lift_up == pygame.K_w:
            action = 11
        elif last_lift_up == pygame.K_s:
            action = 8
        elif last_lift_up == pygame.K_a:
            action = 9
        elif last_lift_up == pygame.K_d:
            action = 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYUP:
            last_lift_up = event.key

    pygame.display.update()

pygame.quit()