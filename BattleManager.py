from sprites.MobByte import MobByte
from sprites.Bullet import Bullet
from sprites.Score import Score
from settings import *
import random
class BattleManager(object):

    def __init__(self, all_sprites, difficulty):
        self.bytes = []
        self.all_sprites = all_sprites
        self.difficulty = difficulty
        DIR = [pow(-1, i) for i in range(0,TARGETS)]

        for m in range(TARGETS):
            self.generateNew(m, DIR.pop(random.randint(0, len(DIR)-1)))

        self.p1Score = Score(PLAYER_1)
        self.p2Score = Score(PLAYER_2)

        self.all_sprites.add(self.p1Score)
        self.all_sprites.add(self.p2Score)

    def submit(self, byte_value, player):
        mobByte = self.bytes[player.position]
        if mobByte.byte_value == byte_value:
            if mobByte.direction == DIRECTION_RISING and mobByte.movingDirection:
                self.p1Score.addScore(BASE_POINTS * mobByte.speed*self.difficulty)
            else:
                self.p2Score.addScore(BASE_POINTS * mobByte.speed*self.difficulty)

            self.all_sprites.add(Bullet(player.position, mobByte.movingDirection*-1, mobByte, player))
            mobByte.direction *= -1

            return True

        return False

    def generateNew(self, position, direction):
        mobByte = MobByte(position, random.randint(0, 255), direction, self.difficulty)
        self.bytes.insert(position, mobByte)
        self.all_sprites.add(mobByte)