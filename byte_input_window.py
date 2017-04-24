import pygame as pg
from settings import *
import os, random


"""IMCOMPLETE  NOTHING WORKING YET"""

class ByteInputWindow(pg.sprite.Sprite):
    def __init__(self, posx, posy, byte_selected):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((BYTE_WINDOW_WIDTH,BYTE_LAUNCHER_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        #self.rect.top = 5
        self.rect.left = posx
        self.rect.centery = posy
        
        
    def update(self):
        pass