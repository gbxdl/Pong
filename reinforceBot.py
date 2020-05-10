from player import *

class reinforceBot(player):
    def __init__(self, gameState, whichPlayer, loadTable):
        super().__init__(gameState, whichPlayer)
        self.probRandom = 0.1
        self.learingRate = 0.1
        if loadTable:
            self.loadTable()
        else:      
            self.initTable()

        
    def checkGameover(self, posBallx, verDiscrete):
        if posBallx == 0:
            if self.whichPlayer == 'left':
                return 'lose'
            if self.whichPlayer == 'right':
                return 'win'
        if posBallx == verDiscrete + 1:
            if self.whichPlayer == 'left':
                return 'win'
            if self.whichPlayer == 'right':
                return 'lose'
        
        
    def initTable(self):#start with just pos ball and pos bat y, more info later
        self.table = {}
        precision = int(self.gs.batLength)
        verDiscrete = int(self.gs.boardHeight/precision)
        horDiscrete = int(self.gs.boardWidth/precision)
        for posBaty in range(verDiscrete):
            for posBally in range(verDiscrete):
                for posBallx in range(verDiscrete + 2): #to include the won and lost positions: posBallx=0,verDiscrete+1 are gameover.
                    outcome = self.checkGameover(postBallx, verDiscrete)
                    itemName = str([posBaty,posBally,posBallx])
                    if outcome == 'win':
                        table[itemName] = 1
                    elif outcome == 'lose':
                        table[itemName] = 0
                    else:
                        table[itemName] = 0.5
        
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

        