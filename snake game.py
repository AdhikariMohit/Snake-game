import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Define game window dimensions
WINDOW_X = 720
WINDOW_Y = 480
BOUNDARY_HEIGHT = 40

# Setup game window
game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
pygame.display.set_caption('Snake Game')

# Set up game clock
clock = pygame.time.Clock()

# Snake properties
snake_block = 10
snake_speed = 15
snake_list = []
snake_length = 1

# Initialize font for score
font_style = pygame.font.SysFont("bahnschrift", 20)

# Define the initial position of the snake and food
def initial_positions():
    return (random.randrange(0, WINDOW_X - snake_block) // 10 * 10,
            random.randrange(BOUNDARY_HEIGHT, WINDOW_Y - snake_block) // 10 * 10)

snake_x, snake_y = initial_positions()
food_x, food_y = initial_positions()

# Function to display the score and high score
def display_score(score, high_score):
    value = font_style.render(f"Score: {score} | High Score: {high_score}", True, BLACK)
    game_window.blit(value, [0, 0])

# Function to draw the boundary
def draw_boundary():
    pygame.draw.line(game_window, BLACK, (0, BOUNDARY_HEIGHT), (WINDOW_X, BOUNDARY_HEIGHT), 2)

# Function to draw the snake
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.circle(game_window, GREEN, (x[0] + snake_block // 2, x[1] + snake_block // 2), snake_block // 2)

# Game over function
def game_over(score, high_score):
    game_window.fill(WHITE)
    game_over_msg = font_style.render(f"Game Over! Final Score: {score}", True, RED)
    game_window.blit(game_over_msg, [WINDOW_X // 6, WINDOW_Y // 3])
    high_score_msg = font_style.render(f"High Score: {high_score}", True, BLACK)
    game_window.blit(high_score_msg, [WINDOW_X // 6, WINDOW_Y // 2])
    restart_msg = font_style.render("Press 'R' to Restart or 'Q' to Quit", True, BLACK)
    game_window.blit(restart_msg, [WINDOW_X // 6, WINDOW_Y // 1.7])
    pygame.display.update()
    time.sleep(2)

# Main game loop
def game_loop():
    game_over_flag = False
    game_close = False
    global snake_x, snake_y, snake_list, snake_length, food_x, food_y

    direction = 'RIGHT'
    change_to = direction

    score = 0
    high_score = 0

    while not game_close:

        while game_over_flag:
            game_over(score, high_score)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_close = True
                        game_over_flag = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Prevent the snake from reversing
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Update snake position
        if direction == 'UP':
            snake_y -= snake_block
        if direction == 'DOWN':
            snake_y += snake_block
        if direction == 'LEFT':
            snake_x -= snake_block
        if direction == 'RIGHT':
            snake_x += snake_block

        # Boundaries check
        if snake_x >= WINDOW_X or snake_x < 0 or snake_y >= WINDOW_Y or snake_y < BOUNDARY_HEIGHT:
            game_over_flag = True

        game_window.fill(WHITE)
        draw_boundary()

        # Respawn food if eaten
        pygame.draw.rect(game_window, BLUE, [food_x, food_y, snake_block, snake_block])

        # Add snake position
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for collisions
        for block in snake_list[:-1]:
            if block == snake_head:
                game_over_flag = True

        # Draw snake and update score
        draw_snake(snake_block, snake_list)
        display_score(score, high_score)

        # Update the game screen
        pygame.display.update()

        # Check if snake eats food
        if snake_x == food_x and snake_y == food_y:
            food_x, food_y = initial_positions()
            snake_length += 1
            score += 1
            if score > high_score:
                high_score = score

        # Control snake speed
        clock.tick(snake_speed)

    pygame.quit()

# Start the game
game_loop()
