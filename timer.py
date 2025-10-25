import pygame
import sys
import time

pygame.init()
pygame.display.set_caption("Timer")

# Colors
BG = (25, 25, 30)
TEXT = (240, 240, 240)
BUTTON = (60, 60, 70)
BUTTON_HOVER = (100, 100, 120)
ACCENT = (130, 180, 255)

# Fonts
font_large = pygame.font.Font(None, 80)
font_small = pygame.font.Font(None, 32)

# Screen
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Timer variables
start_time = time.time()
paused = False
pause_start = 0
total_paused = 0
laps = []

# Buttons
pause_btn = pygame.Rect(WIDTH / 2 - 130, HEIGHT - 100, 120, 45)
lap_btn = pygame.Rect(WIDTH / 2 + 10, HEIGHT - 100, 120, 45)

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def draw_button(rect, text):
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON
    pygame.draw.rect(screen, color, rect, border_radius=10)
    label = font_small.render(text, True, ACCENT)
    screen.blit(label, label.get_rect(center=rect.center))

def get_elapsed():
    if paused:
        return pause_start - start_time - total_paused
    return time.time() - start_time - total_paused

def toggle_pause():
    global paused, pause_start, total_paused
    if paused:
        total_paused += time.time() - pause_start
        paused = False
    else:
        pause_start = time.time()
        paused = True

def add_lap(elapsed):
    laps.insert(0, format_time(elapsed))  # newest first

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pause_btn.collidepoint(event.pos):
                toggle_pause()
            elif lap_btn.collidepoint(event.pos) and not paused:
                add_lap(get_elapsed())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_pause()
            elif event.key == pygame.K_l and not paused:
                add_lap(get_elapsed())
            elif event.key == pygame.K_r:
                start_time = time.time()
                total_paused = 0
                paused = False
                laps.clear()

    # Background
    screen.fill(BG)

    # Timer
    elapsed = get_elapsed()
    timer_text = font_large.render(format_time(elapsed), True, TEXT)
    screen.blit(timer_text, timer_text.get_rect(center=(WIDTH / 2, 100)))

    # Laps area
    lap_y = 180
    for i, lap in enumerate(laps):
        label = font_small.render(f"Lap {len(laps)-i}: {lap}", True, TEXT)
        screen.blit(label, (WIDTH / 2 - 80, lap_y))
        lap_y += 35
        if lap_y > HEIGHT - 160:  # keeps newest visible, like scrolling
            break

    # Divider line
    pygame.draw.line(screen, (80, 80, 90), (50, HEIGHT - 130), (WIDTH - 50, HEIGHT - 130), 2)

    # Buttons below divider
    draw_button(pause_btn, "Resume" if paused else "Pause")
    draw_button(lap_btn, "Lap")

    pygame.display.flip()
    clock.tick(60)
