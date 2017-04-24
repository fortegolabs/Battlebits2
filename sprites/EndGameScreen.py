from settings import *
import pygame as pg
import sys, json
from random import randint
from sprites.PlayerName import PlayerName
from datetime import datetime

class EndGameScreen(object):
    def __init__(self, bbui):
        self.screen = bbui.screen
        self.clock = bbui.clock

        self.winner = bbui.winner
        self.p1Score = bbui.manager.p1Score.score + bbui.p1Stacks * STACK_POINTS
        self.p2Score = bbui.manager.p2Score.score + bbui.p2Stacks * STACK_POINTS

        self.screen.fill(GREY)

        self.load_scores()

        self.addPlayer = None

        self.target = None

        self.newScore(self.p1Score if self.winner == 1 else self.p2Score)

    def newScore(self, score):
        for i in range(0, len(self.scores)):
            if score > self.scores[i]:
                self.target = i
                break

        if self.target != None:
            self.addPlayer = PlayerName()

    def load_scores(self):
        with open(SCORE_FILE, 'r') as f:
            try:
                self.scores, self.players, self.times = json.load(f)
            except ValueError as e:
                self.scores = []
                self.players = []
                self.times = []

    def save_scores(self):
        with open(SCORE_FILE, 'w') as f:
            json.dump((self.scores, self.players, self.times), f)

    def update(self):
        self.screen.fill(GREY)

        winner = (randint(0x00, 0xFF), randint(0x00, 0xFF), randint(0x00, 0xFF))

        self.draw_text("Player %d Wins" % self.winner, 40, PLAYER_1_COLOR if self.winner == PLAYER_1 else PLAYER_2_COLOR, WIDTH/2, HEIGHT/7)
        self.draw_text("Player 1: %d" % self.p1Score, 25, winner if self.winner == 1 else BLACK, (WIDTH / 3), (HEIGHT / 4))
        self.draw_text("Player 2: %d" % self.p2Score, 25, winner if self.winner == 2 else BLACK, WIDTH - (WIDTH / 3), (HEIGHT / 4))
        self.draw_text("Top Scores", 35, WHITE, WIDTH / 2, HEIGHT / 6 * 2)

        for i in range(0,len(self.players)):
            color = WHITE
            if self.addPlayer == None and self.target == i:
                color = (randint(0x00, 0xFF), randint(0x00, 0xFF), randint(0x00, 0xFF))
            self.draw_text("%s  - %4d" % (self.players[i], self.scores[i]), 30, color, WIDTH / 2, HEIGHT/5*2+20+40*i)

        if self.addPlayer is not None:
            self.addPlayer.draw(self.screen)

        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font("res/PressStart2P.ttf", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)

        self.screen.blit(text_surface, text_rect)

    def display(self):

        waiting = True
        while waiting:
            self.update()

            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print("QUITTING")
                    sys.exit()
                elif event.type == pg.JOYBUTTONDOWN:
                    if self.addPlayer != None:
                        if event.button == JOY_START_BUTTON:
                            self.scores.insert(self.target, self.p1Score if self.winner == 1 else self.p2Score)
                            self.players.insert(self.target, self.addPlayer.get_name())
                            self.times.insert(self.target, str(datetime.now()))

                            del self.scores[-1]
                            del self.players[-1]
                            del self.times[-1]

                            self.addPlayer = None
                    else:
                        waiting = False
                elif event.type == pg.JOYAXISMOTION and self.addPlayer != None and (self.winner == PLAYER_2) != (event.joy == 1):
                    if event.type == pg.JOYAXISMOTION:
                        event.value = int(event.value)
                        if event.axis == JOY_X_AXIS:
                            if event.value == -1:
                                self.addPlayer.moveLeft()
                            elif event.value == 1:
                                self.addPlayer.moveRight()
                        else:
                            if event.value == -1:
                                self.addPlayer.increment()
                            elif event.value == 1:
                                self.addPlayer.decrement()

        self.save_scores()