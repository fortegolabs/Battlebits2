import pygame as pg
from settings import *

class StatusEffects(pg.sprite.Sprite):

    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((130, ARENA_BORDER/2-10))

        self.rect = self.image.get_rect()
        self.rect.right = WIDTH - POWER_UP_WIDTH - 75

        if player == PLAYER_1:
            self.rect.top = 10
        else:
            self.rect.bottom = HEIGHT - 10

        self.nibble = False
        self.swapEndian = False
        self.invertBits = False

        self.color = PLAYER_1_COLOR if player == PLAYER_1 else PLAYER_2_COLOR

        self.blinkTime = 0
        self.blinkColor = RED

    def update(self):

        if self.nibble or self.invertBits or self.swapEndian or self.blinkColor == RED:

            if self.blinkTime <= pg.time.get_ticks():
                self.blinkColor = RED if self.blinkColor == BLACK else BLACK
                self.blinkTime = pg.time.get_ticks() + STATUS_BLINK_TIME

                self.image.fill(BLACK)
                font = pg.font.Font("res/digital-7 (mono).ttf", 15)

                display = []

                display.append(font.render("Status Effects", 1, self.color))
                display.append(font.render("Nibble Solved", 1, self.blinkColor if self.nibble else BLACK))
                display.append(font.render("Inverted Bits", 1, self.blinkColor if self.invertBits else BLACK))
                display.append(font.render("Swapped Endianess", 1, self.blinkColor if self.swapEndian else BLACK))

                height = (self.rect.height - sum(list(map(lambda t: t.get_height(), display)))) / 2

                for t in display:
                    width = (self.rect.width - t.get_width()) / 2
                    self.image.blit(t, (width, height))
                    height += t.get_height()