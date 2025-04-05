# imports
import pygame, sys
import respawn
from button import Button

pygame.init()

#consts
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GROUND_Y = SCREEN_HEIGHT
CENTER_Y = SCREEN_HEIGHT // 2
CENTER_X = SCREEN_WIDTH // 2

# colours
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

#background
BG = pygame.image.load("assets/Background.png")

# font for main menu
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


# the game
def play():
    class Player:
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
            pygame.draw.rect(
                SCREEN, self.colour, (self.x, self.y, self.size, self.size)
            )

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

    player = Player(200, 570, 5, red, 50)

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
            if (
                player.y + player.size >= platform.y
                and player.y + player.size <= platform.y + 10
            ):
                if (
                    player.x + player.size > platform.x
                    and player.x < platform.x + platform.width
                ):
                    player.y = platform.y - player.size
                    player.vel_y = 0
                    player.on_ground = True

    platforms = [
        # starting platform
        pygame.Rect(100, SCREEN_HEIGHT - 100, 250, 20),
        # first jump
        pygame.Rect(400, SCREEN_HEIGHT - 150, 200, 20),
        pygame.Rect(600, SCREEN_HEIGHT - 200, 250, 20),
    ]

    clock = pygame.time.Clock()

    show_text = True
    while True:
        SCREEN.fill(black)

        respawn.check_respawn(player, GROUND_Y)

        ytext = font.render(f"y: {player.y}", True, white)
        SCREEN.blit(ytext, (10, 10))
        xtext = font.render(f"x: {player.x}", True, white)
        SCREEN.blit(xtext, (10, 40))

        if show_text:
            tutorialtext = font.render(
                "Use the w key to jump and the a and d keys to move left and right press space to remove me",
                True,
                red,
            )
            SCREEN.blit(tutorialtext, (50, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_text = False

        player.move()
        check_collisions(player, platforms)
        player.render()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            player.up()
        if keys[pygame.K_a]:
            player.left()
            player.on_ground = False
        if keys[pygame.K_d]:
            player.right()
            player.on_ground = False
        if keys[pygame.K_ESCAPE]:
            main_menu()

        check_wall_collision(player)

        for platform in platforms:
            pygame.draw.rect(SCREEN, green, platform)

        clock.tick(60)
        pygame.display.update()

# options menu
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")
        brightness = 0

        OPTIONS_TEXT = get_font(45).render(
            "This is the OPTIONS screen.", True, "Black"
        )
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))  # x, y
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(
            image=None,
            pos=(640, 680),
            text_input="BACK",
            font=get_font(75),
            base_color="Black",
            hovering_color="Green",
        )
        BRIGHTNESS = Button(
            image=None,
            pos=(640, 600),
            text_input="BRIGHTNESS: {}".format(brightness),
            font=get_font(50),
            base_color="Black",
            hovering_color=(255, 255, 0),
        )

        BRIGHTNESS.changeColor(OPTIONS_MOUSE_POS)
        BRIGHTNESS.update(SCREEN)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if BRIGHTNESS.checkForInput(OPTIONS_MOUSE_POS):
                    brightness = brightness + 25

        pygame.display.update()

# main menu
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(
            image=pygame.image.load("assets/Play Rect.png"),
            pos=(640, 250),
            text_input="PLAY",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        OPTIONS_BUTTON = Button(
            image=pygame.image.load("assets/Options Rect.png"),
            pos=(640, 400),
            text_input="OPTIONS",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )
        QUIT_BUTTON = Button(
            image=pygame.image.load("assets/Quit Rect.png"),
            pos=(640, 550),
            text_input="QUIT",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font(None, 25)

pygame.display.set_caption("Square Adventure")

main_menu()

pygame.quit()
