class player:
    def __init__(self,gameState,whichPlayer='left', loadTable = False):
        self.gs = gameState
        self.whichPlayer = whichPlayer
        self.isHuman = False
        
    def makeMove(self):
        return 0
    
    def saveTable(self):
        pass