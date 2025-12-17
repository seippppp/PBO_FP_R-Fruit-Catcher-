import pygame
import sys
from core.settings import *
from screen_manager import ScreenManager
from screens.main_menu import MainMenuScreen
from screens.game_screen import GameScreen
# HAPUS: from screens.high_score_screen import HighScoreScreen

class MainApp:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.manager = ScreenManager(self.screen)
        
        # Register Screens (Cuma 2 sekarang)
        self.manager.add_screen('menu', MainMenuScreen(self.screen, self.manager))
        self.manager.add_screen('game', GameScreen(self.screen, self.manager))
        # HAPUS baris add_screen highscore
        
        self.manager.set_screen('menu')

    def run(self):
        while True:
            self.clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.manager.handle_event_list(events)
            self.manager.update()
            self.manager.draw()
            pygame.display.flip()

if __name__ == '__main__':
    app = MainApp()
    app.run()