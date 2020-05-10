#just move towards  ball

from player import *

class basicBot(player):
    def makeMove(self):
        if self.whichPlayer == 'left':
            self.batPosy = self.gs.batLeftPos[0]
        elif self.whichPlayer == 'right':
            self.batPosy = self.gs.batRightPos[0]
        else:
            print('error: basicBot does not know who he is')
        # print(self.gs.ballPos[0], '>', self.batPosy)
        if self.gs.ballPos[0] > self.batPosy:
            return 1
        elif self.gs.ballPos[0] < self.batPosy:
            return -1
        return 0