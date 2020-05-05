#This will hold the position of the ball and bats, and the speed as the speed will increase over time, but maybe only for human play
import random

class gameState:
    def __init__(self):
        self.boardWidth = 1200
        self.boardHeight = 600
        self.ballRadius = self.boardWidth/60
        self.ballPos = [self.baordHeight/2,self.boadWidth/2]
        self.batThickness = self.boardWidth/60
        self.batLength = self.boardHeight/6
        self.batLeftPos = [self.boardHeight/2,self.batThickness/2]
        self.batRightPos = [self.boardHeight/2,self.boardWidth-self.batThickness/2]
        self.timeStep = 0
        speedx = 1-2*random.random()
        randomsign = 0
        if random.random()>.5:
            randomsign = 1
        self.ballVelocity = [(-1)**round(randomsign*(1-speedx**2)),round(100*speedx)]
            
            
        #later player speed etc.
    
    
    
