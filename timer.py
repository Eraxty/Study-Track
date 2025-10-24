import pygame
import sys
import time

pygame.init()
pygame.display.set_caption("Simple Timer")

# Colors
BG = (25, 25, 25)
TEXT = (255, 255, 255)
BUTTON = (50, 50, 50)
BUTTON_HOVER = (80, 80, 80)

# Fonts
font_large = pygame.font.Font(None, 100)
font_small = pygame.font.Font(None, 40)

# Screen
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Buttons
pause_btn = pygame.Rect(WIDTH/2 - 60, HEIGHT - 80, 120, 50)

# Timer logic
start_time = time.time()
paused = False
paused_time = 0
pause_start = 0

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pause_btn.collidepoint(event.pos):
                if paused:
                    # unpause
                    paused = False
                    paused_time += time.time() - pause_start
                else:
                    # pause
                    paused = True
                    pause_start = time.time()

    screen.fill(BG)

    # Timer display
    if paused:
        elapsed = pause_start - start_time - paused_time
    else:
        elapsed = time.time() - start_time - paused_time

    mins = int(elapsed // 60)
    secs = int(elapsed % 60)
    timer_text = f"{mins:02d}:{secs:02d}"

    text_surface = font_large.render(timer_text, True, TEXT)
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text_surface, text_rect)

    # Button
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER if pause_btn.collidepoint(mouse_pos) else BUTTON
    pygame.draw.rect(screen, color, pause_btn, border_radius=10)

    btn_text = "Resume" if paused else "Pause"
    text_btn = font_small.render(btn_text, True, TEXT)
    text_btn_rect = text_btn.get_rect(center=pause_btn.center)
    screen.blit(text_btn, text_btn_rect)

    pygame.display.flip()
    clock.tick(30)
