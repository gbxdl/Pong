class player:
    def __init__(self,gameState,whichPlayer = 'left', loadTable = False, progress = None):
        self.gs = gameState
        self.whichPlayer = whichPlayer
        self.isHuman = False
        loadTable = loadTable
        self.progress = progress
        
    def makeMove(self):
        return 0
    
    def saveTable(self):
        pass