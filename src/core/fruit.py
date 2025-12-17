import pygame
import random
from .settings import *

class Fruit(pygame.sprite.Sprite):
    def __init__(self, image, score_value):
        super().__init__()
        self.speed = random.randint(4, 7)
        
        # Gambar diterima sudah jadi dari GameScreen
        # Kita pastikan ukurannya seragam (60x60)
        self.image = pygame.transform.scale(image, (60, 60))
        
        # Simpan nilai skor spesifik buah ini
        self.score_value = score_value
        
        self.rect = self.image.get_rect()
        # Posisi Random
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

    def update(self):
        self.rect.y += self.speed
        # Hapus jika lewat batas bawah
        if self.rect.top > HEIGHT:
            self.kill()