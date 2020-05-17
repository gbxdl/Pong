class progress:
    def __init__(self,gameState):
        self.gs = gameState
        self.leftCounter = 0
        self.rightCounter = 0
        
    def timeStep(self,leftPlayer, rightPlayer):
        if self.gs.guiOn:
            self.gs.gui.boundKeys(leftPlayer,rightPlayer)
        
        if leftPlayer.isHuman == False:
            direction = leftPlayer.makeMove()
            self.gs.batLeftPos[0] = self.gs.moveBatLeft(direction)
        if rightPlayer.isHuman == False:
            direction = rightPlayer.makeMove()
            self.gs.batRightPos[0] = self.gs.moveBatRight(direction)
        
        [self.gs.ballPos,self.gs.ballVelocity] = self.gs.moveBall(self.gs.ballPos,self.gs.ballVelocity)
        
        if self.gs.ballPos[1] < 0:
            self.gs.gameover = 1
            self.rightCounter += 1
        elif self.gs.ballPos[1] > self.gs.boardWidth:
            self.gs.gameover = 2
            self.leftCounter += 1
        
        if self.gs.ballVelocity[1] > 0:
            self.gs.ballVelocity[1] = self.gs.ballVelocity[1]+0.01
        else:
            self.gs.ballVelocity[1] = self.gs.ballVelocity[1]-0.01  
    
        
        
        
        
        