import pickle
import random
import math

from player import *

class reinforceBot(player):
    def __init__(self, gameState, whichPlayer, loadTable):
        super().__init__(gameState, whichPlayer)
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
        
        [posBallxDiscrete, posBallyDiscrete] = self.discretizeBallPos(self.gs.ballPos)
        highestProb = 0
        if self.whichPlayer == 'left':
            oldBatHeight = self.gs.batLeftPos[0]
        else: 
            oldBatHeight = self.gs.batRightPos[0]
        oldBatHeightDiscrete = self.discritizeBatPos(oldBatHeight)
        for move in [-1,0,1]:
            newBatHeight = self.gs.batStepSize * move + oldBatHeight
            newBatHeightDiscrete = self.discritizeBatPos(newBatHeight)
            itemName = str([newBatHeightDiscrete,posBallyDiscrete,posBallxDiscrete])
            print(self.table[itemName])
        return 0

    def discritizeBatPos(self,batHeight):
        return math.floor(batHeight * self.verDiscreteBat / self.gs.boardHeight)
        
    def discretizeBallPos(self,ballPos):
        posy = math.floor(ballPos[0] * self.verDiscreteBall / self.gs.boardHeight)
        posx = math.floor(ballPos[1] * self.horDiscreteBall / self.gs.boardWidth)
        return [posx,posy]
        
        
    def updateTable(self,prevState,State): #to do, first see what make move does
        position[lastMove]=0
        oldPosString = self.convertPositionToString(position)
        position[lastMove]=3-self.myColor
        position[bestMove[0]][bestMove[1]] = self.myColor
        newPosString = self.convertPositionToString(position)
        
        for i,tab in enumerate(self.table):
            if tab[0] == oldPosString:
                indexOld = i
            if tab[0] == newPosString:
                indexNew = i
        oldProb = self.table[indexOld][1]
        newProb = self.table[indexNew][1]
        self.table[indexOld][1] = oldProb + self.alpha * (newProb - oldProb) 

        
    def initTable(self):#start with just pos ball and pos bat y, more info later
        self.table = {}
        for posBaty in range(self.verDiscreteBat):
            for posBally in range(self.verDiscreteBall):
                for posBallx in range(self.verDiscreteBall + 2): #to include the won and lost positions: posBallx=0,verDiscrete+1 are gameover.
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

        