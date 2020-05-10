from tkinter import *

class GUI:
    def __init__(self,window, gameState):
        self.window = window
        self.gs = gameState
        self.drawCanvas()
        self.drawBall()
        self.drawBats()

    # GUI.window.bind("<Button-1>", lambda event: self.gamePlay(event,GUI), GUI)
        
    def boundKeys(self,leftPlayer,rightPlayer):
        if(leftPlayer.isHuman):
            self.window.bind('a',lambda event: leftPlayer.makeMove(event))
            self.window.bind('z',lambda event: leftPlayer.makeMove(event))
        if(rightPlayer.isHuman):
            self.window.bind(chr(39),lambda event: rightPlayer.makeMove(event))
            self.window.bind(chr(47),lambda event: rightPlayer.makeMove(event))
            
    def test(self,event):
        print('pressed a')    
        
    def drawCanvas(self):
        self.canvas=Canvas(self.window,width=self.gs.boardWidth,height=self.gs.boardHeight)
        self.canvas.pack()
        self.window.attributes('-topmost',True)
        
    def drawBall(self):
        r = self.gs.ballRadius
        x = self.gs.ballPos[1]
        y = self.gs.ballPos[0]
        self.canvas.create_oval(x-r, y-r, x+r, y+r,fill='black')
        
    def drawBats(self):
        x1 = self.gs.batLeftPos[1] - self.gs.batThickness/2
        y1 = self.gs.batLeftPos[0] - self.gs.batLength/2
        x2 = self.gs.batLeftPos[1] + self.gs.batThickness/2
        y2 = self.gs.batLeftPos[0] + self.gs.batLength/2
        self.canvas.create_rectangle(x1,y1,x2,y2,fill='black')
        x1 = self.gs.batRightPos[1] - self.gs.batThickness/2
        y1 = self.gs.batRightPos[0] - self.gs.batLength/2
        x2 = self.gs.batRightPos[1] + self.gs.batThickness/2
        y2 = self.gs.batRightPos[0] + self.gs.batLength/2
        self.canvas.create_rectangle(x1,y1,x2,y2,fill='black')
    
    def update(self):
        self.canvas.delete(ALL)
        self.drawBall()
        self.drawBats()
        self.window.update()