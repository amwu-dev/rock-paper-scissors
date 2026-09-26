
from sys import exit
import pygame

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

GRAY = '#1C1C1C'
RED = '#e51b20'

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256

EDGE_PADDING = 2
ICON_SIZE = 16

MATRIX = None

RPS_SELECTION_IMG = None

class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

		img1 = Image.open('rock.png')
		img2 = Image.open('paper.png')
		img3 = Image.open('scissors.png')

		RPS_SELECTION_IMG = Image.new('RGB', (64, 64))

		cur_x = EDGE_PADDING
		cur_y = EDGE_PADDING

		RPS_SELECTION_IMG.paste(img1, (cur_x, cur_y))
		cur_x += ICON_SIZE
		RPS_SELECTION_IMG.paste(img2, (cur_x, cur_y))
		cur_x += ICON_SIZE
		RPS_SELECTION_IMG.paste(img3, (cur_x, cur_y))

	
	def run(self):
		self.display_surface.fill(RED)
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			pygame.display.update()
			MATRIX.SetImage(RPS_SELECTION_IMG.convert('RGB'))

if __name__ == '__main__':
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