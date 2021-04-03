import pygame
from random import randint

pygame.init()

win = pygame.display.set_mode((500, 620))
clock = pygame.time.Clock()

class Sprite(pygame.sprite.Sprite):
	def __init__(self, image, size, x, y, speed):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load(image), size)
		self.speed = speed
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def write(self):
		win.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(Sprite):
	def update(self):
		self.rect.y += self.speed

	def randomPos(self): self.rect.x, self.rect.y = randint(0, 428), randint(0, 30)


class Bullet(Sprite):
	def update(self): 
		self.rect.y -= self.speed

class Player(Sprite):
	Bullets = pygame.sprite.Group()
	hp = 5
	def update(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] and self.rect.x > 10:
			self.rect.x -= self.speed
		elif keys[pygame.K_d] and self.rect.x < 400:
			self.rect.x += self.speed

player = Player('x-wing.png', (90, 68), 0, 500, 8)
Enemys = pygame.sprite.Group()
for i in range(5): Enemys.add(Enemy('nlo.png', (72,48), randint(0, 428), randint(0, 100), 5))

kills = 0
stopLose = False
stopWin = False
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and not stopLose:
				player.Bullets.add(Bullet('bullet.png', (12, 25), player.rect.x, player.rect.y, 10))
				player.Bullets.add(Bullet('bullet.png', (12, 25), player.rect.x+78, player.rect.y, 10))
			if event.key == pygame.K_r:
				if stopLose or stopWin:
					stopLose = False
					stopWin = False
					Enemys = pygame.sprite.Group()
					for i in range(5): Enemys.add(Enemy('nlo.png', (72,48), randint(0, 428), randint(0, 100), 5))

	
	win.fill((17, 31, 40))

	if not stopLose and not stopWin:
		text = pygame.font.Font(None, 64).render('kills'+str(kills)+"  hp"+str(player.hp), True, (0, 180, 0))
		player.update()
		player.write()

		for enemy in Enemys:
			enemy.update()
			enemy.write()
			if enemy.rect.y >= 620:
				player.hp -= 1
				enemy.randomPos()
		for bullet in player.Bullets:
			bullet.update()
			bullet.write()
			if bullet.rect.y < 0: bullet.kill()

		for enemy in pygame.sprite.spritecollide(player, Enemys, False): 
			enemy.randomPos()
			player.hp -= 1
		for enemy in pygame.sprite.groupcollide(Enemys, player.Bullets, False, True):
			enemy.randomPos()
			kills += 1

		if player.hp <= 0:
			stopLose = True
		if kills == 200 and player.hp >= 4:
			stopWin = True

	if stopLose: 
		text = pygame.font.Font(None, 64).render('You lose', True, (180, 0, 0))
		kills = 0
		player.hp = 5
	if stopWin:
		text = pygame.font.Font(None, 64).render('You Win', True, (0, 180, 0))
		kills = 0
		player.hp = 5

	win.blit(text, (0, 0))

	clock.tick(60)
	pygame.display.update()