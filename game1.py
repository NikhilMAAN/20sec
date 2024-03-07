import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player properties
player_size = 300
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 7
player_speed = 15  # New variable for player's horizontal speed
jumping = False
jump_count = 10

# Load character image
character_image = pygame.image.load("countryman.png")
character_image = pygame.transform.scale(character_image, (player_size, player_size))

# Load background image
background_image = pygame.image.load("359016.jpg")  # Replace "background.jpg" with your image file
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Ball properties
ball_size = 15
ball_speed = 1  # Reduced ball speed
balls = []

# Load background music
pygame.mixer.music.load("Music.mp3")  # Replace with the path to your background music file
pygame.mixer.music.set_volume(0.5)  # Adjust the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Running and Jumping Game")

# Font for displaying text
font = pygame.font.Font(None, 36)

# Initialize player lives
player_lives = 3

# Clock to control the frame rate
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not jumping:
        if keys[pygame.K_SPACE]:
            jumping = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10

    # Move player
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed

    # Move balls
    for ball in balls:
        ball[0] -= ball_speed
        if ball[0] <= 0:
            balls.remove(ball)

        # Collision detection with player
        if (
            player_x < ball[0] + ball_size
            and player_x + player_size > ball[0]
            and player_y < ball[1] < player_y + player_size
        ):
            player_lives -= 1
            print(f"Ouch! Lives remaining: {player_lives}")
            if player_lives == 0:
                print("Game Over!")
                pygame.quit()
                sys.exit()

    # Generate new balls only on the ground
    if random.randint(0, 50) == 0:
        balls.append([WIDTH, HEIGHT - ball_size - 7])  # Set the y-coordinate to the ground level

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw player (character)
    screen.blit(character_image, (player_x, player_y))

    # Draw balls
    for ball in balls:
        pygame.draw.rect(screen, RED, (ball[0], ball[1], ball_size, ball_size))

    # Draw lives
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 150, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
