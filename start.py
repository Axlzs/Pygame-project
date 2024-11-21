import pygame
from static_variables import *
from static_classes import Button
from game_manager import game_manager
import game  # Game code module


pygame.init()


BUTTON_SPRITE_SHEET = pygame.image.load("images/UI_elements/Metal Buttons Text.png").convert_alpha()
def options():
    WIDTH, HEIGHT = game_manager.update_dimensions()
    background1 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/1.png").convert()
    background2 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/2.png").convert_alpha()
    background3 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/3.png").convert_alpha()
    background4 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/4.png").convert_alpha()

    font = pygame.font.Font("font/Minecraft.ttf", 15*PLAYER_SCALE)
    fullscreen_option = font.render("Fullscreen", True, BLACK)

    background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
    background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
    background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
    background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))
    
    back_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "back", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(120*PLAYER_SCALE)))
    yes_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "yes", (WIDTH//5, HEIGHT//10))
    no_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "no", (WIDTH//5, HEIGHT//10))

    running = True
    transitioning = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_manager.save_settings()
                exit()

            # Handle button events
            if back_button.handle_event(event):
                pygame.time.delay(100)
                running = False
                main_menu()

            if transitioning:  # Skip resize events during transitions
                continue

            if yes_button.handle_event(event):
                game_manager.settings["screen_mode"] = "windowed"
                game_manager.screen = game_manager.apply_settings()
                WIDTH, HEIGHT = game_manager.settings["resolution"]
                pygame.time.wait(100)  # Stabilize transition
                pygame.event.clear()  # Clear resize events
                transitioning = False

                # Scale the background image to match the screen size
                background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
                background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
                background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
                background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))

                back_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "back", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(120*PLAYER_SCALE)))
                yes_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "yes", (WIDTH//5, HEIGHT//10))
                no_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "no", (WIDTH//5, HEIGHT//10))
                game_manager.screen.blit(fullscreen_option,(yes_button.rect.x-80*PLAYER_SCALE, yes_button.rect.midleft[1]))

            if no_button.handle_event(event):  # Fullscreen toggle
                transitioning = True
                game_manager.settings["screen_mode"] = "fullscreen"
                game_manager.screen = game_manager.apply_settings()
                pygame.time.wait(100)  # Stabilize transition
                pygame.event.clear()  # Clear resize events
                transitioning = False

                WIDTH, HEIGHT = game_manager.update_dimensions()
                # Scale the background image to match the screen size
                background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
                background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
                background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
                background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))

                back_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "back", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(120*PLAYER_SCALE)))
                yes_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "yes", (WIDTH//5, HEIGHT//10))
                no_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "no", (WIDTH//5, HEIGHT//10))
                game_manager.screen.blit(fullscreen_option,(yes_button.rect.x-80*PLAYER_SCALE, yes_button.rect.midleft[1]))

            elif event.type == pygame.VIDEORESIZE:  # Windowed resize
                if not transitioning:
                    new_width = max(event.w, MIN_WIDTH)
                    new_height = max(event.h, MIN_HEIGHT)
                    game_manager.settings["resolution"] = (new_width, new_height)
                    game_manager.screen = game_manager.apply_settings()
                    WIDTH, HEIGHT = game_manager.update_dimensions()
                # Scale the background image to match the screen size
                background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
                background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
                background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
                background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))

                back_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "back", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(120*PLAYER_SCALE)))
                yes_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "yes", (WIDTH//5, HEIGHT//10))
                no_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "no", (WIDTH//5, HEIGHT//10))
                game_manager.screen.blit(fullscreen_option,(yes_button.rect.x-80*PLAYER_SCALE, yes_button.rect.midleft[1]))

        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Calculate offsets for each layer based on mouse position
        offset_2 = (mouse_x * 0.01, mouse_y * 0.01)
        offset_3 = (mouse_x * 0.02, mouse_y * 0.02)
        offset_4 = (mouse_x * 0.03, mouse_y * 0.03)  # Most movement

        # Draw layers with parallax effect
        game_manager.screen.blit(background1, (0,0))
        game_manager.screen.blit(background2, (-offset_2[0], -offset_2[1]))
        game_manager.screen.blit(background3, (-offset_3[0], -offset_3[1]))
        game_manager.screen.blit(background4, (-offset_4[0], -offset_4[1]))

        if game_manager.settings["screen_mode"] == "fullscreen":
            yes_button.draw()
        else:
            no_button.draw()
        back_button.draw()


        pygame.display.flip()
        CLOCK.tick(FPS)

def main_menu():

    # Main game loop
    WIDTH, HEIGHT = game_manager.update_dimensions()

    background1 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/1.png").convert()
    background2 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/2.png").convert_alpha()
    background3 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/3.png").convert_alpha()
    background4 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/4.png").convert_alpha()
    start_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "start", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2))
    info_button= Button(game_manager.screen, BUTTON_SPRITE_SHEET, "info", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(40 *PLAYER_SCALE)))
    option_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "option", (WIDTH//2-(40*PLAYER_SCALE), HEIGHT//2+(80*PLAYER_SCALE)))
    quit_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "quit", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(120*PLAYER_SCALE)))

    # Scale the background image to match the screen size
    background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
    background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
    background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
    background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_manager.save_settings()
                exit()
            # Handle button events
            if start_button.handle_event(event):
                pygame.time.delay(100)
                game_manager.save_settings()
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
                game_manager.save_settings()
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE: # resizes the screen only when the window acually resizes
                # Enforce minimum resolution
                new_width = max(event.w, MIN_WIDTH)
                new_height = max(event.h, MIN_HEIGHT)
                game_manager.settings["resolution"] = new_width,new_height

                # Apply the adjusted size to the window
                game_manager.screen = game_manager.apply_settings()
                WIDTH, HEIGHT = game_manager.update_dimensions()
                # Scale the background image to match the screen size
                background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
                background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
                background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
                background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))

                start_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "start", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2))
                info_button= Button(game_manager.screen, BUTTON_SPRITE_SHEET, "info", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(40 *PLAYER_SCALE)))
                option_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "option", (WIDTH//2-(40*PLAYER_SCALE), HEIGHT//2+(80*PLAYER_SCALE)))
                quit_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "quit", (WIDTH//2-(32*PLAYER_SCALE), HEIGHT//2+(120*PLAYER_SCALE)))


        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate offsets for each layer based on mouse position
        offset_2 = (mouse_x * 0.01, mouse_y * 0.01)
        offset_3 = (mouse_x * 0.02, mouse_y * 0.02)
        offset_4 = (mouse_x * 0.03, mouse_y * 0.03)  # Most movement

        # Draw layers with parallax effect
        game_manager.screen.blit(background1, (0,0))
        game_manager.screen.blit(background2, (-offset_2[0], -offset_2[1]))
        game_manager.screen.blit(background3, (-offset_3[0], -offset_3[1]))
        game_manager.screen.blit(background4, (-offset_4[0], -offset_4[1]))

        # Draw everything
        start_button.draw()
        info_button.draw()
        option_button.draw()
        quit_button.draw()

        if RECT_MODE:
            pygame.draw.rect(game_manager.screen, (255, 0, 0), start_button.rect, 2)
            pygame.draw.rect(game_manager.screen, (255, 0, 0), info_button.rect, 2)
            pygame.draw.rect(game_manager.screen, (255, 0, 0), option_button.rect, 2)
            pygame.draw.rect(game_manager.screen, (255, 0, 0), quit_button.rect, 2)

        pygame.display.flip()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    game_manager.apply_settings()
    main_menu()
            