import pygame
import random
import sys
import os

# --- Ініціалізація ---
pygame.init()
try: pygame.mixer.init()
except: pass

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# --- Налаштування візуалу ---
font_size = 22
fall_speed = 5       
mutation_lvl = 5    
tail_len_factor = 25 
color_idx = 0
colors = [(0, 255, 70), (255, 0, 0), (0, 191, 255), (255, 215, 0), (255, 255, 255)]
modes = ["MIX", "BINARY", "HEX", "KATAKANA"]
current_mode = 0

# --- Налаштування Музики ---
music_folder = "music"
playlist = []
current_track_idx = 0
is_paused = False

if not os.path.exists(music_folder):
    os.makedirs(music_folder)
playlist = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]

def play_music(idx):
    if playlist:
        try:
            pygame.mixer.music.load(os.path.join(music_folder, playlist[idx]))
            pygame.mixer.music.play(-1)
        except: pass

if playlist: play_music(current_track_idx)

def get_chars(mode):
    katakana = [chr(i) for i in range(12448, 12543)]
    latin = [chr(i) for i in range(65, 91)]
    digits = [chr(i) for i in range(48, 58)]
    if mode == "BINARY": return ['0', '1']
    if mode == "HEX": return latin[:6] + digits
    if mode == "KATAKANA": return katakana
    return katakana + latin + digits + list("?!/=+-$#*%^&|<>")

chars = get_chars(modes[current_mode])
font = pygame.font.SysFont('ms gothic', font_size, bold=True)
ui_font = pygame.font.SysFont('consolas', 14, bold=True)

class SymbolColumn:
    def __init__(self, x):
        self.x = x
        self.reset()

    def reset(self):
        self.y = random.randint(-HEIGHT, 0)
        self.speed = random.uniform(2, 6) + (fall_speed / 2)
        self.length = random.randint(max(5, tail_len_factor // 2), tail_len_factor)
        self.symbols = [random.choice(chars) for _ in range(self.length)]

    def draw(self):
        for i in range(len(self.symbols)):
            alpha = max(0, 255 - (i * (255 // self.length))) if self.length > 0 else 255
            render_color = (220, 255, 220) if i == 0 else colors[color_idx]
            s = font.render(self.symbols[i], True, render_color)
            s.set_alpha(alpha)
            pos_y = self.y - (i * font_size)
            if -font_size < pos_y < HEIGHT:
                screen.blit(s, (self.x, pos_y))
            if random.random() < 0.01 * mutation_lvl:
                self.symbols[i] = random.choice(chars)

    def update(self):
        self.y += self.speed * (fall_speed / 5)
        if self.y - (self.length * font_size) > HEIGHT:
            self.reset()

columns_list = [SymbolColumn(i * font_size) for i in range(WIDTH // font_size)]

show_ui = False
running = True
while running:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and show_ui:
            # SIZE кнопка
            if WIDTH-125 < mx < WIDTH-95 and 50 < my < 70:
                font_size = max(10, font_size - 2)
                font = pygame.font.SysFont('ms gothic', font_size, bold=True)
                columns_list = [SymbolColumn(i * font_size) for i in range(WIDTH // font_size)]
            if WIDTH-85 < mx < WIDTH-55 and 50 < my < 70:
                font_size = min(60, font_size + 2)
                font = pygame.font.SysFont('ms gothic', font_size, bold=True)
                columns_list = [SymbolColumn(i * font_size) for i in range(WIDTH // font_size)]
            
            # SPEED кнопка
            if WIDTH-125 < mx < WIDTH-95 and 75 < my < 95: fall_speed = max(1, fall_speed - 1)
            if WIDTH-85 < mx < WIDTH-55 and 75 < my < 95: fall_speed = min(20, fall_speed + 1)

            # LEN кнопка
            if WIDTH-125 < mx < WIDTH-95 and 100 < my < 120:
                tail_len_factor = max(5, tail_len_factor - 5)
                for c in columns_list: c.reset()
            if WIDTH-85 < mx < WIDTH-55 and 100 < my < 120:
                tail_len_factor = min(150, tail_len_factor + 5)
                for c in columns_list: c.reset()

            # MODE кнопка
            if WIDTH-230 < mx < WIDTH-20 and 125 < my < 145:
                current_mode = (current_mode + 1) % len(modes)
                chars = get_chars(modes[current_mode])
                for c in columns_list: c.symbols = [random.choice(chars) for _ in range(c.length)]

            # ПЛЕЄР
            if WIDTH-230 < mx < WIDTH-120 and 175 < my < 195: # Pause
                is_paused = not is_paused
                if is_paused: pygame.mixer.music.pause()
                else: pygame.mixer.music.unpause()
            if WIDTH-115 < mx < WIDTH-20 and 175 < my < 195: # Next
                if playlist:
                    current_track_idx = (current_track_idx + 1) % len(playlist)
                    play_music(current_track_idx)
                    is_paused = False

            # COLOR / EXIT
            if WIDTH-230 < mx < WIDTH-20 and 200 < my < 220:
                color_idx = (color_idx + 1) % len(colors)
            if WIDTH-230 < mx < WIDTH-20 and 230 < my < 255:
                running = False

    screen.fill((0, 0, 0))
    for col in columns_list:
        col.draw()
        col.update()

    if mx > WIDTH - 250 and my < 280:
        show_ui = True
        pygame.mouse.set_visible(True)
        # Малюємо панель
        pygame.draw.rect(screen, (15, 15, 15), (WIDTH-240, 10, 230, 260))
        pygame.draw.rect(screen, colors[color_idx], (WIDTH-240, 10, 230, 260), 1)
        
        def d_btn(text, y, val):
            screen.blit(ui_font.render(f"{text}: {val}", True, (200,200,200)), (WIDTH-230, y))
            pygame.draw.rect(screen, (60,60,60), (WIDTH-125, y-3, 30, 18)) # [-]
            pygame.draw.rect(screen, (60,60,60), (WIDTH-85, y-3, 30, 18))  # [+]
            screen.blit(ui_font.render("-", True, (255,255,255)), (WIDTH-115, y-2))
            screen.blit(ui_font.render("+", True, (255,255,255)), (WIDTH-75, y-2))

        d_btn("SIZE", 55, font_size)
        d_btn("SPEED", 80, fall_speed)
        d_btn("LEN", 105, tail_len_factor)
        
        # Кнопка MODE
        pygame.draw.rect(screen, (40,40,40), (WIDTH-230, 125, 210, 20))
        screen.blit(ui_font.render(f"MODE: {modes[current_mode]}", True, (255,255,255)), (WIDTH-220, 128))

        # Музика
        track_n = playlist[current_track_idx][:18] if playlist else "No music"
        screen.blit(ui_font.render(f"SONG: {track_n}", True, (0, 255, 255)), (WIDTH-230, 155))
        pygame.draw.rect(screen, (40, 70, 40), (WIDTH-230, 175, 105, 20))
        screen.blit(ui_font.render("P/PAUSE", True, (255,255,255)), (WIDTH-215, 178))
        pygame.draw.rect(screen, (40, 40, 70), (WIDTH-115, 175, 95, 20))
        screen.blit(ui_font.render("NEXT >>", True, (255,255,255)), (WIDTH-100, 178))

        # Колір та Вихід
        pygame.draw.rect(screen, (40, 40, 40), (WIDTH-230, 200, 210, 20))
        screen.blit(ui_font.render("CHANGE COLOR", True, colors[color_idx]), (WIDTH-220, 203))

        pygame.draw.rect(screen, (150, 0, 0), (WIDTH-230, 230, 210, 25))
        screen.blit(ui_font.render("EXIT PROGRAM", True, (255,255,255)), (WIDTH-185, 235))
    else:
        show_ui = False
        pygame.mouse.set_visible(False)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
