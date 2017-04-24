import pygame as pg
import random
from datetime import datetime
#from battlenet import BattleBitsNet
from BattleManager import BattleManager
from settings import *
#from paho.mqtt import client

from sprites.Player import Player
from sprites.Bullet import Bullet
from sprites.BitString import BitString
from sprites.Stack import Stack
from sprites.StartScreen import StartScreen
from sprites.EndGameScreen import EndGameScreen
from sprites.Column import Column
from sprites.Sweep import Sweep
import json

"""
Networking Client for the MQTT communications 
with the client and the server
"""

class BattleBits:
    def __init__(self):
        self.running = True
        pg.mixer.init() #init sound system
        
        pg.init()
        pg.font.init()  #init font system

        random.seed(datetime.now())
        
        pg.display.set_caption("BattleBits2")
        self.icon = pg.image.load("./res/bb_logo.png")
        pg.display.set_icon(self.icon)

        pg.mixer.music.load('./res/battlebitsdemo.ogg')
        pg.mixer.music.play()

        pg.mouse.set_visible(False)

        self.screen = pg.display.set_mode(size)
        self.clock = pg.time.Clock()    
        self.running = True

        self.diffculty = 1

        self.stackDeath = pg.mixer.Sound("res/stack_hit2.wav")

        self.winner = 0

        # self.bnet = BattleBitsNet(str (random.randint(0,9999)))
        # self.bnet.subscribe("battlebits/move")
        # self.bnet.subscribe("battlebits/color")
        # self.bnet.subscribe("battlebits/set_position")
        # self.bnet.on_message = self.process_message

    def process_message(self, client, userdata, msg):
        print("BBNET: MSG " + str(msg.payload))
        self.player.reset_position(10,10)
        
    def init(self):
        pg.joystick.init()
        self.joysick_number = pg.joystick.get_count()

        if self.joysick_number > 0:
            for x in range(pg.joystick.get_count()):
                pg.joystick.Joystick(x).init()

            # Load up joystickMapping
            with open(JOYSTICK_FILE, 'r') as f:
                try:
                    self.joystickButtons = {int(x):y for x,y in json.load(f).items()}
                except ValueError as e:
                    self.joystickButtons = {}

        self.joystickMode = self.joysick_number > 0

    def new(self):
        #code that resets the game - start a new game
        self.all_sprites = pg.sprite.Group()
        self.columns = pg.sprite.Group()
        self.sweeps = pg.sprite.Group()

        for i in range(0,TARGETS):
            self.columns.add(Column(i))

        self.manager = BattleManager(self.all_sprites, self.diffculty)

        self.powerup_time = random.randint(PU_TIME_MIN, PU_TIME_MAX)

        '''This should be more of a wait for the player join button to be pressed... then send msg to mqtt
        then wait for player accepted msg to start game etc.'''

        #Create players
        self.player1 = Player(PLAYER_1)
        self.bitString1 = BitString(PLAYER_1)

        self.player2 = Player(PLAYER_2)
        self.bitString2 = BitString(PLAYER_2)

        self.evaluatePlayerPosition(self.player1, self.bitString1)
        self.submitPlayerPosition(self.player1, self.bitString1)

        self.evaluatePlayerPosition(self.player2, self.bitString2)
        self.evaluatePlayerPosition(self.player2, self.bitString2)

        self.stacks = [Stack(PLAYER_1, l) for l in range(0,STACK_LEVELS)]
        self.stacks.reverse()
        self.stacks += [Stack(PLAYER_2, l) for l in range(0,STACK_LEVELS)]

        self.p1Stacks = STACK_LEVELS
        self.p2Stacks = STACK_LEVELS

        #Add player sprites to spite groups
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player1.powerUps)
        self.all_sprites.add(self.player1.statusEffects)
        self.all_sprites.add(self.bitString1)

        self.all_sprites.add(self.player2)
        self.all_sprites.add(self.player2.powerUps)
        self.all_sprites.add(self.player2.statusEffects)
        self.all_sprites.add(self.bitString2)

        self.all_sprites.add(self.stacks)
            
        self.run() #start the round / game etc.

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        self.sweeps.update()

        for mobByte in self.manager.bytes:
            if mobByte.rect.top <= PLAYER_1_BOARDER:
                self.winner = PLAYER_2
                self.playing = False
            elif mobByte.rect.bottom >= PLAYER_2_BOARDER:
                self.winner = PLAYER_1
                self.playing = False

            if mobByte.movingDirection == PLAYER_1_DIRECTION and self.bitString1.byte == None:
                self.evaluatePlayerPosition(self.player1, self.bitString1)
            elif mobByte.movingDirection == PLAYER_2_DIRECTION and self.bitString2.byte == None:
                self.evaluatePlayerPosition(self.player2, self.bitString2)

            for stack in self.stacks:
                if mobByte.rect.colliderect(stack.rect):
                    index = self.manager.bytes.index(mobByte)
                    self.all_sprites.remove([stack, mobByte])
                    self.stacks.remove(stack)
                    self.stackDeath.play()
                    self.manager.bytes.remove(mobByte)
                    self.manager.generateNew(index, mobByte.direction*-1)

                    if mobByte.direction == PLAYER_2_DIRECTION:
                        self.p2Stacks -= 1

                        if index == self.player1.position:
                            self.evaluatePlayerPosition(self.player1, self.bitString1)
                    else:
                        self.p1Stacks -= 1
                        if index == self.player2.position:
                            self.evaluatePlayerPosition(self.player2, self.bitString2)
                    break

        if self.powerup_time <= pg.time.get_ticks()/1000:
            mobByte = self.manager.bytes[random.randint(0, TARGETS-1)]

            mobByte.powerUp = True
            self.powerup_time = pg.time.get_ticks()/1000 + random.randint(PU_TIME_MIN, PU_TIME_MAX)

    def swapEndian(self, byte):
        swap = 0x00
        for i in range(0, 8):
            swap += ((byte >> i) & 1) << (7 - i)
        return swap

    def evaluatePlayerPosition(self, player, bitString):
        currentByte = self.manager.bytes[player.position]
        targetValue = currentByte.byte_value
        position = 7

        nibble = 0xF0
        byte = 0x00

        if player.statusEffects.swapEndian:
            targetValue = self.swapEndian(targetValue)
            position = 0
            nibble = 0x0F

        if player.statusEffects.invertBits:
            byte = 0xFF

        if player.statusEffects.nibble:
            byte = targetValue & nibble
            if player.statusEffects.invertBits:
                byte |= (~nibble) & 0xFF
            position = abs(position - 4)


        if currentByte.direction == player.direction:
            bitString.setTarget(targetValue, byte, position)
        else:
            bitString.nullify()

    def submitPlayerPosition(self, player, bitString):
        currentByte = self.manager.bytes[player.position]
        if currentByte.direction == player.direction and currentByte.movingDirection == player.direction:
            byte = bitString.byte

            if player.statusEffects.swapEndian:
                byte = self.swapEndian(byte)

            if self.manager.submit(byte, player):
                player.checkState()
                bitString.nullify()

    def useOffensivePowerUp(self, player):
         self.sweeps.add(Sweep(player.player))

    def handle_player_actions(self, player, opposition, bitString, input):
        currentByte = self.manager.bytes[player.position]

        if input == LEFT or input == RIGHT: #Move left or right
            if not player.update_player_position(PLAYER_MOVE_LEFT if input == LEFT else PLAYER_MOVE_RIGHT):
                return
            player.checkState()
            self.evaluatePlayerPosition(player, bitString)
        elif input == B_1 and player.powerUps.hasNibblePU : #Nibble Power Up
            player.startNibblePU()
        elif input == B_2 and player.powerUps.hasSwapEndianPU and not player.powerUps.lockout: #Swap Endianness Power Up
            player.powerUps.hasSwapEndianPU = False
            player.powerUps.updateImage = True
            opposition.startSwapEndian()
            player.powerUps.startLockOut()
            self.useOffensivePowerUp(player)
        elif input == B_3 and player.powerUps.hasInvertBitsPU and not player.powerUps.lockout: #Invert Bits Power Up
            player.powerUps.hasInvertBitsPU = False
            player.powerUps.updateImage = True
            opposition.startInvertBits()
            player.powerUps.startLockOut()
            self.useOffensivePowerUp(player)

        elif currentByte.direction == player.direction:
            if input == B_5:  #Move bit string left
                bitString.move_left()
            elif input == B_6: #Toggle bit
                bitString.toggle()
                bitString.move_left() if player.statusEffects.swapEndian else bitString.move_right()
            elif input == B_4: #Move bit string right
                bitString.move_right()
            elif input == UP and player.powerUps.hasSwitch: #Switch the direction
                currentByte.direction *= -1
                self.all_sprites.add(Bullet(player.position, currentByte.movingDirection * -1, currentByte, player, False))
                player.useSwitch()
            elif input == DOWN and player.powerUps.hasSlow and currentByte.speed > 1: #Slow down the target
                self.all_sprites.add(Bullet(player.position, currentByte.movingDirection * -1, currentByte, player, True))
                player.useSlow()

        self.submitPlayerPosition(player, bitString)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

            elif self.joystickMode and (event.type == pg.JOYBUTTONDOWN or event.type == pg.JOYAXISMOTION):
                #"""These are high level events for the joystick"""

                if event.joy == 1:
                    player = self.player1
                    bitString = self.bitString1
                    opposition = self.player2
                else:
                    player = self.player2
                    bitString = self.bitString2
                    opposition = self.player1

                if event.type == pg.JOYAXISMOTION:
                    event.value = int(event.value)
                    if event.axis == JOY_X_AXIS:
                        if event.value == -1:
                            self.handle_player_actions(player, opposition, bitString, LEFT)
                        elif event.value == 1:
                            self.handle_player_actions(player, opposition, bitString, RIGHT)
                    else:
                        if event.value == -1:
                            self.handle_player_actions(player, opposition, bitString, UP)
                        elif event.value == 1:
                            self.handle_player_actions(player, opposition, bitString, DOWN)

                elif event.type == pg.JOYBUTTONDOWN:
                    if event.button in self.joystickButtons:
                        self.handle_player_actions(player, opposition, bitString, self.joystickButtons[event.button])

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.handle_player_actions(self.player1, self.player2, self.bitString1, LEFT)
                elif event.key == pg.K_RIGHT:
                    self.handle_player_actions(self.player1, self.player2, self.bitString1, RIGHT)
                elif event.key == pg.K_RCTRL:
                    self.handle_player_actions(self.player1, self.player2, self.bitString1, B_5)
                elif event.key == pg.K_RSHIFT:
                    self.handle_player_actions(self.player1, self.player2, self.bitString1, B_3)
                elif event.key == pg.K_UP:
                    self.handle_player_actions(self.player1, self.player2, self.bitString1, B_6)
                elif event.key == pg.K_DOWN:
                    self.handle_player_actions(self.player1, self.player2, self.bitString1, B_4)
                elif event.key == pg.K_a:
                    self.handle_player_actions(self.player2, self.player1, self.bitString2, LEFT)
                elif event.key == pg.K_d:
                    self.handle_player_actions(self.player2, self.player1, self.bitString2, RIGHT)
                elif event.key == pg.K_w:
                    self.handle_player_actions(self.player2, self.player1, self.bitString2, B_6)
                elif event.key == pg.K_LSHIFT:
                    self.handle_player_actions(self.player2, self.player1, self.bitString2, B_3)

    def draw(self):
        self.screen.fill(BLACK)
        self.columns.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.sweeps.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        self.diffculty = 2**(StartScreen(self).difficulty-1)
    
    def show_gameover_screen(self):
        EndGameScreen(bb).display()

if __name__ == "__main__":
    bb = BattleBits()
    while bb.running:
        bb.init()
        bb.show_start_screen()
        bb.new()
        bb.show_gameover_screen()

    pg.quit()