import pygame
import random

class Enemy(pygame.sprite.Sprite):
	def __init__(self, SCREEN_WIDTH, y, image, scale):
		pygame.sprite.Sprite.__init__(self)
		#define variables
		self.direction = random.choice([-1, 1])
		if self.direction == 1:
			self.flip = True
		else:
			self.flip = False

		#select starting image and create rectangle from it
		self.image = pygame.transform.scale(enemy_image, (30, 30))
		self.rect = self.image.get_rect()

		if self.direction == 1:
			self.rect.x = 0
		else:
			self.rect.x = SCREEN_WIDTH
		self.rect.y = y

	def update(self, scroll, SCREEN_WIDTH):
		#move enemy
		self.rect.x += self.direction * 2
		self.rect.y += scroll

		#check if gone off screen
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()


