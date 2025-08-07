import pygame
from static_variables import Static_variables
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

    font = pygame.font.Font("font/Minecraft.ttf", 15*Static_variables.PLAYER_SCALE)
    fullscreen_option = font.render("Fullscreen", True, Static_variables.BLACK)

    background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
    background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
    background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
    background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))
    
    back_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "back", (WIDTH//2-(32*Static_variables.PLAYER_SCALE), HEIGHT//2+(120*Static_variables.PLAYER_SCALE)))
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
                transitioning = True
                game_manager.settings["screen_mode"] = "windowed"
                game_manager.screen = game_manager.apply_settings()
                pygame.time.wait(100)  # Stabilize transition
                pygame.event.clear()  # Clear resize events
                transitioning = False
                WIDTH, HEIGHT = game_manager.settings["resolution"]

                # Scale the background image to match the screen size
                background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
                background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
                background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
                background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))

                back_button.pos = (WIDTH//2-(32*Static_variables.PLAYER_SCALE), HEIGHT//2+(120*Static_variables.PLAYER_SCALE))
                yes_button.pos = (WIDTH//5, HEIGHT//10)
                no_button.pos = (WIDTH//5, HEIGHT//10)
                game_manager.screen.blit(fullscreen_option,(yes_button.rect.x-80*Static_variables.PLAYER_SCALE, yes_button.rect.midleft[1]))

            elif no_button.handle_event(event):  # Fullscreen toggle
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

                back_button.pos = (WIDTH//2-(32*Static_variables.PLAYER_SCALE), HEIGHT//2+(120*Static_variables.PLAYER_SCALE))
                #yes_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "yes", (WIDTH//5, HEIGHT//10))
                no_button.pos = (WIDTH//5, HEIGHT//10)

            elif event.type == pygame.VIDEORESIZE:  # Windowed resize
                if not transitioning:
                    new_width = max(event.w, Static_variables.MIN_WIDTH)
                    new_height = max(event.h, Static_variables.MIN_HEIGHT)
                    game_manager.settings["resolution"] = (new_width, new_height)
                    game_manager.screen = game_manager.apply_settings()
                    WIDTH, HEIGHT = game_manager.update_dimensions()
                # Scale the background image to match the screen size
                background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
                background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
                background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
                background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))

                back_button.pos = (WIDTH//2-(32*Static_variables.PLAYER_SCALE), HEIGHT//2+(120*Static_variables.PLAYER_SCALE))
                yes_button.pos = (WIDTH//5, HEIGHT//10)
                no_button.pos = (WIDTH//5, HEIGHT//10)


        
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

        game_manager.screen.blit(fullscreen_option,(yes_button.rect.x-80*Static_variables.PLAYER_SCALE, yes_button.rect.midleft[1]))

        if game_manager.settings["screen_mode"] == "fullscreen":
            no_button.set_disabled(True)
            yes_button.set_disabled(False)
            yes_button.draw()
        else:
            no_button.set_disabled(False)
            yes_button.set_disabled(True)
            no_button.draw()
        back_button.draw()


        pygame.display.flip()
        Static_variables.CLOCK.tick(Static_variables.FPS)

def choose_player():
    WIDTH, HEIGHT = game_manager.update_dimensions()

    background1 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/1.png").convert()
    background2 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/2.png").convert_alpha()
    background3 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/3.png").convert_alpha()
    background4 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/4.png").convert_alpha()
    start_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "start", (WIDTH//2-(40*Static_variables.PLAYER_SCALE), 480))
    back_button= Button(game_manager.screen, BUTTON_SPRITE_SHEET, "back", (WIDTH//2-(40*Static_variables.PLAYER_SCALE), HEIGHT//2+(120*Static_variables.PLAYER_SCALE)))

    player1_sheet = pygame.image.load("images/players/sorceress.png").convert_alpha()
    player2_sheet = pygame.image.load("images/players/warrior.png").convert_alpha()

    player1_base_frame = player1_sheet.subsurface((0, 96, 48, 48))
    player2_base_frame = player2_sheet.subsurface((0, 96, 48, 48))

    player1_frame = pygame.transform.scale(player1_base_frame, (240, 240))
    player2_frame = pygame.transform.scale(player2_base_frame, (240, 240))

    player1_rect = pygame.Rect(WIDTH/2-150,240,120,200) # 240
    player2_rect = pygame.Rect(WIDTH/2-10,240,120,200) # 240

    player1_selected = False
    player2_selected = False
    player_choice = 0

    game_manager.screen.blit(player1_frame, (WIDTH/2-280, 0))
    game_manager.screen.blit(player2_frame, (WIDTH/2-160, 0))

    shadow_color = (100,100,100,100)
    selected_shadow_color = (0,0,0,100)
    shadow1 = pygame.Surface((120, 200), pygame.SRCALPHA)
    shadow2 = pygame.Surface((120, 200), pygame.SRCALPHA)

    shadow1.fill(shadow_color)
    shadow2.fill(shadow_color)
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
                game_manager.save_settings()
                pygame.time.delay(100)
                if player1_selected:
                    running = False
                    game.start_game(1)
                elif player2_selected:
                    running = False
                    game.start_game(2)
                else:
                    continue
            if back_button.handle_event(event):
                pygame.time.delay(100)
                game_manager.apply_settings()
                main_menu()

            if event.type == pygame.VIDEORESIZE: # resizes the screen only when the window acually resizes
                # Enforce minimum resolution
                new_width = max(event.w, Static_variables.MIN_WIDTH)
                new_height = max(event.h, Static_variables.MIN_HEIGHT)
                game_manager.settings["resolution"] = new_width,new_height

                # Apply the adjusted size to the window
                game_manager.screen = game_manager.apply_settings()
                WIDTH, HEIGHT = game_manager.update_dimensions()
                # Scale the background image to match the screen size
                background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
                background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
                background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
                background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))

                # # start_button.pos = (WIDTH//2-(40*Static_variables.PLAYER_SCALE), HEIGHT//2+(80*Static_variables.PLAYER_SCALE))
                start_button.pos = WIDTH//2-(40*Static_variables.PLAYER_SCALE), 480
                back_button.pos = (WIDTH//2-(32*Static_variables.PLAYER_SCALE), HEIGHT//2+(120*Static_variables.PLAYER_SCALE))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check for mouse click inside the rectangle
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if player1_rect.collidepoint(mouse_x, mouse_y):
                        player1_selected = not player1_selected
                        player2_selected = False
                    elif player2_rect.collidepoint(mouse_x, mouse_y):
                        player2_selected = not player2_selected
                        player1_selected = False

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

        game_manager.screen.blit(shadow1,player1_rect)
        game_manager.screen.blit(shadow2,player2_rect)
        game_manager.screen.blit(player1_frame, (WIDTH/2 -210, 230))
        game_manager.screen.blit(player2_frame, (WIDTH/2 -70, 240))

        if player1_selected:
            pygame.draw.rect(game_manager.screen, Static_variables.GREEN, player1_rect, 5)
            shadow1.fill(selected_shadow_color)
            player_choice = 1
        else:
            pygame.draw.rect(game_manager.screen, Static_variables.RED, player1_rect, 5)
            shadow1.fill(shadow_color)
        if player2_selected:
            pygame.draw.rect(game_manager.screen, Static_variables.GREEN, player2_rect, 5)
            shadow2.fill(selected_shadow_color)
            player_choice = 2
        else:
            pygame.draw.rect(game_manager.screen, Static_variables.RED, player2_rect, 5)
            shadow2.fill(shadow_color)

        # Draw everything
        start_button.draw()
        back_button.draw()

        if Static_variables.RECT_MODE:
            pygame.draw.rect(game_manager.screen, (255, 0, 0), start_button.rect, 2)
            pygame.draw.rect(game_manager.screen, (255, 0, 0), back_button.rect, 2)

        pygame.display.flip()
        Static_variables.CLOCK.tick(Static_variables.FPS)

def main_menu():

    # Main game loop
    WIDTH, HEIGHT = game_manager.update_dimensions()

    background1 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/1.png").convert()
    background2 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/2.png").convert_alpha()
    background3 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/3.png").convert_alpha()
    background4 = pygame.image.load("images/UI_elements/Backgrounds/Main_menu/4.png").convert_alpha()
    #start_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "start", (WIDTH//2-(32*Static_variables.PLAYER_SCALE), HEIGHT//2))
    start_button= Button(game_manager.screen, BUTTON_SPRITE_SHEET, "start", (WIDTH//2-(32*Static_variables.PLAYER_SCALE), HEIGHT//2+(40 *Static_variables.PLAYER_SCALE)))
    option_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "option", (WIDTH//2-(40*Static_variables.PLAYER_SCALE), HEIGHT//2+(80*Static_variables.PLAYER_SCALE)))
    quit_button = Button(game_manager.screen, BUTTON_SPRITE_SHEET, "quit", (WIDTH//2-(32*Static_variables.PLAYER_SCALE), HEIGHT//2+(120*Static_variables.PLAYER_SCALE)))

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
                
                if game_manager.settings["screen_mode"] == "fullscreen":
                    pass
                else:
                    WIDTH, HEIGHT = game_manager.update_dimensions()
                    game_manager.screen = pygame.display.set_mode((WIDTH, HEIGHT))

                choose_player()
            #if info_button.handle_event(event):
            #    pygame.time.delay(100)
            #    print("Start button presseed!")
            if option_button.handle_event(event):
                pygame.time.delay(100)
                game_manager.save_settings()
                options()
            if quit_button.handle_event(event):
                pygame.time.delay(100)
                game_manager.save_settings()
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE: # resizes the screen only when the window acually resizes
                # Enforce minimum resolution
                new_width = max(event.w, Static_variables.MIN_WIDTH)
                new_height = max(event.h, Static_variables.MIN_HEIGHT)
                game_manager.settings["resolution"] = new_width,new_height

                # Apply the adjusted size to the window
                game_manager.screen = game_manager.apply_settings()
                WIDTH, HEIGHT = game_manager.update_dimensions()
                # Scale the background image to match the screen size
                background1 = pygame.transform.scale(background1, (WIDTH+80, HEIGHT+80))
                background2 = pygame.transform.scale(background2, (WIDTH+80, HEIGHT+80))
                background3 = pygame.transform.scale(background3, (WIDTH+80, HEIGHT+80))
                background4 = pygame.transform.scale(background4, (WIDTH+80, HEIGHT+80))

                #start_button.pos = (WIDTH//2-(32*Static_variables.PLAYER_SCALE), HEIGHT//2)
                start_button.pos = (WIDTH//2-(32*Static_variables.PLAYER_SCALE), HEIGHT//2+(40 *Static_variables.PLAYER_SCALE))
                option_button.pos = (WIDTH//2-(40*Static_variables.PLAYER_SCALE), HEIGHT//2+(80*Static_variables.PLAYER_SCALE))
                quit_button.pos = (WIDTH//2-(32*Static_variables.PLAYER_SCALE), HEIGHT//2+(120*Static_variables.PLAYER_SCALE))


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
        #info_button.draw()
        option_button.draw()
        quit_button.draw()

        if Static_variables.RECT_MODE:
            pygame.draw.rect(game_manager.screen, (255, 0, 0), start_button.rect, 2)
            #pygame.draw.rect(game_manager.screen, (255, 0, 0), info_button.rect, 2)
            pygame.draw.rect(game_manager.screen, (255, 0, 0), option_button.rect, 2)
            pygame.draw.rect(game_manager.screen, (255, 0, 0), quit_button.rect, 2)

        pygame.display.flip()
        Static_variables.CLOCK.tick(Static_variables.FPS)



if __name__ == "__main__": 
    game_manager.get_display_res()
    game_manager.apply_settings()
    main_menu()
            