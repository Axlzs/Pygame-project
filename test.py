class GameManager:
    def __init__(self):
        self.display = self.get_display_res()
        print("display",self.display)

    def get_display_res():
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        display_info = pygame.display.Info()
        display_width = display_info.current_w
        display_height = display_info.current_h
        return display_width,display_height