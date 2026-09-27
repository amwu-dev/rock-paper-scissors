from sys import exit
import pygame

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont

GRAY = "#1C1C1C"
GREEN = "#05a205"

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256

EDGE_PADDING = 2
ICON_SIZE = 16

MATRIX = None


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        img1 = Image.open("rock.png")
        img2 = Image.open("paper.png")
        img3 = Image.open("scissors.png")

        self.RPS_SELECTION_IMG = Image.new("RGB", (64, 64))


        self.mode = "main_screen"
        cur_x = EDGE_PADDING
        cur_y = EDGE_PADDING

        self.RPS_SELECTION_IMG.paste(img1, (cur_x, cur_y))
        cur_x += ICON_SIZE
        self.RPS_SELECTION_IMG.paste(img2, (cur_x, cur_y))
        cur_x += ICON_SIZE
        self.RPS_SELECTION_IMG.paste(img3, (cur_x, cur_y))

        self.draw_text_rps()
        self.OLD_RPS_SELECTION_IMG = self.RPS_SELECTION_IMG.copy()
        self.BASE_RPS_SELECTION_IMG = self.RPS_SELECTION_IMG.copy()

    def draw_text_rps(self):
        draw = ImageDraw.Draw(self.RPS_SELECTION_IMG)
        font = ImageFont.truetype("impact.ttf", size=5)
        draw.text((0, ICON_SIZE + ICON_SIZE), "Rock", fill="white",font=font,align ="middle") 
        draw.text((ICON_SIZE, ICON_SIZE + ICON_SIZE), "Paper",  fill="white",font=font,align ="middle") 
        draw.text((ICON_SIZE + ICON_SIZE, ICON_SIZE + ICON_SIZE), "Scissors", font=font,fill="white",align ="middle") 

    def draw(self, i):
        self.RPS_SELECTION_IMG = self.BASE_RPS_SELECTION_IMG.copy()
        self.RPS_SELECTION_IMG_DRAW = ImageDraw.Draw(self.RPS_SELECTION_IMG)
        self.RPS_SELECTION_IMG_DRAW.line(
            [
                (ICON_SIZE * (i - 1),0),
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
            [
                (ICON_SIZE * (i - 1), ICON_SIZE), 
                (ICON_SIZE * (i), ICON_SIZE)
            ],
            fill="white",
            width=3,
            joint="curve",
        )  # Horizontal bottom
        self.RPS_SELECTION_IMG_DRAW.line(
            [
                (ICON_SIZE * (i-1), 0),
                (ICON_SIZE * (i-1), ICON_SIZE),
            ],
            fill="white",
            width=3,
            joint="curve",
        )  # vertical left
        pygame_surface = pygame.image.frombytes(
            self.RPS_SELECTION_IMG.tobytes(),
            self.RPS_SELECTION_IMG.size,
            self.RPS_SELECTION_IMG.mode,
        )
        pygame_surface = pygame_surface.convert_alpha()

        return pygame_surface
    
    def run(self):
        self.display_surface.fill(GREEN)
        i = 1
        pygame_surface = self.draw(i)
        self.display_surface.blit(pygame_surface, (0, 0))
        MATRIX.SetImage(self.RPS_SELECTION_IMG)

        while True:
            for event in pygame.event.get():
                print(event)
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
                            pygame_surface = self.draw(i)
                            self.display_surface.blit(pygame_surface, (0, 0))
                            MATRIX.SetImage(self.RPS_SELECTION_IMG)

                        elif keys[pygame.K_RIGHT]:
                            i += 1
                            if i == 4:
                                i = 1
                            pygame_surface = self.draw(i)
                            self.display_surface.blit(pygame_surface, (0, 0))
                            MATRIX.SetImage(self.RPS_SELECTION_IMG)

            pygame.display.update()
            #MATRIX.SetImage(self.RPS_SELECTION_IMG)


if __name__ == "__main__":
    main = Main()

    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'
    options.disable_hardware_pulsing = True

    MATRIX = RGBMatrix(options = options)

    main.run()
