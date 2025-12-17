import os

# --- LAYAR & WAKTU ---
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Fruit Catcher - Final Project"

# --- WARNA ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
BLUE = (0, 100, 255)
GRAY = (100, 100, 100)

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMG_DIR = os.path.join(ASSETS_DIR, 'images')
SND_DIR = os.path.join(ASSETS_DIR, 'sounds', 'effects')

# --- GAMEPLAY ---
PLAYER_SPEED = 8
DURATION = 60 

# --- DATA LEVEL ---
LEVEL_DATA = {
    1: {'target': 300,  'obstacles': [], 'penalty': 0},
    2: {'target': 500,  'obstacles': ['rock.png'], 'penalty': 20},
    3: {'target': 700,  'obstacles': ['rock.png', 'trash.png'], 'penalty': 30},
    4: {'target': 900,  'obstacles': ['rock.png', 'trash.png', 'dog.png'], 'penalty': 40},
    5: {'target': 1200, 'obstacles': ['rock.png', 'trash.png', 'dog.png', 'bomb.png'], 'penalty': 50}
}

# --- STATUS LEVEL ---
LEVEL_STATUS = {
    1: False,
    2: False,
    3: False,
    4: False,
    5: False
}

# --- KONFIGURASI BUAH (BARU) ---
# file: nama file di folder images/fruits
# score: poin yang didapat
# weight: peluang muncul (makin besar = makin sering)
FRUIT_DATA = [
    {'file': 'ceri.png',       'score': 10, 'weight': 100}, # Sering
    {'file': 'stroberi.png',   'score': 15, 'weight': 80},
    {'file': 'jeruk.png',      'score': 20, 'weight': 60},
    {'file': 'apel_merah.png', 'score': 25, 'weight': 50},
    {'file': 'apel_hijau.png', 'score': 30, 'weight': 40},
    {'file': 'pir.png',        'score': 50, 'weight': 20},
    {'file': 'anggur.png',     'score': 100, 'weight': 5},  # Sangat Langka (Jackpot)
]