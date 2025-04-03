import pygame
import respawn

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_Y = SCREEN_HEIGHT
CENTER_Y = SCREEN_HEIGHT // 2
CENTER_X = SCREEN_WIDTH // 2

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font(None , 25)

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
        # Change the x positions of the platforms
        move_platforms()

    if player.x + player.size > SCREEN_WIDTH:
        player.x = 0

def move_platforms():
    # Change the x positions of the platforms
    platforms[0].x += 100
    platforms[1].x += 100
    platforms[2].x += 100

def check_collisions(player, platforms):
    for platform in platforms:
        if player.y + player.size >= platform.y and player.y + player.size <= platform.y + 10:
            if player.x + player.size > platform.x and player.x < platform.x + platform.width:
                player.y = platform.y - player.size
                player.vel_y = 0
                player.on_ground = True

player = Player(200, 450, 5, red, 50)

platforms = [
    # starting platform
    pygame.Rect(100, SCREEN_HEIGHT - 100, 250, 20),
    # first jump
    pygame.Rect(400, SCREEN_HEIGHT - 150, 200, 20),
    pygame.Rect(600, SCREEN_HEIGHT - 200, 250, 20)
]

show_text = True
clock = pygame.time.Clock()

run = True
while run:
    screen.fill(black)

    respawn.check_respawn(player, GROUND_Y)

    ytext = font.render(f'y: {player.y}', True, white)
    screen.blit(ytext, (10, 10))
    xtext = font.render(f'x: {player.x}', True, white)
    screen.blit(xtext, (10, 40))

    if show_text:
        tutorialtext = font.render('Use the w key to jump and the a and d keys to move left and right press space to remove me', True, red)
        screen.blit(tutorialtext, (50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_text = False

    player.move()
    check_collisions(player, platforms)
    player.render()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.up()
    if keys[pygame.K_a]:
        player.left()
        player.on_ground = False
    if keys[pygame.K_d]:
        player.right()
        player.on_ground = False

    check_wall_collision(player)

    for platform in platforms:
        pygame.draw.rect(screen, green, platform)

    clock.tick(60)
    pygame.display.update()

pygame.quit()
