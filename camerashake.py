import pygame

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((640, 480))

# Create a surface that covers the entire screen
shake_surface = pygame.Surface((640, 480))
shake_rect = shake_surface.get_rect()

# Set the initial position of the shake surface
x, y = 0, 0

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Shake the screen by changing the position of the shake surface
    for i in range(10):
        x += 5
        y += 5
        shake_rect.topleft = (x, y)
        pygame.time.delay(50)
    x, y = 0, 0
    shake_rect.topleft = (x, y)

    # Draw the shake surface to the screen
    screen.blit(shake_surface, shake_rect)
    pygame.display.flip()

