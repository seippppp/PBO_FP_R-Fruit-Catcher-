import pygame
import random
import os
from .settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, filename, penalty):
        super().__init__()
        self.speed = random.randint(5, 9)
        path = os.path.join(IMG_DIR, 'obstacles', filename)
        
        try:
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (70, 70))
        except:
            self.image = pygame.Surface((70, 70))
            self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        
        self.type = filename
        self.penalty = penalty

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()