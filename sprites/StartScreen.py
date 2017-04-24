import pygame as pg
from settings import *
import os, random, sys, time


class StartScreen(object):
    def __init__(self, bbui):
        #pg.sprite.Sprite.__init__(self)
        self.screen = bbui.screen
        self.clock = bbui.clock
        self.waiting_for_additional_player = False #If a single player joins then we set this to true.
        
        #Sounds - All Created with @ http://www.bfxr.net/
        self.p1_join_sound = pg.mixer.Sound('./res/p1_join.wav')
        self.p2_join_sound = pg.mixer.Sound('./res/p2_join.wav')
        pg.display.flip()
        
        self._p1_joined = False
        self._p2_joined = False

        self.exit = False

        self.pre1_pressed_text = "[ P1 Press Start ]" 
        self.pre2_pressed_text = "[ P2 Press Start ]"
        self.joined1_text = "[ P1 JOINED W00T! ]"
        self.joined2_text = "[ P2 JOINED W00T! ]"

        self.difficulty = 1

        self.p1_text = self.pre1_pressed_text
        self.p2_text = self.pre2_pressed_text
        self.status_text = ""
        self.timer_text = ""  #Dont show this until we are ready to start timer
        
        self.timer_expired = False #This this to false initially
        self.wait_for_player_joins() #Wait until both players press start

    def update_background(self):
        self.logo = pg.image.load("./res/bb_logo.png")
        self.logo = pg.transform.scale(self.logo, (int(WIDTH/2) , int(HEIGHT/2)) )
        self.screen.fill(GREY)
        self.screen.blit(self.logo, (WIDTH/4, 55)) #(width, height)

        self.draw_text(self.p2_text, 18, BLACK, WIDTH - (WIDTH/4), HEIGHT- (HEIGHT/6))
        self.draw_text(self.p1_text, 18, BLACK, (WIDTH/4), HEIGHT- (HEIGHT/6) )
        self.draw_text(self.status_text, 24, BLACK, (WIDTH/2), HEIGHT - (HEIGHT/3) )
        self.draw_text(self.timer_text, 24, BLACK, (WIDTH/2), HEIGHT - (HEIGHT/4))
        self.draw_text("Difficulty: %d" % self.difficulty, 18, BLACK, WIDTH - 2*(WIDTH/4), HEIGHT - (HEIGHT/4) + 60)

        if self.waiting_for_additional_player == True:
            self.status_text = "Waiting for another player"

        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font("res/PressStart2P.ttf", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)        
        
        if(self._p1_joined):
            pg.transform.scale(text_surface,(50,50))
            #self.screen.blit(text_surface)
        elif(self._p2_joined):
            pg.transform.rotate(text_surface, 45)

        self.screen.blit(text_surface, text_rect) 
    
    def start_game_countdown(self):
        """Once both players have hit the start button this 
        countdown will start"""
        pg.time.set_timer(22, GAME_START_COUNTDOWN*1000) #Set a timer event to occur in 5 seconds
        self.timer_count = int(pg.time.get_ticks()/1000) 
        self.timer_zero = self.timer_count + GAME_START_COUNTDOWN
        self.timer_max = self.timer_count + GAME_START_COUNTDOWN

    def wait_for_player_joins(self):
        #This is just for waiting for the players to join the game
        self.update_background()
        waiting = True
        while waiting:
            #self.update_background()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print("QUITTING")
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RSHIFT:
                        self.waiting_for_additional_player = True  # We mark this true in both joins as it doesn not affect our loop
                        self.p1_text = self.joined1_text
                        self._p1_joined = True
                        self.p1_join_sound.play()
                    elif event.key == pg.K_LSHIFT:
                        self.waiting_for_additional_player = True  # We mark this true in both joins as it doesn not affect our loop
                        self.p2_text = self.joined2_text
                        self._p2_joined = True
                        self.p2_join_sound.play()
                    self.update_background()
                elif event.type == pg.JOYBUTTONDOWN:
                    if event.dict['button'] == JOY_START_BUTTON:
                        #This is the start button
                        if event.dict['joy'] == 1: #joystick == p1
                            self.waiting_for_additional_player = True #We mark this true in both joins as it doesn not affect our loop
                            self.p1_text = self.joined1_text
                            self._p1_joined = True
                            self.p1_join_sound.play()
                        else:
                            self.waiting_for_additional_player = True #We mark this true in both joins as it doesn not affect our loop
                            self.p2_text = self.joined2_text
                            self._p2_joined = True
                            self.p2_join_sound.play()
                    elif event.button == JOY_R_BUTTON and self.difficulty < 5:
                        self.difficulty += 1
                    elif event.button == JOY_L_BUTTON and self.difficulty > 1:
                        self.difficulty -= 1
                    elif event.button == JOY_A_BUTTON:
                        self.exit = True
                    elif event.button == JOY_SELECT_BUTTON and self.exit:
                        exit()
                elif event.type == pg.JOYBUTTONUP:
                    if event.button == JOY_A_BUTTON:
                        self.exit = False

                    self.update_background()

                #if self._p1_joined and self._p2_joined:
                if self._p1_joined and self._p2_joined:
                    waiting = False
                    self.timer_count_text = "%d:%d"
                    #Once we have both players joined we set waiting to false and kill the loop
                    
        self.start_game_countdown()  #Game is about to start
        
        while self.timer_expired == False:
            self.timer_count = int(pg.time.get_ticks()/1000) #400
            self.timer_text = str(self.timer_zero - self.timer_count)
            self.status_text = "Game Starting in..."
            self.update_background()
            for event in pg.event.get():
                if(event.type == GAME_TIMER_EXPIRED):
                    self.timer_expired = True
                elif(event.type == pg.QUIT):
                    sys.exit()

        return self.difficulty