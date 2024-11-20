import pygame  # type: ignore
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Catch the Falling Apples!')

# Load images
background_image = pygame.image.load(r'C:\Users\Dell\Desktop\Python\game\images\background1.png')
basket_image = pygame.image.load(r'C:\Users\Dell\Desktop\Python\game\images\basket.png')
apple_image = pygame.image.load(r'C:\Users\Dell\Desktop\Python\game\images\apple.png')
score_image = pygame.image.load(r'C:\Users\Dell\Desktop\Python\game\images\apple.png')  # Placeholder for score image

# Scale images to fit the screen
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
basket_image = pygame.transform.scale(basket_image, (100, 100))
apple_image = pygame.transform.scale(apple_image, (50, 50))
score_image = pygame.transform.scale(score_image, (50, 50))  # Adjust the size as needed

# Basket settings
basket_x = SCREEN_WIDTH // 2 - 50  # Center the basket on the screen
basket_y = SCREEN_HEIGHT - 90
basket_speed = 20

# Apple settings
apple_speed = 4
apples = []  # List to store apple positions

# Function to initialize apples
def init_apples(num_apples):
    global apples
    apples = []
    for _ in range(num_apples):  # Initial number of apples
        apple_x = random.randint(0, SCREEN_WIDTH - 30)
        apple_y = random.randint(-100, -30)
        apples.append([apple_x, apple_y])

# Initialize apples
init_apples(2)

# Score
score = 0
high_score = 0
font = pygame.font.SysFont(None, 28)  # Reduced font size to fit the screen

def update_apple_speed():
    global apple_speed
    # Increase apple speed based on score
    apple_speed = 4 + (score // 5)  # Increases speed every 5 points

def show_score(x, y):
    # Display the score image
    screen.blit(score_image, (x, y))
    
    # Render the score text with a different font size
    score_font = pygame.font.SysFont(None, 50)  # Adjust the size as needed
    score_text = score_font.render(str(score), True, BLACK)
    
    # Adjust margin by changing the y-coordinate
    margin_top = 10  # Adjust this value to control the margin
    screen.blit(score_text, (x + score_image.get_width() + 5, y + margin_top))

def show_game_over():
    global high_score
    if score > high_score:
        high_score = score
    
    # Adjusted Y-coordinates to move text further down
    game_over_text = font.render("Game Over!", True, RED)
    play_again_text = font.render("Press ENTER to Play Again", True, BLACK)
    high_score_text = font.render("High Score: " + str(high_score), True, BLACK)
    final_score_text = font.render("Your Score: " + str(score), True, BLACK)

    # Move text down by increasing the offset
    offset = 2
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - offset))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - offset + 40))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - offset + 80))
    screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 - offset + 120))

    pygame.display.flip()

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    button_text = font.render(text, True, BLACK)
    screen.blit(button_text, (x + (width // 2 - button_text.get_width() // 2), y + (height // 2 - button_text.get_height() // 2)))

def start_game():
    global game_started
    game_started = True

# Function to reset the game state
def reset_game():
    global score, basket_x
    init_apples(2)  # Reset to initial number of apples
    score = 0
    basket_x = SCREEN_WIDTH // 2 - 50
    update_apple_speed()  # Reset apple speed

# Game loop
running = True
game_started = False
game_over = False

while running:
    # Draw the background image
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_started:
            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Enter key to play again
                        game_over = False
                        reset_game()
                    elif event.key == pygame.K_ESCAPE:  # Escape key to exit
                        pygame.quit()
                        sys.exit()

    if not game_started:
        # Display start button
        draw_button("Start Game", SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 25, 150, 50, GREEN, RED, start_game)
    elif not game_over:
        # Basket movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - 100:
            basket_x += basket_speed

        # Move apples
        for apple in apples:
            apple[1] += apple_speed

            # Check if the apple is caught by the basket
            if apple[1] + 30 >= basket_y and basket_x < apple[0] < basket_x + 100:
                score += 1
                apple[0] = random.randint(0, SCREEN_WIDTH - 30)
                apple[1] = random.randint(-100, -30)
                update_apple_speed()  # Update apple speed when catching an apple

                # Add more apples every 10 points
                if score % 10 == 0:
                    init_apples(len(apples) + 1)

            # Check if apple falls beyond the screen without being caught
            if apple[1] > SCREEN_HEIGHT:
                game_over = True

            # Draw apple
            screen.blit(apple_image, (apple[0], apple[1]))

        # Draw basket
        screen.blit(basket_image, (basket_x, basket_y))

        # Show score
        show_score(10, 10)

    else:
        # Show game over screen
        show_game_over()

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(30)

pygame.quit()
