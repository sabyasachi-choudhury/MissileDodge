import pygame
import random

from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)

pygame.mixer.init()

point_sound = pygame.mixer.Sound("point.wav")
up_sound = pygame.mixer.Sound("Rising_putter.ogg")
down_sound = pygame.mixer.Sound("Falling_putter.ogg")
coll_sound = pygame.mixer.Sound("Collision.ogg")
bg_music = pygame.mixer.Sound("better_music.mp3")
bg_music.play(loops=-1)


class CreatePlayer(pygame.sprite.Sprite):
    def __init__(self):
        super(CreatePlayer, self).__init__()
        self.surf = pygame.transform.smoothscale(pygame.image.load("spacejet.png").convert(), (85, 56))
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(center=(s_width/2, s_height/2))

    def move(self, press):
        player_speed = 6

        if press[K_UP]:
            self.rect.move_ip(0, -player_speed)
            up_sound.play()
        if press[K_DOWN]:
            self.rect.move_ip(0, player_speed)
            down_sound.play()
        if press[K_LEFT]:
            self.rect.move_ip(-player_speed, 0)
        if press[K_RIGHT]:
            self.rect.move_ip(player_speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > s_width:
            self.rect.right = s_width
        if self.rect.bottom > s_height:
            self.rect.bottom = s_height
        if self.rect.top < 0:
            self.rect.top = 0


class CreateEnemies(pygame.sprite.Sprite):
    def __init__(self):
        super(CreateEnemies, self).__init__()
        self.surf = pygame.image.load("spr_missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(-30, 0),
                random.randint(35, s_height)
            )
        )
        self.speed = random.randint(4, 7)

    def move(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > s_width:
            self.kill()


class CreateClouds(pygame.sprite.Sprite):
    def __init__(self):
        super(CreateClouds, self).__init__()
        self.surf = pygame.transform.smoothscale(pygame.image.load("SingleCloud.png").convert(), (80, 40))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(-30, 0),
                random.randint(35, s_height)
            )
        )
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.speed = random.randint(3, 6)

    def move(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > s_width:
            self.kill()


class CreateCoins(pygame.sprite.Sprite):
    def __init__(self):
        super(CreateCoins, self).__init__()
        self.surf = pygame.transform.smoothscale(pygame.image.load("Coin.png").convert(), (30, 30))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(-30, 0),
                random.randint(0, s_height)
            )
        )
        self.surf.set_colorkey((0, 0, 0))
        self.speed = 5

    def move(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > s_width:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super(Explosion, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("explosion.png").convert(), (200, 200))
        self.surf.set_colorkey((255, 255, 255))
        self.rect = self.surf.get_rect(center=(player.rect.left, player.rect.top + 28))


global missile_rate
missile_rate = 400

pygame.init()

s_width = 1000
s_height = 700

add_enemy = pygame.USEREVENT + 1
pygame.time.set_timer(add_enemy, missile_rate)

add_cloud = pygame.USEREVENT + 2
pygame.time.set_timer(add_cloud, 900)

add_coin = pygame.USEREVENT + 3
pygame.time.set_timer(add_coin, 1500)

screen = pygame.display.set_mode((s_width, s_height))
player = CreatePlayer()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
clouds = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites.add(player)

run = True
points = 0

while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False

        elif event.type == add_enemy:
            enemy = CreateEnemies()
            enemies.add(enemy)
            all_sprites.add(enemy)
            missile_rate = missile_rate - 100

        if event.type == add_cloud:
            cloud = CreateClouds()
            clouds.add(cloud)
            all_sprites.add(cloud)

        if event.type == add_coin:
            coin = CreateCoins()
            all_sprites.add(coin)
            coins.add(coin)

    pressed = pygame.key.get_pressed()
    player.move(pressed)
    screen.fill((94, 247, 247))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    for enemy in enemies:
        enemy.move()
    for cloud in clouds:
        cloud.move()
    for coin in coins:
        coin.move()

    if pygame.sprite.spritecollideany(player, enemies):
        up_sound.stop()
        down_sound.stop()
        coll_sound.play()
        expl = Explosion()
        screen.blit(expl.surf, expl.rect)
        player.kill()
        run = False
    if pygame.sprite.spritecollideany(player, clouds):
        cloud.kill()
    if pygame.sprite.spritecollideany(player, coins):
        coin.kill()
        point_sound.play()
        points = points + 1

    pygame.display.flip()
    pygame.time.Clock().tick(100)

print("You earned a total of", points, "points!")
pygame.quit()