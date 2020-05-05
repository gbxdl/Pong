class progress:
    def __init__(self,gameState):
        self.gs = gameState
        
    def timeStep(self):
        self.moveLeftBat()
        self.moveRightBat()
        [self.gs.ballPos[1],self.gs.ballPos[0],self.gs.ballVelocity[1],self.gs.ballVelocity[0]] = self.moveBall(self.gs.ballPos[1],self.gs.ballPos[0],self.gs.ballVelocity[1],self.gs.ballVelocity[0])
        
    def moveBall(self,posx,posy,speedx,speedy):
        newPosx = posx + speedx
        newPosy = posy + speedy
        newSpeedx = speedx
        newSpeedy = speedy
        if newPosy < 0:
            newPosy = (-1) * newPosy
            newSpeedy = (-1) * speedy
        if newPosy > self.gs.boardHeight:
            newPosy = self.gs.boardHeight - (newPosy - self.gs.boardHeight)
            newSpeedy = (-1) * speedy
            
        return [posx,posy,speedx,speedy]
        
                
    def moveLeftBat(self):
        pass
        
    def moveRightBat(self):
        pass
        