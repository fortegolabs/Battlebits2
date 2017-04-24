import pygame as pg
from settings import *
from random import randint

class Sweep(pg.sprite.Sprite):
    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((WIDTH, 30),pg.SRCALPHA, 32)

        self.rect = self.image.get_rect()
        self.rect.left = 0

        if player == PLAYER_1:
            self.rect.bottom = ARENA_BORDER
            self.direction = PLAYER_2_DIRECTION
        else:
            self.rect.top = ARENA_HEIGHT
            self.direction = PLAYER_1_DIRECTION

    def update(self):

        #self.image.fill(GREY if self.position % 2 == 0 else DARK_GREY)
        font = pg.font.Font("res/digital-7 (mono).ttf", 45)

        color = (randint(0x01, 0xFF), randint(0x01, 0xFF), randint(0x01, 0xFF))
        text = font.render("********"*10, True, color)
        text_rect = text.get_rect()
        text_rect.centerx = self.rect.width / 2
        text_rect.top = 0
        self.image.blit(text, text_rect)

        self.rect.y += (40 * self.direction)

        if self.direction == PLAYER_2_DIRECTION:
            if self.rect.bottom > ARENA_HEIGHT:
                self.kill()
        elif self.direction == PLAYER_1_DIRECTION:
            if self.rect.top < ARENA_BORDER:
                self.kill()