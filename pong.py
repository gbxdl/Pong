#!/usr/bin/env python3
from tkinter import *
import time

from gameState import *
from progress import *
from GUI import *
from randomBot import *
from human import *
from basicBot import *
from reinforceBot import *

tic = time.time()
numberOfGames = 1000000
gameCounter = 0

gameState = gameState()
progress = progress(gameState)

leftPlayer = reinforceBot(gameState,'left',False)
rightPlayer = randomBot(gameState,'right', False)

while gameState.gameover == 0:
    progress.timeStep(leftPlayer,rightPlayer)
    gameCounter+=1    
    if gameCounter >= numberOfGames:
        break
    # if gameState.guiOn:
        # gameState.gui.update()

toc = time.time()

print('played', numberOfGames,'in', toc-tic, 'seconds')

leftPlayer.saveTable()