# imports
import pygame, sys
from respawn import check_respawn
from button import Button
import respawn

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
GAMEICON = pygame.image.load("assets/icon.png")
GAME_BG = pygame.image.load("assets/Game_Background.png")

def game_over():
    while True:
        GAMEOVER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(white)

        GAMEOVER_TEXT = get_font(100).render(
            "GAME OVER!", True, "Black"
        )
        GAMEOVER_RECT = GAMEOVER_TEXT.get_rect(center=(640, 260))  # x, y
        SCREEN.blit(GAMEOVER_TEXT, GAMEOVER_RECT)

        GAMEOVER_CONTINUE = Button(
                image=None,
                pos=(640, 400),
                text_input="CONTINUE",
                font=get_font(75),
                base_color=red,
                hovering_color="Orange",
            )

        GAMEOVER_CONTINUE.changeColor(GAMEOVER_MOUSE_POS)
        GAMEOVER_CONTINUE.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GAMEOVER_CONTINUE.checkForInput(GAMEOVER_MOUSE_POS):
                    main_menu()
        pygame.display.update()

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

        def render(self):
            pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.size))

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


    levels = [
        [pygame.Rect(100, SCREEN_HEIGHT - 100, 250, 20),
         pygame.Rect(400, SCREEN_HEIGHT - 150, 200, 20),
         pygame.Rect(700, SCREEN_HEIGHT - 200, 250, 20)],

        [pygame.Rect(200, SCREEN_HEIGHT - 120, 200, 20),
         pygame.Rect(600, SCREEN_HEIGHT - 180, 150, 20),
         pygame.Rect(1000, SCREEN_HEIGHT - 230, 150, 20)],

        [pygame.Rect(100, SCREEN_HEIGHT - 100, 100, 20),
         pygame.Rect(300, SCREEN_HEIGHT - 200, 100, 20),
         pygame.Rect(500, SCREEN_HEIGHT - 300, 100, 20),
         pygame.Rect(760, SCREEN_HEIGHT - 300, 100, 20),
         pygame.Rect(1000, SCREEN_HEIGHT - 400, 150, 20)],

         [pygame.Rect(100, SCREEN_HEIGHT - 40, 70, 20),
          pygame.Rect(300, SCREEN_HEIGHT - 40, 70, 20),
          pygame.Rect(500, SCREEN_HEIGHT - 40, 70, 20),
          pygame.Rect(700, SCREEN_HEIGHT - 40, 70, 20),
          pygame.Rect(900, SCREEN_HEIGHT - 40, 70, 20),
          pygame.Rect(1100, SCREEN_HEIGHT - 40, 70, 20)],

         [pygame.Rect(100, SCREEN_HEIGHT - 230, 150, 200)]
    ]

    current_level = 0
    platforms = levels[current_level]

    player = Player(200, 570, 5, black, 50)

    def check_wall_collision(player):
        nonlocal current_level, platforms
        if player.x < 0:
            player.x = 0

        if player.x + player.size >= SCREEN_WIDTH:
            current_level += 1
            if current_level >= len(levels):
                current_level = 0
            platforms = levels[current_level]

            first_platform = platforms[0]
            player.x = first_platform.x + 10
            player.y = first_platform.y - player.size
            player.vel_y = 0


    def check_collisions(player, platforms):
        for platform in platforms:
            if (player.y + player.size >= platform.y and
                player.y + player.size <= platform.y + 10 and
                player.x + player.size > platform.x and
                player.x < platform.x + platform.width):
                player.y = platform.y - player.size
                player.vel_y = 0
                player.on_ground = True

    clock = pygame.time.Clock()
    show_text = True

    deaths = 0

    while True:
        SCREEN.fill(black)
        SCREEN.blit(GAME_BG, (0, 0))

        if deaths == 3:
            game_over()
        if player.y >= 670:
            deaths  += 1

        check_respawn(player, levels, current_level)

        ytext = get_font(25).render(f"y: {player.y}", True, black)
        xtext = get_font(25).render(f"x: {player.x}", True, black)
        XTEXT_RECT = xtext.get_rect(center=(100, 35))
        YTEXT_RECT = ytext.get_rect(center=(100, 70))  # x, y
        SCREEN.blit(xtext, XTEXT_RECT)
        SCREEN.blit(ytext, YTEXT_RECT)

        if show_text:
            tutorialtext = get_font(18).render(
                "Use WAD or Arrow Keys | Space to hide text | ESC to quit",
                True, red)
            SCREEN.blit(tutorialtext, (200, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_text = False
                elif event.key == pygame.K_ESCAPE:
                    main_menu()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.up()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.left()
            player.on_ground = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.right()
            player.on_ground = False

        player.move()
        check_collisions(player, platforms)
        check_wall_collision(player)
        player.render()

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

pygame.display.set_caption("Square Adventure")
pygame.display.set_icon(GAMEICON)

main_menu()

pygame.quit()
