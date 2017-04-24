import pygame as pg
import random
from settings import *

class Stack(pg.sprite.Sprite):

    def __init__(self, player, level):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((WIDTH, STACK_HEIGHT))

        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.left = 0

        if player == PLAYER_1:
            self.rect.top = ARENA_BORDER + STACK_HEIGHT*level
        else:
            self.rect.bottom = ARENA_HEIGHT - STACK_HEIGHT*level

        text = " [STACK 0x%02X] " % level + ''.join([chr(x%2+0x30) for x in random.sample(range(100), 15)])

        binary = pg.font.Font("res/PressStart2P.ttf", 8).render(text, True, PLAYER_1_COLOR if player == PLAYER_1 else PLAYER_2_COLOR)

        binary_rect = binary.get_rect()
        binary_rect.centery = self.rect.height/2
        for i in range(0, int(self.rect.width/binary.get_width())+1):
            binary_rect.left = binary_rect.width*i #- level*20
            self.image.blit(binary, binary_rect)
