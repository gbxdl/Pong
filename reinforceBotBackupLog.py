import pickle
import random
import math
import time

from player import *

class reinforceBot(player):
    def __init__(self, gameState, whichPlayer, loadTable, progress, greedy = False):
        super().__init__(gameState, whichPlayer, loadTable, progress)
        self.probRandom = 0.1
        if greedy:
            self.probRandom = 0
        self.learingRate = 0.1
        self.verDiscreteBat = int(self.gs.boardHeight / self.gs.batStepSize)
        self.maxVerDiscreteBall = 0
        for i in range(100):
            if i == 0:
                twoPowi = 1
            else:
                twoPowi *= 2
            if twoPowi >= self.gs.boardHeight / self.gs.batStepSize and self.maxVerDiscreteBall == 0:    
                self.maxVerDiscreteBall = twoPowi
            if twoPowi >= self.gs.boardWidth / self.gs.batStepSize:
                self.horDiscreteBall = i
                break
        self.horDiscreteVelocity = 1
        self.verDiscreteVelocity = 3
        if whichPlayer == 'left':
            self.fname = 'trainedTableLeft' + '.txt'
        else:
            self.fname = 'trainedTableRight' + '.txt'
        # print(self.verDiscreteBat,self.verDiscreteBall,self.horDiscreteBall)
        if loadTable:
            self.loadTable()
        else:      
            self.initTable()
        self.speedCounterLow = 0
        self.speedCounterMiddle = 0
        self.speedCounterHigh = 0
        
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
        [newBallPos,newBallVelocity] = self.progress.moveBall(self.gs.ballPos,self.gs.ballVelocity)
        newBallPosDiscrete = self.discretizeBallPos(newBallPos) #happens with the old bat position, if new pull inside loop and give batPos
        newBallVelocityDiscrete = self.discretizeBallVelocity(newBallVelocity)
        for move in [0,-1,1]:
            if self.whichPlayer == 'left':
                newBatHeight = self.progress.moveBatLeft(move) 
            else:
                newBatHeight = self.progress.moveBatRight(move)
            newBatHeightDiscrete = self.discretizeBatPos(newBatHeight)
            # print(newBallPosDiscrete)
            itemName = str([newBatHeightDiscrete,newBallPosDiscrete,newBallVelocityDiscrete])
            # print(itemName)
            if self.table[itemName] > highestProb:
                highestProb = self.table[itemName]
                bestMove = move
                newItemName = itemName
        oldItemName = str([oldBatHeightDiscrete,ballPosDiscrete,ballVelocityDescrete])
        self.updateTable(oldItemName,newItemName)
        return bestMove

    def discretizeBatPos(self,batHeight):
        return int(self.verDiscreteBat * batHeight / self.gs.boardHeight)
        
    def discretizeBallVelocity(self,velocity):
        newvelocityx = int(math.copysign(1,velocity[1]))
        if abs(velocity[0]) < self.gs.initSpeed:
            newvelocityy = int(math.copysign(1,velocity[0]))
            self.speedCounterLow += 1
        elif abs(velocity[0]) < 2*self.gs.initSpeed:
            newvelocityy = int(math.copysign(2,velocity[0]))
            self.speedCounterMiddle += 1
        else:
            newvelocityy = int(math.copysign(3,velocity[0]))
            self.speedCounterHigh += 1
        return [newvelocityy,newvelocityx]
        
    def discretizeBallPos(self,ballPos):
        posxDiscreteSmall = ballPos[1] / self.maxVerDiscreteBall
        if ballPos[1] < 0:
            return [0,0]
        elif ballPos[1] > self.gs.boardWidth:
            return [0,self.horDiscreteBall + 1]
        else:
            posx = math.ceil(math.log(posxDiscreteSmall,2))
            if posx < 1:
                posx = 1
        precisiony = self.maxVerDiscreteBall / 2**(posx-1)
        posy = int(ballPos[0] / (self.gs.boardWidth / precisiony))
        return [posy,posx]
        
    def updateTable(self,oldItemName,newItemName):
        oldProb = self.table[oldItemName]
        newProb = self.table[newItemName]
        self.table[oldItemName] = oldProb + self.learingRate * (newProb - oldProb)

    def initTable(self):#Can be done much faster by only looking at 
        tic = time.time()
        self.table = {}
        for posBallx in range(self.horDiscreteBall + 2):#to include the won and lost positions: posBallx=0,verDiscrete+1 are gameover.
            if posBallx <= 1:
                twoPowPosBallx = 1
            else:
                twoPowPosBallx *= 2
            outcome = self.checkGameover(posBallx)
            if outcome == 'win':
                prob = 1
            elif outcome == 'lose':
                prob = 0
            else:
                prob = 0.5
            if posBallx == 0 or posBallx == self.horDiscreteBall + 1:
                precisionyDependingOnx = 1
            else:
                if self.whichPlayer == 'left':
                    precisionyDependingOnx = int(self.maxVerDiscreteBall / twoPowPosBallx)
                else:
                    precisionyDependingOnx = int(twoPowPosBallx)
            # print(posBallx, precisionyDependingOnx)
            for posBally in range(precisionyDependingOnx):
                for posBaty in range(self.verDiscreteBat+1):#half out of bound each side.
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
            
    def checkGameover(self, posBallx):
        if posBallx == 0:
            if self.whichPlayer == 'left':
                return 'lose'
            if self.whichPlayer == 'right':
                return 'win'
        if posBallx == self.horDiscreteBall + 1:
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

        