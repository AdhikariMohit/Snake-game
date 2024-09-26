import pygame
import time
import random
import math

# Game settings
snake_speed = 15
window_x = 720
window_y = 480

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Set up game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (Frames per second) controller
fps = pygame.time.Clock()

# Load font for displaying score
font = pygame.font.Font(pygame.font.match_font('arial'), 30)

# Snake initial settings
snake_pos = [100, 50]  # Starting position
snake_body = [[100, 50], [90, 50], [80, 50]]  # Snake body segments
direction = 'RIGHT'  # Initial direction
change_to = direction  # To store change in direction

# Food position
food_pos = [random.randrange(1, (window_x // 10)) * 10,
            random.randrange(1, (window_y // 10)) * 10]
food_spawn = True

# Score
score = 0

# Game Loop
def game_loop():
    global change_to, direction, snake_pos, snake_body, food_pos, food_spawn, score

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        # Validate direction changes
        if change_to == 'UP':
            direction = 'UP'
        if change_to == 'DOWN':
            direction = 'DOWN'
        if change_to == 'LEFT':
            direction = 'LEFT'
        if change_to == 'RIGHT':
            direction = 'RIGHT'

        # Update snake position
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        
        # Check for food consumption
        if snake_pos == food_pos:
            score += 1
            food_spawn = False  # Food has been eaten
        else:
            snake_body.pop()  # Remove last segment to create movement

        # Food generation
        if not food_spawn:
            food_pos = [random.randrange(1, (window_x // 10)) * 10,
                        random.randrange(1, (window_y // 10)) * 10]
        food_spawn = True  # Food is ready to be eaten again

        # Fill the screen with black color
        game_window.fill(black)

        # Draw the snake with curves and a face
        for i, pos in enumerate(snake_body):
            pygame.draw.circle(game_window, green, (pos[0] + 5, pos[1] + 5), 5)  # Draw body segments
            if i == 0:  # Draw the snake head with a face
                pygame.draw.circle(game_window, green, (pos[0] + 5, pos[1] + 5), 10)  # Head
                pygame.draw.circle(game_window, white, (pos[0] + 3, pos[1] + 3), 3)  # Left eye
                pygame.draw.circle(game_window, white, (pos[0] + 7, pos[1] + 3), 3)  # Right eye
                pygame.draw.arc(game_window, black, (pos[0] + 3, pos[1] + 5, 4, 4), math.radians(0), math.radians(180), 1)  # Mouth

        # Draw the food
        pygame.draw.circle(game_window, red, (food_pos[0] + 5, food_pos[1] + 5), 5)  # Food

        # Display score
        score_text = font.render(f'Score: {score}', True, white)
        game_window.blit(score_text, [10, 10])

        # Control game speed
        fps.tick(snake_speed)

        # Control snake appearance on opposite side
        if snake_pos[0] < 0:
            snake_pos[0] = window_x - 10
        elif snake_pos[0] >= window_x:
            snake_pos[0] = 0
        if snake_pos[1] < 0:
            snake_pos[1] = window_y - 10
        elif snake_pos[1] >= window_y:
            snake_pos[1] = 0

        # Update the game display
        pygame.display.update()

        # Check for collisions
        for block in snake_body[1:]:
            if snake_pos == block:
                running = False  # End the game if snake hits itself

    # Exit game
    pygame.quit()
    print(f'Game Over! Your final score is: {score}')

# Start the game
if __name__ == "__main__":
    game_loop()
