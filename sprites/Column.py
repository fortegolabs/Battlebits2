import pygame as pg
from settings import *
from random import randint

class Column(pg.sprite.Sprite):
    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((COLUMNS, ARENA_HEIGHT-ARENA_BORDER))

        self.image.fill(GREY if position % 2 == 0 else DARK_GREY)

        self.rect = self.image.get_rect()

        self.rect.left = position*COLUMNS
        self.rect.top = ARENA_BORDER
