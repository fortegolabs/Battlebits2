import pygame as pg
from settings import *

class Score(pg.sprite.Sprite):

    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((300, ARENA_BORDER/2-10))

        self.rect = self.image.get_rect()
        self.rect.left = 40

        if player == PLAYER_1:
            self.rect.top = 10
        else:
            self.rect.bottom = HEIGHT - 10

        self.score = 0

    def addScore(self, add):
        self.score += add

    def update(self):
        self.image.fill(BLACK)

        t = pg.font.Font("res/digital-7 (mono).ttf", 50).render("Score: " + ("%d" % self.score).rjust(5,'-'), 1, RED)
        r = t.get_rect()
        r.center = (t.get_width()/2, t.get_height()/2+5)

        self.image.blit(t,r)