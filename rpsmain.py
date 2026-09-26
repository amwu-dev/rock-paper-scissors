
from sys import exit
import pygame

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

GRAY = '#1C1C1C'
RED = '#e51b20'

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256

MATRIX = None

class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

	def run(self):
		self.display_surface.fill(RED)
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			pygame.display.update()

			pil_string_image = pygame.image.tostring(self.display_surface, "RGBA",False)
			pil_image = Image.fromstring("RGBA",(660,660),pil_string_image)
			MATRIX.SetImage(pil_image.convert('RGB'))

if __name__ == '__main__':
	main = Main()

	options = RGBMatrixOptions()
	options.rows = 64
	options.cols = 64
	options.chain_length = 1
	options.parallel = 1
	options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'

	MATRIX = RGBMatrix(options = options)

	main.run()