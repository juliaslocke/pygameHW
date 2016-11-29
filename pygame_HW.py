import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

X_MAX = 800
Y_MAX = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

everything = pygame.sprite.Group()

# class Collision(pygame.sprite.Sprite):
# 	def __init__(self, obj1, obj2):
# 		super(Collision, self).__init__()
# 		#self.obj1_position = (obj1.x_pos, obj1.y_pos)
# 		#self.obj2_position = (obj2.x_pos, obj2.y_pos)
# 		self.image1 = obj1.image
# 		self.image2 = obj2.image
# 		self.obj1rect = obj1.rect.center
# 		self.obj2rect = obj2.rect.center
# 		#print(self.obj1rect)
# 		#print(self.obj2rect)
# 		#self.obj1rect.center = obj1.x,obj1.y
# 		#self.obj2rect.center = obj2.x,obj2.y
# 		self.add(everything)

# 	def update(self):
# 		x1,y1 = self.obj1rect
# 		x2,y2 = self.obj2rect
# 		#x1,y1 = (5,0)
# 		#x2,y2 = (6,8)
# 		health = 3
# 		if (x1 == x2) or (y1 == y2):
# 			health -= 1
# 			if health > 1:
# 				obj1.kill()
# 				game_over = True
# 				sys.exit()

class Mouse(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, groups):
		super(Mouse, self).__init__()
		self.image = pygame.image.load("mouse.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = x_pos,y_pos
		self.x = x_pos
		self.y = y_pos
		self.health = 3
		self.score = 0

		self.add(groups)
		self.velocity = 2
		self.autopilot = False

	def move(self, direction, operation):
		v = 5
		if operation == START:
			if direction == UP:
				self.y -= v
			if direction == DOWN:
				self.y += v
				#self.dy = {UP: -v, DOWN: v}[direction]

			if direction == RIGHT:
				self.x += v
			if direction == LEFT:
				self.x -= v
				#self.dx = {LEFT: -v, RIGHT: v}[direction]
		
		if operation == STOP:
			if direction in (UP, DOWN, LEFT, RIGHT):
				self.rect.center = self.x, self.y
				#self.dy = 0
			#if direction in (LEFT, RIGHT):
			#	self.dx = X_MAX/2

	def update(self):
		#x, y = self.rect.center
		# if not self.autopilot:
			# self.rect.center = x + self.x, y + self.y
		if self.y == 0:
			self.y = Y_MAX
			self.x = X_MAX/2
			self.rect.center = self.x,self.y
		else:
			self.rect.center = self.x, self.y
		
		if self.x < 0:
			self.x = X_MAX -5
			self.rect.center = self.x, self.y
		if self.x > X_MAX:
			self.x = 5
			self.rect.center = self.x, self.y

		if self.health < 0:
			self.kill()
		# else:
		# 	self.rect.center = x,y

class Cat(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, groups):
		super(Cat, self).__init__()
		self.image = pygame.image.load("cat.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x_pos, y_pos)
		self.x = x_pos
		self.y = y_pos

		self.add(groups)

	def move(self):
		x_vel = 1
		self.x += x_vel
		if self.x > X_MAX:
			self.x = -10
		self.rect.center = self.x, self.y

	def update(self):
		self.move()


class Stats(pygame.sprite.Sprite):
	def __init__(self, mouse, groups):
		super(Stats, self).__init__()
		self.image = pygame.Surface((X_MAX, 30))
		self.rect = self.image.get_rect()
		self.rect.bottomleft = 0, Y_MAX

		font = pygame.font.get_default_font()
		self.font = pygame.font.Font(font, 20)
		self.mouse = mouse
		self.add(groups)
	def update(self):
		score = self.font.render("Score : {}".format(self.mouse.score), True, (255,255,255))
		self.image.fill((0,0,0))
		self.image.blit(score, (0,0))

def main():
	game_over = False

	pygame.font.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((X_MAX, Y_MAX), DOUBLEBUF)
	mouse = pygame.sprite.Group()
	cat = pygame.sprite.Group()
	collision = pygame.sprite.Group()

	empty = pygame.Surface((X_MAX, Y_MAX))
	mousey = Mouse(X_MAX/2, Y_MAX, everything)
	mousey.add(everything)
	kitty_list = [
	Cat(X_MAX-50, Y_MAX-165, everything),
	Cat(X_MAX-230, Y_MAX-165, everything),
	Cat(X_MAX-410, Y_MAX-165, everything),
	Cat(X_MAX-590, Y_MAX-165, everything),
	Cat(X_MAX-770, Y_MAX-165, everything),
	Cat(25, Y_MAX-300, everything),
	Cat(X_MAX-140, Y_MAX-300, everything),
	Cat(X_MAX-320, Y_MAX-300, everything),
	Cat(X_MAX-500, Y_MAX-300, everything),
	Cat(X_MAX-680, Y_MAX-300, everything),
	Cat(X_MAX-680, Y_MAX-300, everything),
	Cat(X_MAX-50, Y_MAX-435, everything),
	Cat(X_MAX-230, Y_MAX-435, everything),
	Cat(X_MAX-410, Y_MAX-435, everything),
	Cat(X_MAX-590, Y_MAX-435, everything),
	Cat(X_MAX-770, Y_MAX-435, everything)]
	
	for kitty in kitty_list:
		kitty.add(everything)
		# run_in = Collision(mousey, kitty)
		# run_in.add(everything)

	game_status = Stats(mousey, everything)

	while True:
		for event in pygame.event.get():
			if event.type == K_ESCAPE:
				if event.key == K_ESCAPE:
					sys.exit()
			if not game_over:
				if event.type in [KEYDOWN, KEYUP, K_LEFT, K_RIGHT]:
					if event.key == K_DOWN:
						mousey.move(DOWN, START)
						mousey.move(DOWN, START)
						mousey.move(DOWN, STOP)
					if event.key == K_LEFT:
						mousey.move(LEFT, START)
						mousey.move(LEFT, START)
						mousey.move(LEFT, STOP)
					if event.key == K_RIGHT:
						mousey.move(RIGHT, START)
						mousey.move(RIGHT, START)
						mousey.move(RIGHT, STOP)
					if event.key == K_UP:
						mousey.move(UP, START)
						mousey.move(UP, START)
						mousey.move(UP, STOP)

				#if event.type == KEYUP:
					#if event.key == K_DOWN:
					#	mousey.move(DOWN, STOP)
					#if event.key == K_LEFT:
					#	mousey.move(LEFT, STOP)
					#if event.key == K_RIGHT:
					#	mousey.move(RIGHT, STOP)
					#if event.key == K_UP:
						#mousey.move(UP, STOP)

		if game_over:
			sys.exit()

		everything.clear(screen, empty)
		everything.update()
		everything.draw(screen)
		pygame.display.flip()
if __name__ == '__main__':
	main()
