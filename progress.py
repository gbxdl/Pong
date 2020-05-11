class progress:
    def __init__(self,gameState):
        self.gs = gameState
        self.leftCounter = 0
        self.rightCounter = 0
        
    def timeStep(self,leftPlayer, rightPlayer):
        if self.gs.guiOn:
            self.gs.gui.boundKeys(leftPlayer,rightPlayer)
        ballPosx = self.gs.ballPos[1]
        ballPosy = self.gs.ballPos[0]
        ballSpeedx = self.gs.ballVelocity[1]
        ballSpeedy = self.gs.ballVelocity[0]
        
        if leftPlayer.isHuman == False:
            self.gs.batLeftPos[0] = self.moveBatLeft(leftPlayer)
        if rightPlayer.isHuman == False:
            self.gs.batRightPos[0] = self.moveBatRight(rightPlayer)
            
        [ballPosx,ballPosy,ballSpeedx,ballSpeedy] = self.moveBall(ballPosx,ballPosy,ballSpeedx,ballSpeedy)
        [self.gs.ballPos[1],self.gs.ballPos[0],self.gs.ballVelocity[1],self.gs.ballVelocity[0]] = [ballPosx,ballPosy,ballSpeedx,ballSpeedy]
        
        if ballPosx < 0:
            self.gs.gameover = 1
            self.rightCounter+=1
        elif ballPosx > self.gs.boardWidth:
            self.gs.gameover = 2
            self.leftCounter+=1
        
        if self.gs.ballVelocity[1] > 0:
            self.gs.ballVelocity[1] = self.gs.ballVelocity[1]+0.01
        else:
            self.gs.ballVelocity[1] = self.gs.ballVelocity[1]-0.01  
    
    def moveBatLeft(self,leftPlayer):
        direction = leftPlayer.makeMove()
        return self.gs.batStepSize*direction + self.gs.batLeftPos[0]
            
    def moveBatRight(self,rightPlayer):
        direction = rightPlayer.makeMove()
        return  self.gs.batStepSize*direction + self.gs.batRightPos[0]
        
    def moveBall(self,posx,posy,speedx,speedy):
        newPosx = posx + speedx
        newPosy = posy + speedy
        newSpeedx = speedx
        newSpeedy = speedy
        if newPosy < 0:
            newPosy = (-1) * posy
            newSpeedy = (-1) * speedy
        if newPosy > self.gs.boardHeight:
            newPosy = self.gs.boardHeight - (newPosy - self.gs.boardHeight)
            newSpeedy = (-1) * speedy
        
        leftEdge = self.gs.batThickness + self.gs.ballRadius
        rightEdge = self.gs.boardWidth - self.gs.batThickness - self.gs.ballRadius
        if rightEdge >= newPosx >= leftEdge:
            return [newPosx,newPosy,newSpeedx,newSpeedy]
        
        lowEdge = self.gs.batLeftPos[0] + self.gs.batLength/2
        highEdge = self.gs.batLeftPos[0] - self.gs.batLength/2
        distToCenter = newPosy - self.gs.batLeftPos[0]
        # print(newPosx,'<',leftEdge,'and', lowEdge,'>=',newPosy,'>=',highEdge)
        if newPosx < leftEdge and lowEdge >= newPosy >= highEdge:
            newPosx = leftEdge + (leftEdge - newPosx)
            newSpeedx = (-1) * newSpeedx
            newSpeedy = newSpeedy + distToCenter/2
            #to do: newSpeedy depends on where on the bat
        lowEdge = self.gs.batRightPos[0] + self.gs.batLength/2
        highEdge = self.gs.batRightPos[0] - self.gs.batLength/2
        distToCenter = newPosy - self.gs.batRightPos[0]
        
        if newPosx > rightEdge and lowEdge >= newPosy >= highEdge:
            newPosx = rightEdge + (rightEdge - newPosx)
            newSpeedx = (-1) * newSpeedx
            newSpeedy = newSpeedy + distToCenter/2
        return [newPosx,newPosy,newSpeedx,newSpeedy]
        
        
        
        
        