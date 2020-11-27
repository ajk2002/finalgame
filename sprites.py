import pygame as pg
from settings import *
import math
import random


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.hitbox = (self.vx, self.vy, TILESIZE, TILESIZE)

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collisions(self, dir):
        if dir == 'x':

            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            point_hits = pg.sprite.spritecollide(self, self.game.points, False)
            for points in point_hits:
                points.hit()

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collisions('x')
        self.rect.y = self.y
        self.collisions('y')


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Point(pg.sprite.Sprite):
    def __init__(self, game, answernum):
        self.groups = game.all_sprites, game.points
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        if answernum == 0:
            self.image.fill((48, 105, 152))

        elif answernum == 1:
            self.image.fill((255, 0, 0))

        elif answernum == 2:
            self.image.fill((100, 100, 100))


        self.rect = self.image.get_rect()
        self.x = -5
        self.y = -5
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.answernum = answernum

    def hit(self):
        self.game.next_question(self.answernum) # answernum used as choice in show_answers

    def move_point(self, coords): # draws new points in random locations using the x and y.
        self.x = coords[0]
        self.y = coords[1]
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
