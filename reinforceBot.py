import pickle
import random
import math
import time

from player import *

class reinforceBot(player):
    def __init__(self, gameState, whichPlayer, loadTable, progress):
        super().__init__(gameState, whichPlayer, loadTable, progress)
        self.probRandom = 0.1
        self.learingRate = 0.1
        horPrecision = int(2*self.gs.batLength)
        verPrecision = int(self.gs.batLength/8)
        self.verDiscreteBat = int(self.gs.boardHeight / self.gs.batStepSize) + 2#half out of bound each side.
        self.verDiscreteBall = int(self.gs.boardHeight / verPrecision)
        self.horDiscreteBall = int(self.gs.boardWidth / horPrecision)
        self.horDiscreteVelocity = 1
        self.verDiscreteVelocity = 1
        if whichPlayer == 'left':
            self.fname = 'trainedTableLeft' + '.txt'
        else:
            self.fname = 'trainedTableRight' + '.txt'
        # print(self.verDiscreteBat,self.verDiscreteBall,self.horDiscreteBall)
        if loadTable:
            self.loadTable()
        else:      
            self.initTable()
        
    def makeMove(self):
        if random.random() < self.probRandom:
            return 1-int(3*random.random())
        
        ballPosDiscrete = self.discretizeBallPos(self.gs.ballPos)
        ballVelocityDescrete = self.discretizeBallVelocity(self.gs.ballVelocity)
        highestProb = -1
        bestMove = 0
        if self.whichPlayer == 'left':
            oldBatHeight = self.gs.batLeftPos[0]
        else: 
            oldBatHeight = self.gs.batRightPos[0]
        oldBatHeightDiscrete = self.discretizeBatPos(oldBatHeight)
        for move in [0,-1,1]:
            if self.whichPlayer == 'left':
                newBatHeight = self.progress.moveBatLeft(move) 
            else:
                newBatHeight = self.progress.moveBatRight(move)
            [newBallPos,newBallVelocity] = self.progress.moveBall(self.gs.ballPos,self.gs.ballVelocity)
            newBatHeightDiscrete = self.discretizeBatPos(newBatHeight)
            newBallPosDiscrete = self.discretizeBallPos(newBallPos)
            newBallVelocityDiscrete = self.discretizeBallVelocity(newBallVelocity)
            # print(newBallPosDiscrete)
            itemName = str([newBatHeightDiscrete,newBallPosDiscrete,newBallVelocityDiscrete])
            if self.table[itemName] > highestProb:
                highestProb = self.table[itemName]
                # print(highestProb)
                bestMove = move
                newItemName = itemName
        oldItemName = str([oldBatHeightDiscrete,ballPosDiscrete,ballVelocityDescrete])
        self.updateTable(oldItemName,newItemName)
        return bestMove

    def discretizeBatPos(self,batHeight):
        return int(batHeight * self.verDiscreteBat / self.gs.boardHeight)
        
    def discretizeBallVelocity(self,velocity):
        newvelocityx = int(math.copysign(1,velocity[1]))
        # if abs(velocity[0]) < self.gs.batLength:
        newvelocityy = int(math.copysign(1,velocity[0]))
        # else:
        #     newvelocityy = int(math.copysign(2,velocity[0]))
        return [newvelocityy,newvelocityx]
        
    def discretizeBallPos(self,ballPos):
        posy = math.floor(ballPos[0] * self.verDiscreteBall / self.gs.boardHeight)
        posx = math.floor(ballPos[1] * self.horDiscreteBall / self.gs.boardWidth)
        if posx < -1:
            posx = -1
        if posx > self.horDiscreteBall + 1:
            posx = self.horDiscreteBall + 1
        return [posy,posx+1]
        
        
    def updateTable(self,oldItemName,newItemName):
        oldProb = self.table[oldItemName]
        newProb = self.table[newItemName]
        self.table[oldItemName] = oldProb + self.learingRate * (newProb - oldProb)
        
    def initTable(self):#Can be done much faster by only looking at 
        tic = time.time()
        self.table = {}
        for posBallx in range(self.horDiscreteBall + 2):#to include the won and lost positions: posBallx=0,verDiscrete+1 are gameover.
            outcome = self.checkGameover(posBallx, self.verDiscreteBall)
            if outcome == 'win':
                prob = 1
            elif outcome == 'lose':
                prob = 0
            else:
                prob = 0.5
            for posBaty in range(self.verDiscreteBat):
                for posBally in range(self.verDiscreteBall):
                    for velocityx in range(-self.horDiscreteVelocity, self.horDiscreteVelocity+1):
                        if velocityx == 0:
                            continue
                        for velocityy in range(-self.verDiscreteVelocity,self.verDiscreteVelocity+1):
                            if velocityy == 0:
                                continue
                            itemName = str([posBaty,[posBally,posBallx],[velocityy,velocityx]])
                            self.table[itemName] = prob
        toc = time.time()
        self.saveTable()
        print('table init took:', toc-tic, 'seconds')
            
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
        with open(self.fname, 'rb') as f:
            self.table = pickle.load(f)
        
    def saveTable(self):
        with open(self.fname, 'wb') as f:
            pickle.dump(self.table,f,protocol=pickle.HIGHEST_PROTOCOL)

        