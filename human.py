from player import *

class human(player):
    def __init__(self,gameState,whichPlayer):
        super().__init__(gameState,whichPlayer)
        self.isHuman = True
        
    def makeMove(self,event):
        if event.char == 'a' :
            self.gs.batLeftPos[0] = -self.gs.boardHeight/20 + self.gs.batLeftPos[0]
        if event.char == 'z' and self.whichPlayer == 'left':
            self.gs.batLeftPos[0] = self.gs.boardHeight/20 + self.gs.batLeftPos[0]
        if event.char == chr(39):
            self.gs.batRightPos[0] = -self.gs.boardHeight/20 + self.gs.batRightPos[0]
        if event.char == chr(47):
            self.gs.batRightPos[0] = self.gs.boardHeight/20 + self.gs.batRightPos[0]
        return