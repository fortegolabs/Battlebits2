import pygame as pg
from settings import *

class BitString(pg.sprite.Sprite):

    def __init__(self, player):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((WIDTH/3, ARENA_BORDER/2-10))

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2

        self.player = player

        if player == PLAYER_1:
            self.rect.top = 10
        else:
            self.rect.bottom = HEIGHT - 10

        self.byte = None
        self.target = None
        self.position = 7
        self.warn = False

        self.color = PLAYER_1_COLOR if player == PLAYER_1 else PLAYER_2_COLOR

    def setTarget(self, target, byte=0x00, position=7):
        self.byte = byte
        self.target = target
        self.position = position

    def nullify(self):
        self.byte = None

    def toggle(self):
        if self.byte != None:
            self.byte ^= 1 << self.position

    def move_right(self):
        if self.position > 0:
            self.position -= 1

    def move_left(self):
        if self.position < 7:
            self.position += 1

    def update(self):
        self.image.fill(BLACK)

        font = pg.font.Font("res/digital-7 (mono).ttf", 50)

        display = []

        headerFont = pg.font.Font("res/digital-7 (mono).ttf", 20)

        cb = headerFont.render('Current Byte   MSB                  LSB', 1, RED)
        tb = headerFont.render('Target Byte', 1, self.color)

        if self.byte == None:
            display.append(font.render("0x--", 1, RED))
            display.append(font.render("  ---- ----  ", 1, WHITE))
            display.append(font.render("0x--", 1, self.color))
        else:
            b = bin(self.byte)[2:].zfill(8)
            n1, n2 = b[:len(b)//2], b[len(b)//2:]

            display.append(font.render('0x%02X' % self.byte + "  ", 1, RED))

            if self.position > 3:
                display.append(font.render(n1[:7-self.position], 1, WHITE))
                display.append(font.render(n1[7-self.position], 1, RED))
                display.append(font.render(n1[8-self.position:], 1, WHITE))

                display.append(font.render(" " + n2, 1, WHITE))
            else:
                display.append(font.render(n1 + " ", 1, WHITE))

                display.append(font.render(n2[:3 - self.position], 1, WHITE))
                display.append(font.render(n2[3 - self.position], 1, RED))
                display.append(font.render(n2[4 - self.position:], 1, WHITE))

            display.append(font.render("  " + '0x%02X' % self.target, 1, self.color))

        rect = display[0].get_rect()

        total_width = sum(list(map(lambda t:t.get_width(), display)))

        rect.left = (self.rect.width - total_width)/2

        rect.centery = self.rect.height/2+5

        self.image.blit(cb, (rect.left, 0))

        for t in display:
            self.image.blit(t, rect)
            rect.centerx += t.get_width()

        self.image.blit(tb, ((self.rect.width + total_width)/2-tb.get_width(),0))