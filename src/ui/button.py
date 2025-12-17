import pygame
from core.settings import *

class Button:
    def __init__(self, text, x, y, width, height, func):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.func = func
        self.font = pygame.font.Font(None, 36)
        
        self.base_color = GREEN
        self.hover_color = YELLOW
        self.current_color = self.base_color
        self.text_color = WHITE

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        self.current_color = self.hover_color if is_hovered else self.base_color
        
        if is_hovered:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.func()

    def draw(self, screen):
        # Draw Rect
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=12)
        
        # Draw Text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)