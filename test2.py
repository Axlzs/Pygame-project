def upgrade_screen(player_type):
    BUTTON_SPRITE_SHEET = pygame.image.load("images/UI_elements/Debuff buttons.png").convert_alpha()
    health_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "health", (100, HEIGHT//2))
    strength_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "strengthen", (200, HEIGHT//2))
    attack_speed_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "swing", (300, HEIGHT//2))
    speed_uppgrade = LesserButton(game_manager.screen, BUTTON_SPRITE_SHEET, "levelup", (400, HEIGHT//2))

    font = pygame.font.Font("font/Minecraft.ttf", 15*PLAYER_SCALE)
    text = font.render("Choose upgrades", True, WHITE)
    game_manager.screen.blit(text, (WIDTH//2-100*PLAYER_SCALE, HEIGHT//2))

    running = True
    while running:

        health_uppgrade.draw()
        strength_uppgrade.draw()
        attack_speed_uppgrade.draw()
        speed_uppgrade.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_manager.save_settings()
                exit()
            if health_uppgrade.handle_event(event):
                pygame.time.delay(100)
                player.maxhealth += 20
                running = False
            if strength_uppgrade.handle_event(event):
                pygame.time.delay(100)
                PLAYER_DATA[player_type]['damage'] += 10
                running = False
            if attack_speed_uppgrade.handle_event(event):
                pygame.time.delay(100)
                if player.shoot_cooldown > 10 and player_type ==1:
                    player.shoot_cooldown - 50
                    running = False

                if player.melee_cooldown > 10 and player_type ==2:
                    player.melee_cooldown - 50
                    running = False
            if speed_uppgrade.handle_event(event):
                pygame.time.delay(100)
                SPEED_DIAGONAL *1.5
                SPEED_LINEAR * 1.5
                running = False