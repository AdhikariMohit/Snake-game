import pygame
import time
import random
import os

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

# Initialize font for score
font_style = pygame.font.SysFont("bahnschrift", 20)

# Load High Score from File
high_score_file = "high_score.txt"

def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            return int(file.read().strip())
    return 0

def save_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

# Function to generate new position for food
def generate_food(snake_list):
    while True:
        food_x = random.randrange(0, WINDOW_X - snake_block, 10)
        food_y = random.randrange(BOUNDARY_HEIGHT, WINDOW_Y - snake_block, 10)
        if [food_x, food_y] not in snake_list:
            return food_x, food_y

# Function to display the score and high score
def display_score(score, high_score):
    value = font_style.render(f"Score: {score} | High Score: {high_score}", True, BLACK)
    game_window.blit(value, [10, 10])

# Function to draw the boundary
def draw_boundary():
    pygame.draw.line(game_window, BLACK, (0, BOUNDARY_HEIGHT), (WINDOW_X, BOUNDARY_HEIGHT), 2)

# Function to draw the snake
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.circle(game_window, GREEN, (x[0] + snake_block // 2, x[1] + snake_block // 2), snake_block // 2)

# Main game loop
def game_loop():
    game_close = False
    game_over_flag = False

    # Snake properties
    snake_x, snake_y = random.randrange(0, WINDOW_X - snake_block, 10), random.randrange(BOUNDARY_HEIGHT, WINDOW_Y - snake_block, 10)
    snake_list = []
    snake_length = 1

    # Initial direction
    direction = 'RIGHT'
    change_to = direction

    # Score
    score = 0
    high_score = load_high_score()

    # Food position
    food_x, food_y = generate_food(snake_list)

    while not game_close:

        while game_over_flag:
            game_window.fill(WHITE)
            game_over_msg = font_style.render(f"Game Over! Final Score: {score}", True, RED)
            game_window.blit(game_over_msg, [WINDOW_X // 6, WINDOW_Y // 3])
            high_score_msg = font_style.render(f"High Score: {high_score}", True, BLACK)
            game_window.blit(high_score_msg, [WINDOW_X // 6, WINDOW_Y // 2])
            restart_msg = font_style.render("Press 'R' to Restart or 'Q' to Quit", True, BLACK)
            game_window.blit(restart_msg, [WINDOW_X // 6, WINDOW_Y // 1.7])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_close = True
                        game_over_flag = False
                    if event.key == pygame.K_r:
                        game_loop()  # Restart without recursion

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to  # Apply direction change

        # Update snake position
        if direction == 'UP':
            snake_y -= snake_block
        elif direction == 'DOWN':
            snake_y += snake_block
        elif direction == 'LEFT':
            snake_x -= snake_block
        elif direction == 'RIGHT':
            snake_x += snake_block

        # Check for boundary collision
        if snake_x >= WINDOW_X or snake_x < 0 or snake_y >= WINDOW_Y or snake_y < BOUNDARY_HEIGHT:
            game_over_flag = True

        game_window.fill(WHITE)
        draw_boundary()

        # Draw food
        pygame.draw.rect(game_window, BLUE, [food_x, food_y, snake_block, snake_block])

        # Update snake position
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake collides with itself
        for block in snake_list[:-1]:
            if block == snake_head:
                game_over_flag = True

        # Draw snake
        draw_snake(snake_list)

        # Display score
        display_score(score, high_score)

        # Update the game screen
        pygame.display.update()

        # Check if snake eats food
        if snake_x == food_x and snake_y == food_y:
            food_x, food_y = generate_food(snake_list)  # Ensure food doesn't spawn inside snake
            snake_length += 1
            score += 1
            if score > high_score:
                high_score = score
                save_high_score(high_score)  # Save new high score

        # Control snake speed
        clock.tick(snake_speed)

    pygame.quit()

# Start the game
game_loop()
