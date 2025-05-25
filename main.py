import pygame
import sys
from game_setup import *

def main():
    """
    Main function for the Flappy Bird game.
    Sets up Pygame, loads assets, runs the main loop with three states:
     - Menu:        choose difficulty
     - Playing:     flap bird, move pipes, detect collisions
     - Game Over:   show final score, click to return to Menu
    """
    # INITIALISE
    pygame.init()           # Initialize all Pygame modules
    pygame.font.init()      # Initialize font module
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Flappy Bird (Simplified)")
    clock = pygame.time.Clock()

    # LOAD GRAPHICS
    bg_image = pygame.image.load('images/bg_day.png').convert()
    land_image = pygame.image.load('images/land.png').convert_alpha()
    pipe_top_image = pygame.image.load('images/pipe_down.png').convert_alpha()
    pipe_bottom_image = pygame.image.load('images/pipe_up.png').convert_alpha()
    bird_image = pygame.image.load('images/bird0_0.png').convert_alpha()

    # Font text
    FONT = pygame.font.SysFont(None, 48)

    # Get dimensions for collision and placement
    pipe_w = pipe_top_image.get_width()
    pipe_h = pipe_top_image.get_height()
    land_h = land_image.get_height()

    # BIRD VARIABLES
    bird_x, bird_y = WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2
    bird_vel = 0           # vertical velocity
    gravity = 0.5         # how much velocity changes each frame
    flap_power = 9           # velocity given when we flap

    # DIFFICULTIES
    pipe_gap = 180             # vertical pipe gap
    pipe_speed = 3               # horizontal pipe speed

    x_land = 0

    # CREATE PIPE
    pipes = [
        create_pipe_pair(WINDOW_WIDTH,     pipe_gap, pipe_w, pipe_h),
        create_pipe_pair(WINDOW_WIDTH+300, pipe_gap, pipe_w, pipe_h)
    ]

    score = 0
    state = STATE_MENU

    # GAME LOOP
    while True:
        screen.blit(bg_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Cleanly exit on window close
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos  # mouse x, y

                if state == STATE_MENU:
                    # Check which difficulty button was clicked
                    if BTN_EASY.collidepoint(mx, my):
                        pipe_gap, pipe_speed = 220, 2
                        # Reset game variables for new session
                        score, bird_y, bird_vel = 0, WINDOW_HEIGHT//2, 0
                        pipes = [
                            create_pipe_pair(WINDOW_WIDTH,     pipe_gap, pipe_w, pipe_h),
                            create_pipe_pair(WINDOW_WIDTH+300, pipe_gap, pipe_w, pipe_h)
                        ]
                        state = STATE_PLAYING

                    elif BTN_MEDIUM.collidepoint(mx, my):
                        pipe_gap, pipe_speed = 180, 3
                        score, bird_y, bird_vel = 0, WINDOW_HEIGHT//2, 0
                        pipes = [
                            create_pipe_pair(WINDOW_WIDTH,     pipe_gap, pipe_w, pipe_h),
                            create_pipe_pair(WINDOW_WIDTH+300, pipe_gap, pipe_w, pipe_h)
                        ]
                        state = STATE_PLAYING

                    elif BTN_HARD.collidepoint(mx, my):
                        pipe_gap, pipe_speed = 150, 4
                        score, bird_y, bird_vel = 0, WINDOW_HEIGHT//2, 0
                        pipes = [
                            create_pipe_pair(WINDOW_WIDTH,     pipe_gap, pipe_w, pipe_h),
                            create_pipe_pair(WINDOW_WIDTH+300, pipe_gap, pipe_w, pipe_h)
                        ]
                        state = STATE_PLAYING

                elif state == STATE_PLAYING:
                    # When playing, click = bird flap
                    bird_vel = -flap_power

                elif state == STATE_GAMEOVER:
                    # After game over, click goes back to menu
                    state = STATE_MENU

        # RENDER & UPDATE BY STATE

        if state == STATE_MENU:
            # Draw menu title and buttons
            draw_text("Select Difficulty", screen,
                      WINDOW_WIDTH//2, WINDOW_HEIGHT//4, FONT)
            pygame.draw.rect(screen, GREEN,  BTN_EASY)
            pygame.draw.rect(screen, YELLOW, BTN_MEDIUM)
            pygame.draw.rect(screen, RED,    BTN_HARD)
            draw_text("Easy",  screen, BTN_EASY.centerx,   BTN_EASY.centery,   FONT)
            draw_text("Med",   screen, BTN_MEDIUM.centerx, BTN_MEDIUM.centery, FONT)
            draw_text("Hard",  screen, BTN_HARD.centerx,   BTN_HARD.centery,   FONT)

        elif state == STATE_PLAYING:
            # Apply gravity to bird's velocity
            bird_vel += gravity
            # Update bird's vertical position
            bird_y   += bird_vel

            # Build a Rect for collision detection
            bird_rect = pygame.Rect(bird_x, bird_y,
                                     bird_image.get_width(),
                                     bird_image.get_height())
            # Shrink it so the bird can brush pipes slightly
            hitbox = bird_rect.inflate(-8, -8)

            # Handle pipes: move, recycle, score, draw
            for p in pipes:
                top_r, bot_r, passed = p
                # Move pipes left
                top_r.x -= pipe_speed
                bot_r.x -= pipe_speed

                # If off-screen left, reset to right
                if top_r.x < -pipe_w:
                    top_r.x = WINDOW_WIDTH
                    bot_r.x = WINDOW_WIDTH
                    top_r.y   = random.randint(-300, -50)
                    bot_r.y   = top_r.y + pipe_h + pipe_gap
                    p[2]      = False    # mark not-yet-passed

                # If bird has passed this pipe pair, increase score once
                if not passed and top_r.x + pipe_w < bird_x:
                    score += 1
                    p[2] = True

                # Draw the two pipe images
                screen.blit(pipe_top_image,    (top_r.x,  top_r.y))
                screen.blit(pipe_bottom_image, (bot_r.x,  bot_r.y))

            # Draw the bird on top of everything
            screen.blit(bird_image, (bird_x, bird_y))

            # Scroll and draw ground
            x_land -= pipe_speed
            if x_land <= -WINDOW_WIDTH:
                x_land = 0
            screen.blit(land_image, (x_land, WINDOW_HEIGHT - land_h))
            screen.blit(land_image, (x_land + WINDOW_WIDTH,
                                     WINDOW_HEIGHT - land_h))

            # Check collisions with pipes or ground/top
            for top_r, bot_r, _ in pipes:
                if hitbox.colliderect(top_r) or hitbox.colliderect(bot_r):
                    state = STATE_GAMEOVER
            if bird_y >= WINDOW_HEIGHT - land_h or bird_y <= 0:
                state = STATE_GAMEOVER

            # Draw current score at top center
            draw_text(str(score), screen,
                      WINDOW_WIDTH//2, 50, FONT)

        else:  # STATE_GAMEOVER
            # Game over screen: only show “Game Over” and final score
            draw_text("Game Over!", screen,
                      WINDOW_WIDTH//2, WINDOW_HEIGHT//3, FONT)
            draw_text(f"Score: {score}", screen,
                      WINDOW_WIDTH//2, WINDOW_HEIGHT//2, FONT)
            draw_text("Click to return", screen,
                      WINDOW_WIDTH//2, WINDOW_HEIGHT*2//3, FONT)

        # FLIP DISPLAY & CAP FRAME RATE
        pygame.display.update()  # render everything to the screen
        clock.tick(60)           # cap at 60 frames per second

if __name__ == '__main__':
    main()
