from sys import exit
import pygame

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont

import random

GRAY = "#1C1C1C"
GREEN = "#05a205"

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256

PICTURE_SIZE = 64
EDGE_PADDING = 2
ICON_SIZE = 16

MATRIX = None


# Converts a PIL image to Pygame surface
def convert_image(img):
    pygame_surface = pygame.image.frombytes(
        img.tobytes(),
        img.size,
        img.mode,
    )
    pygame_surface = pygame_surface.convert_alpha()
    return pygame_surface


class Main:
    def __init__(self):
        pygame.init()
        random.seed()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        img1 = Image.open("rock.png")
        img2 = Image.open("paper.png")
        img3 = Image.open("scissors.png")

        self.RPS_SELECTION_IMG = Image.new("RGB", (PICTURE_SIZE, PICTURE_SIZE))

        self.mode = "main_screen"
        cur_x = EDGE_PADDING
        cur_y = EDGE_PADDING
        self.rps_map = {1: "rock", 2: "paper", 3: "scissors"}
        self.rps_img_map = {1: img1, 2: img2, 3: img3}

        self.RPS_SELECTION_IMG.paste(img1, (cur_x, cur_y))
        cur_x += ICON_SIZE
        self.RPS_SELECTION_IMG.paste(img2, (cur_x, cur_y))
        cur_x += ICON_SIZE
        self.RPS_SELECTION_IMG.paste(img3, (cur_x, cur_y))

        self.draw_text_rps()
        self.OLD_RPS_SELECTION_IMG = self.RPS_SELECTION_IMG.copy()
        self.BASE_RPS_SELECTION_IMG = self.RPS_SELECTION_IMG.copy()

    # Draws text at bottom of selection screen
    def draw_text_rps(self):
        draw = ImageDraw.Draw(self.RPS_SELECTION_IMG)
        font = ImageFont.truetype("impact.ttf", size=13)
        # draw.text((0, ICON_SIZE + ICON_SIZE), "Rock", fill="white",font=font,align ="middle")
        # draw.text((ICON_SIZE, ICON_SIZE + ICON_SIZE), "Paper",  fill="white",font=font,align ="middle")
        # draw.text((ICON_SIZE + ICON_SIZE, ICON_SIZE + ICON_SIZE), "Scissors", font=font,fill="white",align ="middle")
        draw.text(
            (3, ICON_SIZE + 3), "      WIN TO ", font=font, fill="white", align="middle"
        )
        draw.text(
            (3, ICON_SIZE + 3 + 13),
            "GET CANDY!",
            font=font,
            fill="white",
            align="middle",
        )

    # Victory Screen
    def draw_victory(self):
        img = Image.new("RGB", (PICTURE_SIZE, PICTURE_SIZE))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("impact.ttf", size=13)
        draw.text((3, 3), "YOU WON ", font=font, fill="white", align="middle")
        draw.text((3, 3 + 13), "   CANDY!", font=font, fill="white", align="middle")
        # MATRIX.SetImage(self.RPS_SELECTION_IMG)

        return img

    # Tie screen
    def draw_tie(self):
        img = Image.new("RGB", (PICTURE_SIZE, PICTURE_SIZE))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("impact.ttf", size=13)
        draw.text((12, 12), "YOU TIED", font=font, fill="white", align="middle")
        # MATRIX.SetImage(self.RPS_SELECTION_IMG)

        return img

    # Loss screen
    def draw_loss(self):
        img = Image.new("RGB", (PICTURE_SIZE, PICTURE_SIZE))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("impact.ttf", size=13)
        draw.text((12, 12), ":(", font=font, fill="white", align="middle")
        # MATRIX.SetImage(self.RPS_SELECTION_IMG)

        return img

    # Draws boxes around the rock-paper-scissors selection
    def draw_box(self, i):
        self.RPS_SELECTION_IMG = self.BASE_RPS_SELECTION_IMG.copy()
        self.RPS_SELECTION_IMG_DRAW = ImageDraw.Draw(self.RPS_SELECTION_IMG)
        self.RPS_SELECTION_IMG_DRAW.line(
            [
                (ICON_SIZE * (i - 1), 0),
                (ICON_SIZE * i, 0),
            ],
            fill="white",
            width=3,
            joint="curve",
        )  # Horizontal top
        self.RPS_SELECTION_IMG_DRAW.line(
            [
                (ICON_SIZE * i, 0),
                (ICON_SIZE * i, ICON_SIZE),
            ],
            fill="white",
            width=3,
            joint="curve",
        )  # vertical right
        self.RPS_SELECTION_IMG_DRAW.line(
            [(ICON_SIZE * (i - 1), ICON_SIZE), (ICON_SIZE * (i), ICON_SIZE)],
            fill="white",
            width=3,
            joint="curve",
        )  # Horizontal bottom
        self.RPS_SELECTION_IMG_DRAW.line(
            [
                (ICON_SIZE * (i - 1), 0),
                (ICON_SIZE * (i - 1), ICON_SIZE),
            ],
            fill="white",
            width=3,
            joint="curve",
        )  # vertical left
        MATRIX.SetImage(self.RPS_SELECTION_IMG)
        return convert_image(self.RPS_SELECTION_IMG)

    # player versus AI
    def versus(self, player_selection):
        player1 = player_selection
        player2 = random.randint(1, 3)
        player1_selection = self.rps_map[player1]
        player2_selection = self.rps_map[player2]
        winner = 1
        tie = False
        if player1_selection == player2_selection:
            tie = True
        elif (
            (player1_selection == "rock" and player2_selection == "scissors")
            or (player1_selection == "paper" and player2_selection == "rock")
            or (player1_selection == "scissors" and player2_selection == "paper")
        ):
            winner = 0
        # --------------------- AI selection animation -----------------
        old_time = pygame.time.get_ticks()
        new_time = old_time

        background = Image.new("RGB", (PICTURE_SIZE, PICTURE_SIZE))
        background.paste(self.rps_img_map[player1], (ICON_SIZE, 17))
        img = Image.new("RGB", (PICTURE_SIZE, PICTURE_SIZE))
        x = ICON_SIZE + ICON_SIZE  # try and hit 1/3
        j = 0
        while new_time - old_time < 1200:
            j += 1
            pygame.time.wait(144)
            new_time = pygame.time.get_ticks()
            MATRIX.SetImage(img)
            pygame_surface = convert_image(img)
            self.display_surface.blit(pygame_surface, (0, 0))
            img = background.copy()
            img.paste(self.rps_img_map[j % 3 + 1], (x, 17))
            pygame.display.update()
        j = 1
        while j <= 3:
            pygame.time.wait(144)
            new_time = pygame.time.get_ticks()
            MATRIX.SetImage(img)
            pygame_surface = convert_image(img)
            self.display_surface.blit(pygame_surface, (0, 0))
            img = background.copy()
            selection = j % 3 + 1
            img.paste(self.rps_img_map[selection], (x, 17))
            pygame.display.update()
            j += 1
            if selection == player2_selection:
                break
        # --------------------- floating animation ---------------------
        img = self.floating_animation(
            self.rps_img_map[player1], self.rps_img_map[player2], winner=winner, tie=tie
        )
        # --------------------------------------------------------------
        if tie:
            img = self.draw_tie()
        elif winner == 0:
            img = self.draw_victory()
        else:
            img = self.draw_loss()
        MATRIX.SetImage(img)
        pygame_surface = convert_image(img)
        self.display_surface.blit(pygame_surface, (0, 0))
        return img


    # The animation for each victorious player
    # A floating rock, paper, or scissor for who is victorious or if it was a tie, both float slowly
    def floating_animation(
        self,
        img1,
        img2,
        winner=0,
        tie=False,
        coor1=(ICON_SIZE, 17),
        coor2=(ICON_SIZE + ICON_SIZE, 17),
        t=1200,
    ):
        old_time = pygame.time.get_ticks()
        new_time = old_time
        # background = img.copy()
        background = Image.new("RGB", (PICTURE_SIZE, PICTURE_SIZE))
        img = Image.new("RGB", (PICTURE_SIZE, PICTURE_SIZE))
        x, y = coor1  # try and hit 1/3
        w, z = coor2

        while new_time - old_time < t:
            if y > 0:
                if tie:
                    y -= 1
                    z -= 1
                elif winner == 0:
                    y -= 1
                else:
                    z -= 1
            img.paste(img1, (x, y))
            img.paste(img2, (w, z))
            pygame.time.wait(144)
            new_time = pygame.time.get_ticks()
            MATRIX.SetImage(img)
            pygame_surface = convert_image(img)
            self.display_surface.blit(pygame_surface, (0, 0))
            img = background.copy()
            pygame.display.update()
        return img

    # The main game logic
    def run(self):
        self.display_surface.fill(GREEN)
        i = 1
        pygame_surface = self.draw_box(i)
        self.display_surface.blit(pygame_surface, (0, 0))
        end = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif self.mode == "main_screen":
                    keys = pygame.key.get_pressed()
                    if event.type == pygame.KEYDOWN:
                        if keys[pygame.K_LEFT]:
                            i -= 1
                            if i == 0:
                                i = 3
                            pygame_surface = self.draw_box(i)
                            self.display_surface.blit(pygame_surface, (0, 0))
                            end = False
                        elif keys[pygame.K_RIGHT]:
                            i += 1
                            if i == 4:
                                i = 1
                            pygame_surface = self.draw_box(i)
                            self.display_surface.blit(pygame_surface, (0, 0))

                            end = False
                        elif keys[pygame.K_SPACE] and not end:
                            pygame_surface = self.versus(i)
                            end = True
                            pygame.event.clear()

                            # MATRIX.SetImage(self.RPS_SELECTION_IMG)

            pygame.display.update()


if __name__ == "__main__":
    main = Main()

    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'
    options.disable_hardware_pulsing = True
    options.pwm_bits = 3
    options.gpio_slowdown = 5
    options.limit_refresh_rate_hz = 144
    MATRIX = RGBMatrix(options = options)

    main.run()
