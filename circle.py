import pygame
import math

# Initialize Pygame
pygame.init()

# Set the window size and caption
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Rotating Circle")


class Battle_invisCircle():
    def __init__(self,centre_x,centre_y,radius,angle,angular_velocity,line_width):
        self.centre_x, self.centre_y = centre_x, centre_y
        self.radius = radius
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.line_width = line_width
        self.colour = (255,0,0,0)
        self.top_x, self.top_y = 0,0
        
    def update(self):
        # Update the angle
        self.angle += self.angular_velocity
        # Convert the angle to radians
        radians = math.radians(self.angle)
        # Calculate the position of the top point
        self.top_x = self.centre_x + self.radius * math.cos(radians)
        self.top_y = self.centre_y + self.radius * math.sin(radians)

    def draw(self):
        # Draw the circle
        pygame.draw.circle(screen, self.colour, (self.centre_x, self.centre_y), self.radius, self.line_width)

circle = Battle_invisCircle(200, 200, 100, 0, 5, 1)

# Set the framerate
framerate = 60
clock = pygame.time.Clock()

# Run the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    circle.update()
    circle.draw()

    # Update the display
    pygame.display.flip()

    # Limit the framerate
    clock.tick(framerate)

# Quit Pygame
pygame.quit()
