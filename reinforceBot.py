import pickle
import random
import math

from player import *

class reinforceBot(player):
    def __init__(self, gameState, whichPlayer, loadTable, progress):
        super().__init__(gameState, whichPlayer)
        self.progress = progress
        self.probRandom = 0.1
        self.learingRate = 0.1
        self.precision = int(self.gs.batLength)
        self.verDiscreteBat = int(self.gs.boardHeight / self.gs.batStepSize)
        self.verDiscreteBall = int(self.gs.boardHeight/self.precision)
        self.horDiscreteBall = int(self.gs.boardWidth/self.precision)
        # print(self.verDiscreteBat,self.verDiscreteBall,self.horDiscreteBall)
        if loadTable:
            self.loadTable()
        else:      
            self.initTable()
        
        
    def makeMove(self):
        if random.random() < self.probRandom:
            return 1-math.floor(3*random.random())
        
        ballPosDiscrete = self.discretizeBallPos(self.gs.ballPos)
        highestProb = -1
        bestMove = 0
        if self.whichPlayer == 'left':
            oldBatHeight = self.gs.batLeftPos[0]
        else: 
            oldBatHeight = self.gs.batRightPos[0]
        oldBatHeightDiscrete = self.discretizeBatPos(oldBatHeight)
        for move in [0,-1,1]:
            newBatHeight = self.gs.batStepSize * move + oldBatHeight
            [newBallPos,speed] = self.progress.moveBall(self.gs.ballPos,self.gs.ballVelocity)
            newBatHeightDiscrete = self.discretizeBatPos(newBatHeight)
            newBallPosDiscrete = self.discretizeBallPos(newBallPos)
            # print(newBallPosDiscrete)
            itemName = str([newBatHeightDiscrete,newBallPosDiscrete[0],newBallPosDiscrete[1]])
            # print(self.table[itemName])
            if self.table[itemName] > highestProb:
                highestProb = self.table[itemName]
                print(highestProb)
                bestMove = move
                newItemName = itemName
        oldItemName = str([oldBatHeightDiscrete,ballPosDiscrete[0],ballPosDiscrete[1]])
        self.updateTable(oldItemName,newItemName)
        return bestMove

    def discretizeBatPos(self,batHeight):
        return math.floor(batHeight * self.verDiscreteBat / self.gs.boardHeight)
        
    def discretizeBallPos(self,ballPos):
        posy = math.floor(ballPos[0] * self.verDiscreteBall / self.gs.boardHeight)
        posx = math.floor(ballPos[1] * self.horDiscreteBall / self.gs.boardWidth)
        if posx < 0:
            posx = 0
        if posx > self.horDiscreteBall + 1:
            posx = self.horDiscreteBall + 1
        # print(ballPos[1],posx)
        return [posy,posx]
        
        
    def updateTable(self,oldItemName,newItemName):
        oldProb = self.table[oldItemName]
        newProb = self.table[newItemName]
        # print(oldProb, newProb)
        self.table[oldItemName] = oldProb + self.learingRate * (newProb - oldProb)
        # print(self.table[oldItemName])

        
    def initTable(self):#start with just pos ball and pos bat y, more info later
        self.table = {}
        for posBaty in range(self.verDiscreteBat):
            for posBally in range(self.verDiscreteBall):
                for posBallx in range(self.horDiscreteBall + 2): #to include the won and lost positions: posBallx=0,verDiscrete+1 are gameover.
                    outcome = self.checkGameover(posBallx, self.verDiscreteBall)
                    itemName = str([posBaty,posBally,posBallx])
                    if outcome == 'win':
                        self.table[itemName] = 1
                    elif outcome == 'lose':
                        self.table[itemName] = 0
                    else:
                        self.table[itemName] = 0.5
            
    def checkGameover(self, posBallx, verDiscreteBall):
        if posBallx == 0:
            if self.whichPlayer == 'left':
                return 'lose'
            if self.whichPlayer == 'right':
                return 'win'
        if posBallx == verDiscreteBall + 1:
            if self.whichPlayer == 'left':
                return 'win'
            if self.whichPlayer == 'right':
                return 'lose'
        return 0
        
    def loadTable(self):
        if self.whichPlayer == 'left':
            fname='reinforcementTable_left.txt'
        elif self.whichPlayer == 'right':
            fname='reinforcementTable_right.txt'
        with open(fname, 'rb') as f:
            self.table = pickle.load(f)
        
    def saveTable(self):
        if self.whichPlayer == 'left':
            fname='reinforcementTable_left.txt'
        elif self.whichPlayer == 'right':
            fname='reinforcementTable_right.txt'
        with open(fname, 'wb') as f:
            pickle.dump(self.table,f)

        