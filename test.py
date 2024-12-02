                game_manager.screen = pygame.display.set_mode(
                game_manager.settings["resolution"],
                pygame.FULLSCREEN if game_manager.settings["screen_mode"] == "fullscreen" else 0)  # No RESIZABLE flag