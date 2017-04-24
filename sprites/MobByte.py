import pygame as pg
from settings import *
from random import randint

speedColors = { 1 : SPEED_COLOR_1, 2 : SPEED_COLOR_2, 2**2 : SPEED_COLOR_3, 2**3 : SPEED_COLOR_4, 2**4: SPEED_COLOR_5}

class MobByte(pg.sprite.Sprite):
    def __init__(self, position, byte_value, direction, difficulty):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((SPRITE_STEP_RATE,40))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.rect.left = position * SPRITE_STEP_RATE
        self.rect.centery = HEIGHT / 2

        pg.display.flip()

        self.position = position
        self.speed = 1
        self.direction = direction
        self.movingDirection = direction
        self.byte_value = byte_value
        self.difficulty = difficulty

        self.powerUp = False
        self.reset = True

        self.update_time = pg.time.get_ticks()

    def update(self):
        if self.powerUp or self.reset:
            self.image.fill(GREY if self.position % 2 ==0 else DARK_GREY)
            #font = pg.font.SysFont("monospace", 50)
            font = pg.font.Font("res/digital-7 (mono).ttf", 35)

            color = (randint(0x01, 0xFF), randint(0x01, 0xFF), randint(0x01, 0xFF)) if self.powerUp else speedColors.get(self.speed, SPEED_COLOR_5)

            textSurf = font.render('0x%02X' % self.byte_value, 1, color)
            textSurf_rect = textSurf.get_rect()
            textSurf_rect.center = (self.rect.width/2, self.rect.height/2)
            self.image.blit(textSurf, textSurf_rect)

        speedy = self.speed*self.movingDirection

        if self.update_time <= pg.time.get_ticks():
            self.rect.y += speedy
            self.update_time = pg.time.get_ticks() + BYTE_DELAY//self.difficulty

        if self.reset:
            self.reset = False