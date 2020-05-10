import random
import math

from player import *

class randomBot(player):

    def makeMove(self):
        return 1-math.floor(3*random.random()) 