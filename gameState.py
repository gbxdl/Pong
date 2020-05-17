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
        self.batStepSize = self.batLength/10#power of two
        self.initSpeed = self.boardHeight/60
        self.batLeftPos = [self.boardHeight/2, self.batThickness/2]
        self.batRightPos = [self.boardHeight/2, self.boardWidth-self.batThickness/2]

        self.startGame()
        
        if self.guiOn:
            window = Tk()
            self.gui = GUI(window, self)
            
    def startGame(self):
        self.ballPos = [self.boardHeight/2,self.boardWidth/2]
        self.timeStep = 0
        speedy = self.initSpeed*(1-2*random.random())
        randomsign = 0
        if random.random()>.5:
            randomsign = 1
        speedx = (-1)**randomsign * 3
        self.gameover = False
        self.ballVelocity = [speedy,speedx]
        #later player speed etc.
    
    def moveBatLeft(self,direction):
        newPos = self.batStepSize * direction + self.batLeftPos[0]
        if 0 <= newPos <= self.boardHeight:
            return newPos
        return self.batLeftPos[0]
            
    def moveBatRight(self,direction):
        newPos = self.batStepSize * direction + self.batRightPos[0]
        if 0 <= newPos <= self.boardHeight:
            return newPos
        return self.batRightPos[0]
        
    def moveBall(self,pos,speed):
        posx = pos[1]
        posy = pos[0]
        speedx = speed[1]
        speedy = speed[0]
        newPosx = posx + speedx
        newPosy = posy + speedy
        newSpeedx = speedx
        newSpeedy = speedy
        if newPosy < 0:
            newPosy = (-1) * newPosy
            newSpeedy = (-1) * newSpeedy
        if newPosy > self.boardHeight:
            newPosy = self.boardHeight - (newPosy - self.boardHeight)
            newSpeedy = (-1) * speedy
        
        leftEdge = self.batThickness + self.ballRadius
        rightEdge = self.boardWidth - self.batThickness - self.ballRadius
        if rightEdge >= newPosx >= leftEdge:
            return [[newPosy,newPosx],[newSpeedy,newSpeedx]]
        
        lowEdge = self.batLeftPos[0] + self.batLength/2
        highEdge = self.batLeftPos[0] - self.batLength/2
        distToCenter = newPosy - self.batLeftPos[0]
        # print(newPosx,'<',leftEdge,'and', lowEdge,'>=',newPosy,'>=',highEdge)
        if newPosx < leftEdge and lowEdge >= newPosy >= highEdge:
            newPosx = leftEdge + (leftEdge - newPosx)
            newSpeedx = (-1) * newSpeedx
            newSpeedy = newSpeedy + distToCenter/self.batLength * 10 #give variable a name
            return [[newPosy,newPosx],[newSpeedy,newSpeedx]]
            
        lowEdge = self.batRightPos[0] + self.batLength/2
        highEdge = self.batRightPos[0] - self.batLength/2
        distToCenter = newPosy - self.batRightPos[0]
        
        if newPosx > rightEdge and lowEdge >= newPosy >= highEdge:
            newPosx = rightEdge + (rightEdge - newPosx)
            newSpeedx = (-1) * newSpeedx
            newSpeedy = newSpeedy + distToCenter/self.batLength *10
        return [[newPosy,newPosx],[newSpeedy,newSpeedx]]
    
