import pygame as pg
from settings import *

class PlayerName(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((WIDTH/5, HEIGHT/5))
        self.image.fill(DARK_GREY)

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2

        self.name = [0, 0, 0]

        self.position = 0

    def get_name(self):
        return "".join([chr(p + 65) for p in self.name])

    def moveLeft(self):
        if self.position > 0:
            self.position -= 1

    def moveRight(self):
        if self.position < 2:
            self.position += 1

    def increment(self):
        self.name[self.position] = (self.name[self.position] + 1) % 26

    def decrement(self):
        self.name[self.position] = (self.name[self.position] - 1) % 26

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.image.fill(DARK_GREY)
        font = pg.font.Font("res/PressStart2P.ttf", 40)

        text = ' '.join([chr(p + 65) for p in self.name])

        title = pg.font.Font("res/PressStart2P.ttf", 15).render("Enter Name:", True, YELLOW)
        title_rect = title.get_rect()
        title_rect.center = (self.rect.width/2, 30)

        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.rect.width/2, self.rect.height/2)

        index = font.render("  "*self.position + "_" + "  "*(2-self.position) , True, WHITE)
        index_rect = index.get_rect()
        index_rect.center = (self.rect.width/2, self.rect.height/2 + 10)

        self.image.blit(title, title_rect)
        self.image.blit(text_surface, text_rect)
        self.image.blit(index, index_rect)