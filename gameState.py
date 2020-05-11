#This will hold the position of the ball and bats, and the speed as the speed will increase over time, but maybe only for human play
import random

from GUI import *

class gameState:
    def __init__(self, play = False, showGame = False):
        self.play = play
        self.showGame = showGame
        self.guiOn = False
        
        if self.play or self.showGame:
            self.guiOn = True
        
        self.boardWidth = 1200
        self.boardHeight = 600
        self.ballRadius = self.boardWidth/240
        self.batThickness = self.boardWidth/60
        self.batLength = self.boardHeight/6
        self.batLeftPos = [self.boardHeight/2,self.batThickness/2]
        self.batRightPos = [self.boardHeight/2,self.boardWidth-self.batThickness/2]
        self.batStepSize = self.batLength/10
        self.startGame()
        if self.guiOn:
            window = Tk()
            self.gui = GUI(window, self)
            
    def startGame(self):
        self.ballPos = [self.boardHeight/2,self.boardWidth/2]
        self.timeStep = 0
        speedy = 10*(1-2*random.random())
        randomsign = 0
        if random.random()>.5:
            randomsign = 1
        speedx = (-1)**randomsign * 3
        self.gameover = False
        self.ballVelocity = [speedy,speedx]
        #later player speed etc.
    
    
    
