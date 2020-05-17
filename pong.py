#!/usr/bin/env python3
import time

from gameState import *
from progress import *
from GUI import *
from randomBot import *
from human import *
from basicBot import *
from reinforceBot import *

play = 0
train = 0# when training the ball velocity is set much higher
showGame = 1
test = 0

tic = time.time()
numberOfGames = 10
gameCounter = 0

gameState = gameState(play, showGame)
progress = progress(gameState)

if play:
    leftPlayer = reinforceBot(gameState, 'left', True, progress)
    rightPlayer = human(gameState,'right', True, progress)
    while gameState.gameover == 0:
        progress.timeStep(leftPlayer,rightPlayer)
        gameState.gui.update()
        if gameState.gameover > 0:
            gameCounter += 1
            gameState.startGame()
        if gameCounter >= numberOfGames:
            break
elif train:
    leftPlayer = reinforceBot(gameState,'left',True, progress)
    rightPlayer = randomBot(gameState,'right', False)
    while gameState.gameover == 0:
        progress.timeStep(leftPlayer,rightPlayer)
        if gameState.gameover > 0:
            gameCounter += 1
            gameState.startGame()
        if gameCounter >= numberOfGames:
            break
elif showGame:
        numberOfGames = 10  
        leftPlayer = reinforceBot(gameState,'left',True, greedy = True)
        rightPlayer = basicBot(gameState,'right', True, greedy = True)
        # gameState.ballVelocity[1] *= 50
        while gameState.gameover == 0:
            # time.sleep(.1)
            progress.timeStep(leftPlayer,rightPlayer)
            gameState.gui.update()
            if gameState.gameover > 0:
                gameCounter += 1
                gameState.startGame()
                # gameState.ballVelocity[1] *= 50
            if gameCounter >= numberOfGames:
                break
elif test:
    numberOfGames = 1000
    leftPlayer = reinforceBot(gameState,'left', True, progress)
    rightPlayer = reinforceBot(gameState,'right', True, progress)
    for i in range(numberOfGames):
        while gameState.gameover == 0:
            progress.timeStep(leftPlayer,rightPlayer)
        gameState.startGame()

toc = time.time()

print('played', numberOfGames,'games in', toc-tic, 'seconds')
print('left won', progress.leftCounter, 'out of', numberOfGames)

leftPlayer.saveTable()
rightPlayer.saveTable()