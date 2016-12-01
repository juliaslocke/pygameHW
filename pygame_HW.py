import random
import sys
import pygame
from pygame.locals import Rect, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, K_LEFT, K_UP, K_RIGHT, KEYUP

X_MAX = 800
Y_MAX = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

everything = pygame.sprite.Group()

class Mouse(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, groups, outside_group):
		super(Mouse, self).__init__()
		self.image = pygame.image.load("mouse.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = x_pos,y_pos
		self.x = x_pos
		self.y = y_pos
		self.health = 3
		self.score = 0
		self.level = 1
		self.add(groups)
		self.velocity = 2
		self.other_group = outside_group

	def move(self, direction, operation):
		v = 5
		if operation == START:
			if direction == UP:
				self.y -= v
			if direction == DOWN:
				self.y += v

			if direction == RIGHT:
				self.x += v
			if direction == LEFT:
				self.x -= v
		
		if operation == STOP:
			if direction in (UP, DOWN, LEFT, RIGHT):
				self.rect.center = self.x, self.y

	def update(self):
		if self.y == 0:
			self.score += 1
			self.y = Y_MAX
			self.x = X_MAX/2
			self.rect.center = self.x,self.y
			for each in self.other_group:
				each.speed_up()
			self.level += 1
		else:
			self.rect.center = self.x, self.y
		
		if self.x < 0:
			self.x = X_MAX -5
			self.rect.center = self.x, self.y
		if self.x > X_MAX:
			self.x = 5
			self.rect.center = self.x, self.y

		if self.health <= 0:
			sys.exit()

	def collision(self, target):
		return self.rect.colliderect(target)

class Cat(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, x_vel, groups):
		super(Cat, self).__init__()
		self.image = pygame.image.load("cat.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x_pos, y_pos)
		self.x = x_pos
		self.y = y_pos
		self.x_vel = x_vel

		self.add(groups)

	def move(self):
		self.x += self.x_vel
		if self.x > X_MAX:
			self.x = -10
		self.rect.center = self.x, self.y
	
	def speed_up(self):
		self.x_vel += 0.5

	def update(self):
		self.move()

class Cheese(pygame.sprite.Sprite):
	def __init__(self, x_pos, y_pos, mouse, groups):
		super(Cheese, self).__init__()
		self.image = pygame.image.load("cheese.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x_pos, y_pos)
		self.x = x_pos
		self.y = y_pos
		self.reappear_x = x_pos
		self.reappear_y = y_pos
		self.mouse = mouse
		self.add(groups)
		self.starter = 0
	
	def update(self):
		while self.starter <= 0:
			self.x = random.randint(20, X_MAX-20)
			self.y = random.randint(20, Y_MAX-20)
			self.rect.center = self.x,self.y
			self.starter += 1
	
	def move(self):
		self.x = random.randint(20, X_MAX-20)
		self.y = random.randint(20, Y_MAX-20)
		self.rect.center = self.x,self.y

class Stats(pygame.sprite.Sprite):
	def __init__(self, mouse, groups):
		super(Stats, self).__init__()
		self.image = pygame.Surface((100, 50))
		self.rect = self.image.get_rect()
		self.rect.topright = X_MAX, 0

		font = pygame.font.get_default_font()
		self.font = pygame.font.Font(font, 20)
		self.mouse = mouse
		self.add(groups)

	def update(self):
		score = self.font.render("Score : {}".format(self.mouse.score), True, (255,255,255))
		health = self.font.render("Lives : {}".format(self.mouse.health), True, (255,255,255))
		self.image.fill((0,0,0))
		self.image.blit(score, (0,0))
		self.image.blit(health, (0,30))

class Level_Stats(Stats):
	def __init__(self, mouse, groups):
		super(Level_Stats, self).__init__(mouse, groups)
		self.image = pygame.Surface((100, 50))
		self.rect.bottomleft = 0, Y_MAX

	def update(self):
		level = self.font.render("Level : {}".format(self.mouse.level), True, (255, 255, 255))
		self.image.fill((0,0,0))
		self.image.blit(level, (0,0))

def main():
	game_over = False

	pygame.font.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((X_MAX, Y_MAX))
	mouse = pygame.sprite.Group()
	cat = pygame.sprite.Group()
	collision = pygame.sprite.Group()
	cheese = pygame.sprite.Group()

	empty = pygame.Surface((X_MAX, Y_MAX))
	mousey = Mouse(X_MAX/2, Y_MAX, [everything, mouse], cat)
	kitty_list = [
	Cat(X_MAX-50, Y_MAX-165, 0.5, [everything, cat]),
	Cat(X_MAX-230, Y_MAX-165, 0.5, [everything, cat]),
	Cat(X_MAX-410, Y_MAX-165, 0.5, [everything, cat]),
	Cat(X_MAX-590, Y_MAX-165, 0.5, [everything, cat]),
	Cat(X_MAX-770, Y_MAX-165, 0.5, [everything, cat]),
	Cat(25, Y_MAX-300, 0.5, [everything, cat]),
	Cat(X_MAX-140, Y_MAX-300, 0.5, [everything, cat]),
	Cat(X_MAX-320, Y_MAX-300, 0.5, [everything, cat]),
	Cat(X_MAX-500, Y_MAX-300, 0.5, [everything, cat]),
	Cat(X_MAX-680, Y_MAX-300, 0.5, [everything, cat]),
	Cat(X_MAX-680, Y_MAX-300, 0.5, [everything, cat]),
	Cat(X_MAX-50, Y_MAX-435, 0.5, [everything, cat]),
	Cat(X_MAX-230, Y_MAX-435, 0.5, [everything, cat]),
	Cat(X_MAX-410, Y_MAX-435, 0.5, [everything, cat]),
	Cat(X_MAX-590, Y_MAX-435, 0.5, [everything, cat]),
	Cat(X_MAX-770, Y_MAX-435, 0.5, [everything, cat])]
	

	cheesey = Cheese(random.randint(0,X_MAX-20), random.randint(0,Y_MAX-20), mousey, [everything, cheese])
	game_status = Stats(mousey, everything)
	level_status = Level_Stats(mousey, everything)

	while True:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					game_over = True
			if not game_over:
				if event.type in [KEYDOWN, KEYUP]:
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

				if mousey.collision(cheesey):
					mousey.score += 2
					cheesey.move()
				for kitty in kitty_list:
					if mousey.collision(kitty):
						mousey.health -= 1
						mousey.x = X_MAX/2
						mousey.y = Y_MAX
						mousey.rect.center = mousey.x,mousey.y

		if game_over:
			sys.exit()

		everything.clear(screen, empty)
		everything.update()
		everything.draw(screen)
		pygame.display.flip()
if __name__ == '__main__':
	main()
