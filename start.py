import pygame
from static_variables import *
from static_classes import Button
import game  # Game code module


pygame.init()
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("IKONIKS")

def options():
    global screen, fullscreen, WIDTH, HEIGHT
    background1 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/1.png").convert()
    background2 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/2.png").convert_alpha()
    background3 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/3.png").convert_alpha()
    background4 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/4.png").convert_alpha()

    # Scale the background image to match the screen size
    background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
    background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
    background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
    background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))
    
    font = pygame.font.Font("font/Minecraft.ttf", 15*PLAYER_SCALE)
    fullscreen_option = font.render("Fullscreen", True, BLACK)

    back_button = Button(screen, BUTTON_SPRITE_SHEET, "back", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(120*PLAYER_SCALE)))
    yes_button = Button(screen, BUTTON_SPRITE_SHEET, "yes", (WIDTH//5, HEIGHT//10))
    no_button = Button(screen, BUTTON_SPRITE_SHEET, "no", (WIDTH//5, HEIGHT//10))


    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Calculate offsets for each layer based on mouse position
        offset_2 = (mouse_x * 0.01, mouse_y * 0.01)
        offset_3 = (mouse_x * 0.02, mouse_y * 0.02)
        offset_4 = (mouse_x * 0.03, mouse_y * 0.03)  # Most movement

        # Draw layers with parallax effect
        screen.blit(background1, (0,0))
        screen.blit(background2, (-offset_2[0], -offset_2[1]))
        screen.blit(background3, (-offset_3[0], -offset_3[1]))
        screen.blit(background4, (-offset_4[0], -offset_4[1]))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle button events
            if back_button.handle_event(event):
                pygame.time.delay(100)
                running = False
                main_menu()
            if yes_button.handle_event(event):
                fullscreen = True
                screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
            if no_button.handle_event(event):
                fullscreen = False
                screen = pygame.display.set_mode((1000, 700),pygame.RESIZABLE)

        if fullscreen:
            WIDTH, HEIGHT = screen.get_size()
            background1 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/1.png").convert()
            background2 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/2.png").convert_alpha()
            background3 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/3.png").convert_alpha()
            background4 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/4.png").convert_alpha()

            # Scale the background image to match the screen size
            background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
            background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
            background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
            background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))

            font = pygame.font.Font("font/Minecraft.ttf", 15*PLAYER_SCALE)
            fullscreen_option = font.render("Fullscreen", True, BLACK)

            back_button = Button(screen, BUTTON_SPRITE_SHEET, "back", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(120*PLAYER_SCALE)))
            yes_button = Button(screen, BUTTON_SPRITE_SHEET, "yes", (WIDTH//5, HEIGHT//10))
            no_button = Button(screen, BUTTON_SPRITE_SHEET, "no", (WIDTH//5, HEIGHT//10))
            back_button.draw()
            yes_button.draw()
        else:
            WIDTH, HEIGHT = screen.get_size()
            background1 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/1.png").convert()
            background2 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/2.png").convert_alpha()
            background3 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/3.png").convert_alpha()
            background4 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/4.png").convert_alpha()
        
            # Scale the background image to match the screen size
            background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
            background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
            background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
            background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))
            
            font = pygame.font.Font("font/Minecraft.ttf", 15*PLAYER_SCALE)
            fullscreen_option = font.render("Fullscreen", True, BLACK)
        
            back_button = Button(screen, BUTTON_SPRITE_SHEET, "back", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(120*PLAYER_SCALE)))
            yes_button = Button(screen, BUTTON_SPRITE_SHEET, "yes", (WIDTH//5, HEIGHT//10))
            no_button = Button(screen, BUTTON_SPRITE_SHEET, "no", (WIDTH//5, HEIGHT//10))
            no_button.draw()
            back_button.draw()

            


        screen.blit(fullscreen_option,(yes_button.rect.x-80*PLAYER_SCALE, yes_button.rect.midleft[1]))

        pygame.display.flip()
        CLOCK.tick(FPS)

def main_menu():
    start_button = Button(screen, BUTTON_SPRITE_SHEET, "start", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2))
    info_button= Button(screen, BUTTON_SPRITE_SHEET, "info", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(40 *PLAYER_SCALE)))
    option_button = Button(screen, BUTTON_SPRITE_SHEET, "option", (WIDTH//2-(40*PLAYER_SCALE), HEIGHT//2+(80*PLAYER_SCALE)))
    quit_button = Button(screen, BUTTON_SPRITE_SHEET, "quit", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(120*PLAYER_SCALE)))

    background1 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/1.png").convert()
    background2 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/2.png").convert_alpha()
    background3 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/3.png").convert_alpha()
    background4 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/4.png").convert_alpha()

    # Scale the background image to match the screen size
    background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
    background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
    background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
    background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))



    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle button events
            if start_button.handle_event(event):
                pygame.time.delay(100)
                running = False
                game.start_game()
            if info_button.handle_event(event):
                pygame.time.delay(100)
                print("Start button presseed!")
            if option_button.handle_event(event):
                pygame.time.delay(100)
                options()
            if quit_button.handle_event(event):
                pygame.time.delay(100)
                pygame.quit()
                exit()

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate offsets for each layer based on mouse position
        offset_2 = (mouse_x * 0.01, mouse_y * 0.01)
        offset_3 = (mouse_x * 0.02, mouse_y * 0.02)
        offset_4 = (mouse_x * 0.03, mouse_y * 0.03)  # Most movement

        # Draw layers with parallax effect
        screen.blit(background1, (0,0))
        screen.blit(background2, (-offset_2[0], -offset_2[1]))
        screen.blit(background3, (-offset_3[0], -offset_3[1]))
        screen.blit(background4, (-offset_4[0], -offset_4[1]))

        # Draw everything
        start_button.draw()
        info_button.draw()
        option_button.draw()
        quit_button.draw()

        if RECT_MODE:
            pygame.draw.rect(screen, (255, 0, 0), start_button.rect, 2)
            pygame.draw.rect(screen, (255, 0, 0), info_button.rect, 2)
            pygame.draw.rect(screen, (255, 0, 0), option_button.rect, 2)
            pygame.draw.rect(screen, (255, 0, 0), quit_button.rect, 2)

        pygame.display.flip()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main_menu()
            