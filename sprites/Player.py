import pygame as pg
from settings import *
import os, random
from .PowerUps import PowerUps
from .StatusEffects import StatusEffects

class Player(pg.sprite.Sprite):
    def __init__(self, player):

        #Sprite members#
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("./res/labs_yellow.png") if player == PLAYER_2 else pg.image.load("./res/labs.jpg")
        self.image = pg.transform.scale(self.image, (self.image.get_width() * PLAYER_HEIGHT//self.image.get_height(), PLAYER_HEIGHT))
        self.rect = self.image.get_rect()

        self.position = random.randint(0, TARGETS-1)

        self.rect.centerx = SPRITE_STEP_RATE*self.position + SPRITE_STEP_RATE/2

        if player == PLAYER_1:
            self.rect.bottom = PLAYER_1_BOARDER
        else:
            self.rect.top = PLAYER_2_BOARDER
            self.image = pg.transform.flip(self.image, False, True)

        self.byte_window_active = False

        self.playerMoveSound = pg.mixer.Sound('res/move.wav')
        self.getPowerUpSound = pg.mixer.Sound('res/powerup.wav')

        #Player members#
        self.byte = 0x00
        self.direction = PLAYER_1_DIRECTION if player == PLAYER_1 else PLAYER_2_DIRECTION

        self.status = 0

        self.invertBitsTimer = 0
        self.swapEndianTimer = 0
        self.nibbleTimer = 0

        self.powerUps = PowerUps(player)
        self.statusEffects = StatusEffects(player)

        self.player = player

    def startNibblePU(self):
        self.statusEffects.nibble = True
        self.nibbleTimer = pg.time.get_ticks()/1000 + 5
        self.powerUps.hasNibblePU = False
        self.powerUps.updateImage = True

    def startSwapEndian(self):
        self.statusEffects.swapEndian = True
        self.swapEndianTimer = pg.time.get_ticks()/1000 + 5
        self.powerUps.updateImage = True

    def startInvertBits(self):
        self.statusEffects.invertBits = True
        self.invertBitsTimer = pg.time.get_ticks()/1000 + 5
        self.powerUps.updateImage = True

    def useSlow(self):
        if self.powerUps.lockout:
            return

        self.powerUps.startLockOut()
        self.powerUps.hasSlow = False
        self.powerUps.updateImage = True

    def useSwitch(self):
        self.powerUps.hasSwitch = False
        self.powerUps.updateImage = True

    def update_player_position(self, direction):
        if direction == PLAYER_MOVE_LEFT:
            if self.position > 0:
                self.position -= 1
                self.rect.x -= SPRITE_STEP_RATE
                self.image = pg.transform.flip(self.image, True, False)
                #self.playerMoveSound.play()
                return True

        elif direction == PLAYER_MOVE_RIGHT:
            if self.position < TARGETS-1:
                self.position += 1
                self.rect.x += SPRITE_STEP_RATE
                self.image = pg.transform.flip(self.image, True, False)
                #self.playerMoveSound.play()
                return True

        return False

    def assignPowerup(self):
        i = random.randint(0, 2)
        self.getPowerUpSound.play()

        # A little complicated but it makes sure you always get a new powerup
        # Could use an array instead but hopefully games won't last long enough to get 2 powerups
        x = i
        while True:
            if i == 0:
                if self.powerUps.hasNibblePU:
                    i = (i + 1) % 3
                else:
                    self.powerUps.hasNibblePU = True
                    break
            elif i == 1:
                if self.powerUps.hasInvertBitsPU:
                    i = (i + 1) % 3
                else:
                    self.powerUps.hasInvertBitsPU = True
                    break
            else:
                if self.powerUps.hasSwapEndianPU:
                    i = (i + 1) % 3
                else:
                    self.powerUps.hasSwapEndianPU = True
                    break
            if x==i:
                break
        self.powerUps.updateImage = True

    def checkState(self):
        time = pg.time.get_ticks()/1000
        if self.statusEffects.invertBits and self.invertBitsTimer <= time:
            self.statusEffects.invertBits = False
        if self.statusEffects.swapEndian and self.swapEndianTimer <= time:
            self.statusEffects.swapEndian = False
        if self.statusEffects.nibble and self.nibbleTimer <= time:
            self.statusEffects.nibble = False