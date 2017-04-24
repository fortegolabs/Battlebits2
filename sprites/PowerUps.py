import pygame as pg
from settings import *

class PowerUps(pg.sprite.Sprite):

    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((POWER_UP_WIDTH, ARENA_BORDER/2-10))

        self.rect = self.image.get_rect()
        self.rect.right = WIDTH - 40

        if player == PLAYER_1:
            self.rect.top = 10
        else:
            self.rect.bottom = HEIGHT - 10

        self.hasSlow = True
        self.hasSwitch = True

        self.hasNibblePU = False
        self.hasInvertBitsPU = False
        self.hasSwapEndianPU = False

        self.updateImage = True

        self.color = PLAYER_1_COLOR if player == PLAYER_1 else PLAYER_2_COLOR
        self.color2 = self.color

        self.lockout = False
        self.targetTime = 0
        self.time = 0

    def startLockOut(self):
        self.lockout = True
        self.targetTime = pg.time.get_ticks()/1000 + POWERUP_LOCKOUT_SECONDS
        self.color2 = GREY

    def update(self):

        time = 0

        if self.lockout:
            self.time = pg.time.get_ticks()/1000
            self.updateImage = True

            time = int(self.targetTime - self.time)

            if time<=0:
                self.lockout = False
                self.color2 = self.color

        if self.updateImage:
            self.image.fill(BLACK)

            font = pg.font.Font("res/digital-7 (mono).ttf", 30)
            font_small = pg.font.Font("res/digital-7 (mono).ttf", 25)

            row1 = []
            row2 = []

            row1.append(font.render("Power Ups: ", 1, RED))
            row1.append(font.render("Shoot ", 1, self.color if self.hasSwitch else BLACK))
            row1.append(font.render("Slow ", 1, self.color if self.hasSlow else BLACK))
            row2.append(font_small.render(str(time).rjust(2,'0'), 1, WHITE))
            row2.append(font.render("Invert ", 1, self.color2 if self.hasInvertBitsPU else BLACK))
            row2.append(font.render("Nibble ", 1, self.color2 if self.hasNibblePU else BLACK))
            row2.append(font.render("Swap", 1, self.color2 if self.hasSwapEndianPU else BLACK))

            offset = (self.rect.width - sum(list(map(lambda t: t.get_width(), row1)))) / 2 + 15

            height = (self.rect.height - row2[1].get_height() - row1[0].get_height()) / 2

            for t in row1:
                self.image.blit(t, (offset, height))
                offset += t.get_width()

            offset = (self.rect.width - sum(list(map(lambda t: t.get_width(), row2)))) / 2 + 15
            height += row2[1].get_height()

            for t in row2:
                self.image.blit(t, (offset, height))
                offset += t.get_width()

            self.updateImage = False