import pygame
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CENTER_Y = SCREEN_HEIGHT // 2
CENTER_X = SCREEN_WIDTH // 2

# Variables
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Square Adventure")

class Player():
    def __init__(self, x, y, speed, colour, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.colour = colour

        self.vel_y = 0
        self.on_ground = True

    def render(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.size, self.size))

    def up(self):
        if self.on_ground:
            self.vel_y = -12  # A smaller negative value for slower jump height
            self.on_ground = False

    def move(self):
        self.y += self.vel_y

        # Gravity (slowed down further to make the player fall slower)
        if not self.on_ground:
            self.vel_y += 0.4  # Slower gravity pull for slower descent

        # Prevent falling through the floor
        if self.y >= SCREEN_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - self.size
            self.vel_y = 0
            self.on_ground = True

    def right(self):
        self.x = self.x + self.speed

    def left(self):
        self.x = self.x - self.speed


player = Player(CENTER_X, CENTER_Y, 3, red, 50)  # x, y, speed, colour, size

run = True
while run:
    screen.fill(black)

    player.move()
    player.render()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.up()
    if keys[pygame.K_a]:
        player.left()
    if keys[pygame.K_d]:
        player.right()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
