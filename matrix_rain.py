import pygame
import random
import sys

# Ініціалізація
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Matrix 1.2")
clock = pygame.time.Clock()

# --- Параметри Matrix 1.2 ---
font_size = 22
speed = 30
# Кольори: Зелений, Червоний, Синій, Золотий, Білий
colors = [(0, 255, 70), (255, 0, 0), (0, 191, 255), (255, 215, 0), (255, 255, 255)]
c_idx = 0

# Набір символів (Катакана + 0/1 + Цифри)
chars = [chr(int('0x30a0', 16) + i) for i in range(96)] + ['0', '1'] + [str(i) for i in range(2, 10)]
font = pygame.font.SysFont('ms gothic', font_size, bold=True)
ui_font = pygame.font.SysFont('consolas', 20, bold=True)

columns = WIDTH // font_size
drops = [random.randint(-HEIGHT, 0) for _ in range(columns)]

running = True
show_ui = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c: # Зміна кольору
                c_idx = (c_idx + 1) % len(colors)
            if event.key == pygame.K_UP: speed = min(120, speed + 5)
            if event.key == pygame.K_DOWN: speed = max(5, speed - 5)

    # Логіка панелі (правий верхній кут)
    mx, my = pygame.mouse.get_pos()
    if mx > WIDTH - 250 and my < 200:
        show_ui = True
        pygame.mouse.set_visible(True)
    else:
        show_ui = False
        pygame.mouse.set_visible(False)

    # Фон (ефект хвоста)
    s = pygame.Surface((WIDTH, HEIGHT))
    s.set_alpha(35)
    s.fill((0, 0, 0))
    screen.blit(s, (0, 0))

    # Малювання символів
    for i in range(len(drops)):
        char = random.choice(chars)
        msg = font.render(char, True, colors[c_idx])
        screen.blit(msg, (i * font_size, drops[i] * font_size))
        
        if drops[i] * font_size > HEIGHT and random.random() > 0.975:
            drops[i] = 0
        drops[i] += 1

    # Панель налаштувань
    if show_ui:
        panel = pygame.Surface((230, 150))
        panel.set_alpha(190)
        panel.fill((20, 20, 20))
        screen.blit(panel, (WIDTH - 240, 10))
        pygame.draw.rect(screen, colors[c_idx], (WIDTH - 240, 10, 230, 150), 2)
        
        info_lines = [f"SPEED: {speed}", f"COLOR: {c_idx+1}", "[UP/DOWN]: Speed", "[C]: Change Color"]
        for i, line in enumerate(info_lines):
            t = ui_font.render(line, True, (255, 255, 255))
            screen.blit(t, (WIDTH - 230, 25 + i * 30))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
