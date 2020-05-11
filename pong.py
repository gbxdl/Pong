#!/usr/bin/env python3
import time

from gameState import *
from progress import *
from GUI import *
from randomBot import *
from human import *
from basicBot import *
from reinforceBot import *

play = False
train = True # when training the ball velocity is set much higher
showGame = False

tic = time.time()
numberOfGames = 1000
gameCounter = 0

gameState = gameState(play, showGame)
progress = progress(gameState)

if play:
    leftPlayer = human(gameState, 'left')
    rightPlayer = basicBot(gameState,'right', False)
    while gameState.gameover == 0:
        progress.timeStep(leftPlayer,rightPlayer)
        gameState.gui.update()
elif train:
    leftPlayer = reinforceBot(gameState,'left',False)
    rightPlayer = basicBot(gameState,'right', False)
    gameState.ballVelocity[1] *= 50
    while gameState.gameover == 0:
        progress.timeStep(leftPlayer,rightPlayer)
        if gameState.gameover > 0:
            gameCounter+=1
            gameState.startGame()
            gameState.ballVelocity[1] *= 50
        if gameCounter >= numberOfGames:
            break
elif showGame:
        numberOfGames = 1    
        leftPlayer = basicBot(gameState,'left',False)
        rightPlayer = basicBot(gameState,'right', False)
        gameState.ballVelocity[1] *= 50
        while gameState.gameover == 0:
            time.sleep(.1)
            progress.timeStep(leftPlayer,rightPlayer)
            gameState.gui.update()
            if gameState.gameover > 0:
                gameCounter+=1
                gameState.startGame()
            if gameCounter >= numberOfGames:
                break
    # if gameState.guiOn:
        # gameState.gui.update()

toc = time.time()

print('played', numberOfGames,'games in', toc-tic, 'seconds')

leftPlayer.saveTable()