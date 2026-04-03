import pygame
import random
import sys
import os

# Ініціалізація
pygame.init()
pygame.mixer.init() # Для музики

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Matrix v1.4")
clock = pygame.time.Clock()

# --- Параметри Matrix v1.4 ---
font_size = 22
base_speed = 30 # Базова швидкість
color_idx = 0
colors = [(0, 255, 70), (255, 0, 0), (0, 191, 255), (255, 215, 0), (255, 255, 255)]
highlights = [(180, 255, 200), (255, 150, 150), (200, 230, 255), (255, 255, 200), (255, 255, 255)] # Світліші відтінки

modes = ["MIX", "BINARY", "HEX", "KATAKANA"]
current_mode = 0

def get_chars(mode):
    if mode == "BINARY": return ['0', '1']
    if mode == "HEX": return list("0123456789ABCDEF")
    if mode == "KATAKANA": return [chr(int('0x30a0', 16) + i) for i in range(96)]
    return [chr(int('0x30a0', 16) + i) for i in range(96)] + ['0', '1'] + [str(i) for i in range(2, 10)]

chars = get_chars(modes[current_mode])
font = pygame.font.SysFont('ms gothic', font_size, bold=True)
ui_font = pygame.font.SysFont('consolas', 16, bold=True)

# Кількість колонок
columns = WIDTH // font_size

# v1.4: Дані про кожну колонку: [позиція_y, індивідуальна_швидкість]
drops_data = [[random.randint(-HEIGHT, 0), random.uniform(0.5, 1.5)] for _ in range(columns)]

# Завантаження музики ( Silicon Dreams.mp3 )
music_file = "Silicon Dreams.mp3"
music_started = False
if os.path.exists(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1) # Безкінечний повтор
    music_started = True

show_ui = False
running = True

while running:
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            
        # ОБРОБКА КЛІКІВ ТА КЛАВІШ
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c: color_idx = (color_idx + 1) % len(colors)
            if event.key == pygame.K_UP: base_speed = min(120, base_speed + 5)
            if event.key == pygame.K_DOWN: base_speed = max(5, base_speed - 5)

        if event.type == pygame.MOUSEBUTTONDOWN and show_ui:
            # Кнопки Розміру
            if WIDTH-80 < mx < WIDTH-45 and 55 < my < 80: # +
                font_size = min(60, font_size + 2)
                columns = WIDTH // font_size
                drops_data = [[random.randint(-HEIGHT, 0), random.uniform(0.5, 1.5)] for _ in range(columns)]
                font = pygame.font.SysFont('ms gothic', font_size, bold=True)
            if WIDTH-120 < mx < WIDTH-85 and 55 < my < 80: # -
                font_size = max(10, font_size - 2)
                columns = WIDTH // font_size
                drops_data = [[random.randint(-HEIGHT, 0), random.uniform(0.5, 1.5)] for _ in range(columns)]
                font = pygame.font.SysFont('ms gothic', font_size, bold=True)
            
            # Кнопки Швидкості
            if WIDTH-80 < mx < WIDTH-45 and 85 < my < 110: # +
                base_speed = min(120, base_speed + 5)
            if WIDTH-120 < mx < WIDTH-85 and 85 < my < 110: # -
                base_speed = max(5, base_speed - 5)

            # Кнопка Кольору
            if WIDTH-230 < mx < WIDTH-20 and 115 < my < 140: color_idx = (color_idx + 1) % len(colors)
                
            # Кнопка Режиму
            if WIDTH-230 < mx < WIDTH-20 and 145 < my < 170:
                current_mode = (current_mode + 1) % len(modes)
                chars = get_chars(modes[current_mode])

    # Показ панелі
    if mx > WIDTH - 250 and my < 220:
        show_ui = True
        pygame.mouse.set_visible(True)
    else:
        show_ui = False
        pygame.mouse.set_visible(False)

    # Малювання
    # Зробимо фон трохи темнішим (set_alpha менше), щоб шлейф був довше
    s = pygame.Surface((WIDTH, HEIGHT))
    s.set_alpha(30)
    s.fill((0, 0, 0))
    screen.blit(s, (0, 0))

    current_color = colors[color_idx]
    current_highlight = highlights[color_idx]

    for i in range(columns):
        # Отримуємо дані про колонку
        pos_y, col_speed = drops_data[i]
        
        # v1.4: Символ міняється в польоті (Glitch effect)
        # 10% шанс, що символ зміниться
        if random.random() < 0.1:
            char = random.choice(chars)
        else:
            # Якщо не міняється, вибираємо випадковий, але фіксований для цього кадру
            char = random.choice(chars)

        # v1.4: 1% шанс яскравого спалаху
        if random.random() < 0.01:
            color = current_highlight
        else:
            color = current_color

        # Малюємо символ
        msg = font.render(char, True, color)
        # Використовуємо індивідуальну швидкість колонки
        screen.blit(msg, (i * font_size, pos_y * font_size))

        # Оновлення позиції (з індивідуальною швидкістю)
        pos_y += col_speed
        
        # Скидання колони
        if pos_y * font_size > HEIGHT and random.random() > 0.975:
            pos_y = 0
            # Перераховуємо швидкість при скиданні
            col_speed = random.uniform(0.5, 1.5)
            
        drops_data[i] = [pos_y, col_speed]

    # ПАНЕЛЬ v1.4
    if show_ui:
        panel_rect = pygame.Rect(WIDTH - 240, 10, 230, 210)
        pygame.draw.rect(screen, (20, 20, 20), panel_rect)
        pygame.draw.rect(screen, current_color, panel_rect, 2)
        
        screen.blit(ui_font.render(f"MATRIX v1.4", True, (255,255,255)), (WIDTH-230, 20))
        
        screen.blit(ui_font.render(f"Size: {font_size}", True, (255,255,255)), (WIDTH-230, 58))
        pygame.draw.rect(screen, (60, 60, 60), (WIDTH-120, 55, 35, 25))
        pygame.draw.rect(screen, (60, 60, 60), (WIDTH-80, 55, 35, 25))
        screen.blit(ui_font.render("-", True, (255,255,255)), (WIDTH-108, 58))
        screen.blit(ui_font.render("+", True, (255,255,255)), (WIDTH-68, 58))

        screen.blit(ui_font.render(f"Speed: {base_speed}", True, (255,255,255)), (WIDTH-230, 88))
        pygame.draw.rect(screen, (60, 60, 60), (WIDTH-120, 85, 35, 25))
        pygame.draw.rect(screen, (60, 60, 60), (WIDTH-80, 85, 35, 25))
        screen.blit(ui_font.render("-", True, (255,255,255)), (WIDTH-108, 88))
        screen.blit(ui_font.render("+", True, (255,255,255)), (WIDTH-68, 88))

        pygame.draw.rect(screen, (60, 60, 60), (WIDTH-230, 115, 210, 25))
        screen.blit(ui_font.render(f"CHANGE COLOR (C)", True, (255,255,255)), (WIDTH-220, 118))

        pygame.draw.rect(screen, (60, 60, 60), (WIDTH-230, 145, 210, 25))
        screen.blit(ui_font.render(f"MODE: {modes[current_mode]}", True, (255,255,255)), (WIDTH-220, 148))
        
        # Індикатор музики
        music_status = "Mus: ON" if music_started else "Mus: OFF"
        color_status = (0,255,0) if music_started else (150,150,150)
        screen.blit(ui_font.render(music_status, True, color_status), (WIDTH-230, 175))

        screen.blit(ui_font.render("ESC to EXIT", True, (150,150,150)), (WIDTH-230, 195))

    pygame.display.flip()
    # v1.4: Тепер base_speed контролирує FPS, а індивідуальні швидкості колонок - темп падіння
    clock.tick(base_speed)

pygame.quit()
sys.exit()
