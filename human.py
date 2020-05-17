from player import *

class human(player):
    def __init__(self,gameState, whichPlayer = 'left', loadTable = False):
        super().__init__(gameState,whichPlayer, loadTable)
        self.isHuman = True
        
    def makeMove(self,event):
        humanhelp = 2
        if event.char == 'a' and self.whichPlayer == 'left':
            self.gs.batLeftPos[0] = self.progress.moveBatLeft(-1*humanhelp)
        if event.char == 'z' and self.whichPlayer == 'left':
            self.gs.batLeftPos[0] = self.progress.moveBatLeft(1*humanhelp)
        if event.char == chr(39) and self.whichPlayer == 'right':
            self.gs.batRightPos[0] = self.progress.moveBatRight(-1*humanhelp)
        if event.char == chr(47) and self.whichPlayer == 'right':
            self.gs.batRightPos[0] = self.progress.moveBatRight(1*humanhelp)