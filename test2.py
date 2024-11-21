import pygame
from test import game_manager

def options_menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    # Toggle fullscreen
                    if game_manager.settings["screen_mode"] == "fullscreen":
                        game_manager.settings["screen_mode"] = "windowed"
                        game_manager.apply_settings()
                    else:
                        game_manager.settings["screen_mode"] = "fullscreen"
                        game_manager.apply_settings()
                    game_manager.update_dimensions()  # Update WIDTH and HEIGHT

        # Example: Draw options screen
        game_manager.screen.fill((50, 50, 50))
        pygame.display.flip()

options_menu()