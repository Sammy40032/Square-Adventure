import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CENTER_Y = SCREEN_HEIGHT // 2
CENTER_X = SCREEN_WIDTH // 2

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
        self.last_jump_time = 0

    def render(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.size, self.size))

    def up(self):
        if self.on_ground:
            self.vel_y = -10
            self.on_ground = False

    def move(self):
        self.y += self.vel_y

        if not self.on_ground:
            self.vel_y += 0.4

        if self.y >= SCREEN_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - self.size
            self.vel_y = 0
            self.on_ground = True

    def right(self):
        self.x += self.speed

    def left(self):
        self.x -= self.speed

def check_wall_collision(player):
    if player.x < 0:
        player.x = 0
    if player.x + player.size > SCREEN_WIDTH:
        player.x = SCREEN_WIDTH - player.size

player = Player(CENTER_X, SCREEN_HEIGHT - 50 - 50, 5, red, 50) # x, y, speed, colour, size

clock = pygame.time.Clock()

run = True
while run:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    player.move()
    player.render()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.up()
    if keys[pygame.K_a]:
        player.left()
    if keys[pygame.K_d]:
        player.right()

    check_wall_collision(player)

    clock.tick(60)

    pygame.display.update()

pygame.quit()
