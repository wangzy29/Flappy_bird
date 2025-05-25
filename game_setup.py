import pygame
import random

# The size of our game window (width x height)
WINDOW_WIDTH = 432
WINDOW_HEIGHT = 768

# COLOR
WHITE = (255, 255, 255)  # Pure white
GREEN = (0, 255, 0)      # Bright green
YELLOW = (255, 255, 0)    # Bright yellow
RED = (255, 0, 0)      # Pure red

# We'll keep track of whether we're in the menu, playing, or game-over screen
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2

# MENU BUTTONS
# Define three clickable rectangles for Easy/Medium/Hard
BTN_WIDTH = 100
BTN_HEIGHT = 50
BTN_Y = WINDOW_HEIGHT // 2 - BTN_HEIGHT // 2
# Position them left, center, and right
BTN_EASY = pygame.Rect(50, BTN_Y, BTN_WIDTH, BTN_HEIGHT)
BTN_MEDIUM = pygame.Rect((WINDOW_WIDTH - BTN_WIDTH)//2, BTN_Y, BTN_WIDTH, BTN_HEIGHT)
BTN_HARD = pygame.Rect(WINDOW_WIDTH - 50 - BTN_WIDTH, BTN_Y, BTN_WIDTH, BTN_HEIGHT)

def draw_text(text, surface, x, y, font, color=WHITE):

    txt_surf = font.render(text, True, color)      # Create a Surface with the text drawn
    txt_rect = txt_surf.get_rect(center=(x, y))   # Get its rect and center it at (x,y)
    surface.blit(txt_surf, txt_rect)               # Draw it onto the target surface

def create_pipe_pair(x, gap, pipe_w, pipe_h):

    # Randomly choose the top pipe's y position above the screen
    top_y    = random.randint(-300, -50)
    # Bottom pipe sits immediately below top + gap
    bottom_y = top_y + pipe_h + gap

    # Build the two rects
    top_rect    = pygame.Rect(x, top_y, pipe_w, pipe_h)
    bottom_rect = pygame.Rect(x, bottom_y, pipe_w, pipe_h)

    return [top_rect, bottom_rect, False]
