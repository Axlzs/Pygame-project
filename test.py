import pygame
from static_variables import *
from static_classes import *
from game_manager import game_manager

pygame.init()
class LesserButton:
    def __init__(self, screen, sprite_sheet, button_type, pos):
        self.screen = screen
        self.scale = PLAYER_SCALE
        self.type = button_type
        self.sprite_sheet = sprite_sheet
        self.data = LESSER_BUTTON_DATA[self.type]
        self.pos = pos
        self.rect = pygame.Rect(
            self.pos,
            (self.data["width"] * PLAYER_SCALE, self.data["height"] * PLAYER_SCALE)
        )

        self.images = []
        for i in range(2):  # Buttons have 2 states: normal, hover
            rect = pygame.Rect(
                self.data["x"] + (i * self.data["width"]),
                self.data["y"],
                self.data["width"],
                self.data["height"],
            )
            image = self.sprite_sheet.subsurface(rect)

            if self.scale != 1.0:
                scaled_width = int(self.data["width"] * self.scale+3)
                scaled_height = int(self.data["height"] * self.scale+3)
                image = pygame.transform.scale(image, (scaled_width, scaled_height))
            self.images.append(image)

        self.current_image = self.images[0]

    def draw(self):
        """Draw the button on the screen."""
        self.screen.blit(self.current_image, self.pos)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.current_image = self.images[1]  # Hover state
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True  # Button clicked
        else:
            self.current_image = self.images[0]  # Normal state
        return False
    
screen = pygame.display.set_mode((1000, 700))

BUTTON_SPRITE_SHEET = pygame.image.load("images/UI_elements/Debuff buttons.png").convert_alpha()
health_uppgrade = LesserButton(screen, BUTTON_SPRITE_SHEET, "health", (100, HEIGHT//2))
strength_uppgrade = LesserButton(screen, BUTTON_SPRITE_SHEET, "strengthen", (200, HEIGHT//2))
attack_speed_uppgrade = LesserButton(screen, BUTTON_SPRITE_SHEET, "swing", (300, HEIGHT//2))
speed_uppgrade = LesserButton(screen, BUTTON_SPRITE_SHEET, "levelup", (400, HEIGHT//2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_manager.save_settings()
            exit()

    health_uppgrade.draw()
    strength_uppgrade.draw()
    attack_speed_uppgrade.draw()
    speed_uppgrade.draw()
    pygame.display.flip()