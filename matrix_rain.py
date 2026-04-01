#! py -3.12
import pygame
import random

# Ініціалізація
pygame.init()

# Налаштування екрану (можна вказати конкретне розширення або full screen)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Matrix Rain")

# Кольори та символи
FONT_SIZE = 20
font = pygame.font.SysFont('ms gothic', FONT_SIZE, bold=True)
chars = [chr(int('0x30a0', 16) + i) for i in range(96)] # Японські ієрогліфи (катакана) + цифри
chars += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Створення колонок
columns = WIDTH // FONT_SIZE
drops = [1 for _ in range(columns)]

clock = pygame.time.Clock()

running = True
while running:
    # Перевірка виходу (клавіша Esc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Ефект затухання (напівпрозорий чорний прямокутник поверх усього)
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(25) # Чим менше число, тим довший "хвіст" у символів
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Малюємо символи
    for i in range(len(drops)):
        # Вибираємо випадковий символ
        char = random.choice(chars)
        char_render = font.render(char, True, (0, 255, 70)) # Яскраво-зелений колір
        
        # Позиція символа
        x = i * FONT_SIZE
        y = drops[i] * FONT_SIZE
        
        screen.blit(char_render, (x, y))

        # Якщо символ вийшов за екран, повертаємо його вгору з випадковою затримкою
        if y > HEIGHT and random.random() > 0.975:
            drops[i] = 0
        
        drops[i] += 1

    pygame.display.flip()
    clock.tick(30) # Швидкість оновлення (FPS)

pygame.quit()
