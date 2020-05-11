class progress:
    def __init__(self,gameState):
        self.gs = gameState
        self.leftCounter = 0
        self.rightCounter = 0
        
    def timeStep(self,leftPlayer, rightPlayer):
        if self.gs.guiOn:
            self.gs.gui.boundKeys(leftPlayer,rightPlayer)
        
        if leftPlayer.isHuman == False:
            self.gs.batLeftPos[0] = self.moveBatLeft(leftPlayer)
        if rightPlayer.isHuman == False:
            self.gs.batRightPos[0] = self.moveBatRight(rightPlayer)
        
        [self.gs.ballPos,self.gs.ballVelocity]= self.moveBall(self.gs.ballPos,self.gs.ballVelocity)
        
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
    
    def moveBatLeft(self,leftPlayer):
        direction = leftPlayer.makeMove()
        newPos = self.gs.batStepSize * direction + self.gs.batLeftPos[0]
        if self.gs.batLength/2 <= newPos <= self.gs.boardHeight - self.gs.batLength/2:
            return newPos
        return self.gs.batLeftPos[0]
            
    def moveBatRight(self,rightPlayer):
        direction = rightPlayer.makeMove()
        newPos = self.gs.batStepSize*direction + self.gs.batRightPos[0]
        if self.gs.batLength/2 <= newPos <= self.gs.boardHeight - self.gs.batLength/2:
            return newPos
        return self.gs.batRightPos[0]
        
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
        if newPosy > self.gs.boardHeight:
            newPosy = self.gs.boardHeight - (newPosy - self.gs.boardHeight)
            newSpeedy = (-1) * speedy
        
        leftEdge = self.gs.batThickness + self.gs.ballRadius
        rightEdge = self.gs.boardWidth - self.gs.batThickness - self.gs.ballRadius
        if rightEdge >= newPosx >= leftEdge:
            return [[newPosy,newPosx],[newSpeedy,newSpeedx]]
        
        lowEdge = self.gs.batLeftPos[0] + self.gs.batLength/2
        highEdge = self.gs.batLeftPos[0] - self.gs.batLength/2
        distToCenter = newPosy - self.gs.batLeftPos[0]
        # print(newPosx,'<',leftEdge,'and', lowEdge,'>=',newPosy,'>=',highEdge)
        if newPosx < leftEdge and lowEdge >= newPosy >= highEdge:
            newPosx = leftEdge + (leftEdge - newPosx)
            newSpeedx = (-1) * newSpeedx
            newSpeedy = newSpeedy + distToCenter/self.gs.batLength *10
            #to do: newSpeedy depends on where on the bat
        lowEdge = self.gs.batRightPos[0] + self.gs.batLength/2
        highEdge = self.gs.batRightPos[0] - self.gs.batLength/2
        distToCenter = newPosy - self.gs.batRightPos[0]
        
        if newPosx > rightEdge and lowEdge >= newPosy >= highEdge:
            newPosx = rightEdge + (rightEdge - newPosx)
            newSpeedx = (-1) * newSpeedx
            newSpeedy = newSpeedy + distToCenter/self.gs.batLength *10
        return [[newPosy,newPosx],[newSpeedy,newSpeedx]]
        
        
        
        
        