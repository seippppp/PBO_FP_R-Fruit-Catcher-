import pygame
import random
import os
from core.settings import *
from core.player import Basket
from core.fruit import Fruit
from core.obstacle import Obstacle
from .base import BaseScreen

# Class Dummy
class DummySound:
    def play(self): pass
    def set_volume(self, v): pass
    def stop(self): pass

class GameScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.bgs = {}
        self.fruit_images = {} # Dictionary untuk menyimpan gambar buah yang di-load
        
        self.load_assets()
        self.current_level = 1

    def smart_scale_bg(self, original_img):
        img_rect = original_img.get_rect()
        screen_ratio = WIDTH / HEIGHT
        img_ratio = img_rect.width / img_rect.height
        if img_ratio < screen_ratio:
            scale_factor = WIDTH / img_rect.width
            new_width = WIDTH
            new_height = int(img_rect.height * scale_factor)
        else:
            scale_factor = HEIGHT / img_rect.height
            new_height = HEIGHT
            new_width = int(img_rect.width * scale_factor)
        scaled_img = pygame.transform.scale(original_img, (new_width, new_height))
        final_surface = pygame.Surface((WIDTH, HEIGHT))
        x_pos = (WIDTH - new_width) // 2
        y_pos = (HEIGHT - new_height) // 2
        final_surface.blit(scaled_img, (x_pos, y_pos))
        return final_surface

    def load_assets(self):
        print("--- LOADING ASSETS (INDIVIDUAL FRUITS) ---")
        
        # 1. Backgrounds
        bg_folder = r"C:\Users\asuss\Documents\PBO FP\assets\images\backgrounds"
        for i in range(1, 6):
            try:
                path = os.path.join(bg_folder, f"level{i}_bg.jpg")
                img = pygame.image.load(path).convert()
                self.bgs[i] = self.smart_scale_bg(img)
            except:
                self.bgs[i] = pygame.Surface((WIDTH, HEIGHT)); self.bgs[i].fill(BLUE)
        
        # 2. FRUITS (LOAD SATU PER SATU DARI SETTINGS)
        fruit_folder = r"C:\Users\asuss\Documents\PBO FP\assets\images\fruits"
        
        for data in FRUIT_DATA:
            filename = data['file']
            path = os.path.join(fruit_folder, filename)
            try:
                # Load gambar
                img = pygame.image.load(path).convert_alpha()
                # Simpan ke dictionary: {'ceri.png': Surface, ...}
                self.fruit_images[filename] = img
                print(f"✅ Loaded: {filename}")
            except Exception as e:
                print(f"❌ Gagal load {filename}: {e}")
                # Fallback kotak warna random
                surf = pygame.Surface((60, 60))
                surf.fill((random.randint(50,255), random.randint(50,255), 0))
                self.fruit_images[filename] = surf

        # 3. Sounds
        try:
            self.snd_catch = pygame.mixer.Sound(os.path.join(SND_DIR, 'catch.wav'))
            self.snd_catch.set_volume(0.5)
            self.snd_bomb = pygame.mixer.Sound(os.path.join(SND_DIR, 'bomb_explode.wav'))
            self.snd_bomb.set_volume(0.6)
            self.snd_gameover = pygame.mixer.Sound(os.path.join(SND_DIR, 'game_over.wav'))
        except:
            self.snd_catch = DummySound()
            self.snd_bomb = DummySound()
            self.snd_gameover = DummySound()

    def on_enter(self, level=1):
        pygame.mixer.stop()
        self.current_level = level
        self.start_new_level()

    def start_new_level(self):
        self.all_sprites = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        
        self.player = Basket()
        self.all_sprites.add(self.player)
        
        self.score = 0
        self.start_ticks = pygame.time.get_ticks()
        self.state = "PLAYING" 

    def handle_event_list(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.state in ["GAMEOVER", "WIN"]:
                    if event.key == pygame.K_r:
                        self.on_enter(self.current_level)
                    elif event.key == pygame.K_m:
                        self.manager.set_screen('menu')

    def update(self):
        if self.state != "PLAYING": return

        if pygame.mixer.get_busy(): pass 

        self.all_sprites.update()
        
        # --- SPAWN LOGIC (WEIGHTED RANDOM) ---
        if random.random() < 0.02 + (self.current_level * 0.005):
            # 1. Pisahkan Data dan Bobot
            choices = FRUIT_DATA
            weights = [item['weight'] for item in FRUIT_DATA]
            
            # 2. Pilih buah berdasarkan kelangkaan
            # random.choices return list, ambil elemen [0]
            selected = random.choices(choices, weights=weights, k=1)[0]
            
            # 3. Ambil aset yang sesuai
            image = self.fruit_images[selected['file']]
            score_val = selected['score']
            
            # 4. Buat objek Buah
            f = Fruit(image, score_val)
            self.all_sprites.add(f)
            self.fruits.add(f)
            
        # Spawn Obstacle
        lvl_data = LEVEL_DATA[self.current_level]
        if lvl_data['obstacles'] and random.random() < 0.015:
            obs_name = random.choice(lvl_data['obstacles'])
            o = Obstacle(obs_name, lvl_data['penalty'])
            self.all_sprites.add(o); self.obstacles.add(o)

        # --- COLLISION LOGIC ---
        
        # 1. Cek Buah
        hits = pygame.sprite.spritecollide(self.player, self.fruits, True)
        for hit in hits:
            # Tambah skor sesuai jenis buah yang ditangkap
            pts = hit.score_value
            print(f"[DEBUG] Menangkap Buah! Poin: +{pts}")
            
            self.snd_catch.stop()
            self.snd_catch.play()
            self.score += pts

        # 2. Cek Obstacle
        obs_hits = pygame.sprite.spritecollide(self.player, self.obstacles, True)
        for obs in obs_hits:
            print(f"[DEBUG] Menabrak {obs.type}.")
            self.snd_bomb.stop()
            self.snd_bomb.play()
            
            if 'bomb' in obs.type:
                print("[DEBUG] IT WAS A BOMB -> GAME OVER")
                self.state = "GAMEOVER"
            else:
                self.score -= obs.penalty

        # Win Condition
        if self.score >= lvl_data['target']:
            self.state = "WIN"
            from core.settings import LEVEL_STATUS
            LEVEL_STATUS[self.current_level] = True
        
        # Time Check
        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.time_left = int(DURATION - elapsed)
        
        if self.time_left <= 0:
            self.snd_gameover.play()
            self.state = "GAMEOVER"

    def draw(self):
        self.screen.blit(self.bgs[self.current_level], (0, 0))
        self.all_sprites.draw(self.screen)
        
        # HUD
        self.draw_text(f"Score: {self.score}", 30, WHITE, WIDTH/2, 10)
        self.draw_text(f"Target: {LEVEL_DATA[self.current_level]['target']}", 25, YELLOW, WIDTH-80, 10)
        self.draw_text(f"Time: {self.time_left}", 25, WHITE, 60, 10)
        self.draw_text(f"Level: {self.current_level}", 25, WHITE, 60, 40)
        
        if self.state == "GAMEOVER":
            self.draw_overlay("GAME OVER", RED, "Press 'R' Retry or 'M' Menu")
        elif self.state == "WIN":
            self.draw_overlay("LEVEL COMPLETE!", GREEN, "Press 'M' for Menu")

    def draw_text(self, text, size, color, x, y):
        font = self.font if size < 40 else self.big_font
        surf = font.render(str(text), True, color)
        rect = surf.get_rect(midtop=(x, y))
        self.screen.blit(surf, rect)

    def draw_overlay(self, title, color, sub):
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(150)
        s.fill(BLACK)
        self.screen.blit(s, (0,0))
        self.draw_text(title, 72, color, WIDTH//2, HEIGHT//2 - 50)
        self.draw_text(sub, 36, WHITE, WIDTH//2, HEIGHT//2 + 20)