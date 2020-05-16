#!/usr/bin/env python3
import time
import matplotlib.pyplot as plt

from gameState import *
from progress import *
from GUI import *
from randomBot import *
from human import *
from basicBot import *
from reinforceBot import *

numberOfGames = 10000
gameCounter = 0
saveEvery = 1000

winRate = []
partialWinRate = []
timeDataPoints = []
partialGameCounter = 0
partialWinCounter = 0

gameState = gameState()
progress = progress(gameState)

leftPlayer = reinforceBot(gameState, whichPlayer = 'left', loadTable = True, progress = progress)
rightPlayer = randomBot(gameState, whichPlayer = 'right', loadTable = False, progress = progress)

tic = time.time()
tic2 = time.time()
while gameState.gameover == 0:
    progress.timeStep(leftPlayer,rightPlayer)
    if gameState.gameover > 0:
        gameCounter += 1
        partialGameCounter += 1
        if gameState.gameover == 2:
            partialWinCounter += 1
        gameState.startGame()
        if gameCounter % saveEvery == 0:
            winRate.append(progress.leftCounter / gameCounter)
            partialWinRate.append(partialWinCounter / partialGameCounter)
            toc = time.time()
            print(gameCounter, 'games, time:', toc-tic, 'seconds, overall winRate left:', progress.leftCounter / gameCounter)
            print('last', saveEvery, 'games, time:', toc-tic2, 'seconds, partial winRate left:', partialWinCounter / partialGameCounter)
            partialGameCounter = 0
            partialWinCounter = 0
            timeDataPoints.append(toc-tic2)
            leftPlayer.saveTable()
            rightPlayer.saveTable()
            tic2 = time.time()
    if gameCounter >= numberOfGames:
        break

bins = int(numberOfGames/saveEvery)
games = [saveEvery * i for i in range(bins+1)]

print(winRate)

toc = time.time()

print('played', numberOfGames,'games in', toc-tic, 'seconds')
print('left won', progress.leftCounter, 'out of', numberOfGames)

leftPlayer.saveTable()

progress.leftCounter = 0
numberOfGames = 100

leftPlayer = reinforceBot(gameState, whichPlayer = 'left', loadTable = True, progress = progress, greedy = True)
rightPlayer = randomBot(gameState,'right', False, progress)

for i in range(numberOfGames):
    while gameState.gameover == 0:
        progress.timeStep(leftPlayer,rightPlayer)
    gameState.startGame()

print('test: played', numberOfGames,'games against randomBot')
print('won', progress.leftCounter, 'out of', numberOfGames)

progress.leftCounter = 0
rightPlayer = basicBot(gameState,'right', False, progress)

for i in range(numberOfGames):
    while gameState.gameover == 0:
        progress.timeStep(leftPlayer,rightPlayer)
    gameState.startGame()

print('Test: played', numberOfGames,'games against basicBot')
print('Won', progress.leftCounter, 'out of', numberOfGames)

plt.figure('overall win rate')
plt.plot(games[1:], winRate, label='Overall win rate')
plt.legend(loc="upper left")

plt.figure('partial win rate')
plt.plot(games[1:], partialWinRate, label='Win rate of segment')
plt.legend(loc="upper left")
# 
plt.figure('time')
plt.plot(games[1:], timeDataPoints, label='Time of segment')
plt.legend(loc="upper left")
plt.show()