import pygame as pg
from settings import *
import os, random

class Bullet(pg.sprite.Sprite):
    def __init__(self, position, direction, mobByteTarget, player, slow=False):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((35, 60),pg.SRCALPHA, 32)

        self.rect = self.image.get_rect()
        self.rect.centerx = SPRITE_STEP_RATE*position + SPRITE_STEP_RATE/2

        if direction == PLAYER_2_DIRECTION:
            self.rect.bottom = ARENA_BORDER
        else:
            self.rect.top = ARENA_HEIGHT

        self.slow = slow

        self.direction = direction

        self.mobByteTarget = mobByteTarget
        self.player = player

        self.speed = 4

        self.hitSound = pg.mixer.Sound('res/hit3.wav')

        font = pg.font.Font("res/Nova Display.ttf", 10)
        font.set_bold(True)

        if slow:
            missile = ["/\\", "==", "==", "==", "\\>"]
        else:
            missile = ["/\\", "|||", "|||", "/ = \\", "|/*\\|"] if self.direction == PLAYER_1_DIRECTION else ["|\\*/|","\\ = /","|||","|||","\\/"]

        centery = 0

        color =  RED if slow else (PLAYER_1_COLOR if self.direction == PLAYER_2_DIRECTION else PLAYER_2_COLOR)

        for m in missile:
            text = font.render(m, True,color)
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.width/2
            text_rect.top = centery
            centery += 10
            self.image.blit(text, text_rect)

        pg.mixer.Sound('res/shoot.wav').play()

    def update(self):
        self.rect.y += (self.speed * self.direction)

        if self.rect.colliderect(self.mobByteTarget.rect):
            self.hitSound.play()

            self.mobByteTarget.reset = True

            if self.slow:
                self.mobByteTarget.speed //= 2
            else:
                self.mobByteTarget.movingDirection = self.direction
                self.mobByteTarget.speed *= 2

                if self.mobByteTarget.powerUp:
                    self.player.assignPowerup()
                    self.mobByteTarget.powerUp = False

            self.kill()

        if self.direction == DIRECTION_FALLING:
            if self.rect.y > HEIGHT + 10:
                self.kill()
        elif self.direction == DIRECTION_RISING:
            if self.rect.y < -10:
                self.kill()