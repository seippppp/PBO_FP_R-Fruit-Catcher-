import pygame
import os
from .settings import *

class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        path = os.path.join(IMG_DIR, 'ui', 'basket.png')
        try:
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, 80))
        except:
            print("Warning: basket.png not found, using placeholder.")
            self.image = pygame.Surface((100, 80))
            self.image.fill(RED)
            
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        # Batas Layar
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH