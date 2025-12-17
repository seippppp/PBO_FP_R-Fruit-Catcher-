import pygame
import sys
import os
from core.settings import *
from .base import BaseScreen
from ui.button import Button

class MainMenuScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        self.font_title = pygame.font.Font(None, 70)
        self.buttons = []
        
        # --- LOAD BACKGROUND MENU (PATH SPESIFIK) ---
        # Menggunakan r"" (raw string) agar backslash terbaca benar di Windows
        bg_path = r"C:\Users\asuss\Documents\PBO FP\assets\images\menu\menu.jpg"
        
        print(f"Attempting to load menu background from: {bg_path}")
        
        try:
            # Load gambar
            bg_img = pygame.image.load(bg_path).convert()
            # Skala gambar agar pas dengan ukuran layar game
            self.bg_image = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
            print("✅ Menu background loaded successfully.")
        except Exception as e:
            print(f"❌ Error loading menu background: {e}")
            print("Using fallback color (BLACK).")
            # Fallback: Buat latar belakang hitam jika gambar gagal dimuat
            self.bg_image = pygame.Surface((WIDTH, HEIGHT))
            self.bg_image.fill(BLACK)

        # Buat tombol pertama kali
        self.create_level_buttons()

    def create_level_buttons(self):
        """ Membuat 5 tombol level secara otomatis """
        self.buttons = [] # Reset list tombol
        
        btn_w, btn_h = 250, 50
        # Sesuaikan posisi Y awal agar tidak menutupi background terlalu banyak
        start_y = 180 
        gap = 70
        center_x = WIDTH // 2 - btn_w // 2

        for level in range(1, 6):
            # Cek status level dari settings.py
            is_done = LEVEL_STATUS[level]
            
            # Tentukan Teks dan Warna
            if is_done:
                text = f"LEVEL {level} (DONE)"
                color = GREEN
            else:
                text = f"LEVEL {level}"
                color = BLUE
            
            y_pos = start_y + (level-1) * gap
            
            # Lambda untuk menangkap nilai level
            btn = Button(text, center_x, y_pos, btn_w, btn_h, 
                         lambda l=level: self.manager.set_screen('game', level=l))
            
            btn.base_color = color
            self.buttons.append(btn)

        # Tombol Quit (posisi disesuaikan)
        quit_y = start_y + 5 * gap + 20
        self.btn_quit = Button("QUIT GAME", center_x, quit_y, btn_w, btn_h, 
                               lambda: self.quit_game())
        self.buttons.append(self.btn_quit)

    def on_enter(self, level=1):
        # Hentikan semua suara yang tersisa dari game sebelumnya
        pygame.mixer.stop() 
        
        # Refresh tombol (update status DONE)
        self.create_level_buttons()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_event_list(self, events):
        for btn in self.buttons:
            btn.update(events)

    def draw(self):
        # --- GAMBAR BACKGROUND ---
        # Gantikan fill(BLACK) dengan blit image
        self.screen.blit(self.bg_image, (0, 0))
        
        # Judul (Opsional: Bisa dihapus jika sudah ada di gambar background)
        # Saya beri bayangan sedikit agar lebih terbaca di atas gambar
        title_shadow = self.font_title.render("SELECT LEVEL", True, BLACK)
        title = self.font_title.render("SELECT LEVEL", True, YELLOW)
        
        rect_s = title_shadow.get_rect(center=(WIDTH//2 + 2, 80 + 2))
        rect = title.get_rect(center=(WIDTH//2, 80))
        
        self.screen.blit(title_shadow, rect_s)
        self.screen.blit(title, rect)
        
        # Draw semua tombol
        for btn in self.buttons:
            btn.draw(self.screen)