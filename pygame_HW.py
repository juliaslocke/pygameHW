import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

X_MAX = 800
Y_MAX = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

everything = pygame.sprite.Group()

class Mouse(pygame.sprite.Sprite):
	def __init__(self, groups):
		super(Mouse, self).__init__()
		self.image = pygame.image.load("mouse.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (X_MAX/2, Y_MAX)
		self.dx = self.dy = 0
		self.health = 3
		self.score = 0

		self.add(groups)
		self.velocity = 2
		self.autopilot = False

	def update(self):
		x, y = self.rect.center
		if not self.autopilot:
			self.rect.center = x + self.dx, y + self.dy

			if self.health < 0:
				self.kill()
		else:
			self.rect.center = x,y

	def move(self, direction, operation):
		v = 5
		if operation == START:
			if direction in (UP, DOWN):
				self.dy = {UP: -v, DOWN: v}[direction]
			if direction in (LEFT, RIGHT):
				self.dx = {LEFT: -v, RIGHT: v}[direction]
		if operation == STOP:
			if direction in (UP, DOWN):
				self.dy = 0
			if direction in (LEFT, RIGHT):
				self.dx = X_MAX/2

def main():
	game_over = False

	pygame.font.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((X_MAX, Y_MAX), DOUBLEBUF)
	mouse = pygame.sprite.Group()

	empty = pygame.Surface((X_MAX, Y_MAX))
	mousey = Mouse(everything)
	mousey.add(everything)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT or event.type == K_ESCAPE:
				sys.exit()
			if not game_over:
				if event.type == KEYDOWN:
					if event.key == K_DOWN:
						mousey.move(DOWN, START)
					if event.key == K_LEFT:
						mousey.move(LEFT, START)
					if event.key == K_RIGHT:
						mousey.move(RIGHT, START)
					if event.key == K_UP:
						mousey.move(UP, START)

				if event.type == KEYUP:
					if event.key == K_DOWN:
						mousey.move(DOWN, STOP)
					if event.key == K_LEFT:
						mousey.move(LEFT, STOP)
					if event.key == K_RIGHT:
						mousey.move(RIGHT, STOP)
					if event.key == K_UP:
						mousey.move(UP, STOP)

		if game_over:
			sys.exit()

		everything.clear(screen, empty)
		everything.update()
		everything.draw(screen)
		pygame.display.flip()
if __name__ == '__main__':
	main()