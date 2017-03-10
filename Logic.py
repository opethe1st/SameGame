import random
import os
import sys

if getattr(sys, 'frozen', False):
    # we are running in a bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = '.'

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (34,139,34)
RED =   (255,   0,   0)
DARKORCHID =(153,50,204)
BROWN = (165,42,42)

BallColours = [RED,BLUE,GREEN,DARKORCHID,BROWN]

class Ball:
    def __init__(self,colour = WHITE):
        self.colour = colour
    def clear(self):
        self.colour = WHITE

class Square:
    def __init__(self,colour,position):
        self.colour = colour
        self.position = position
    def clear(self):
        self.colour = WHITE

class Board:
    def __init__(self, width=20,height=16):
        self.width = width
        self.height = height
        self.balls = [[Ball() for i in range(self.height)] for j in range(self.width)]
        self.nballsleft = width*height
        self.nmoves = 0
        self.score = 0
        f = open(basedir + os.sep +'TopScores.txt','r')
        score = f.readline()
        if len(score)>0:    
            self.highScore = int(score)
        else:
            self.highScore = 0 
    
    def initBoard(self):
        for i in range(self.width):
            for j in range(self.height):
                self.balls[i][j].colour = BallColours[random.randint(0,4)]

    def adjacent(self,position):
            "returns the list of balls of the same colour adjacent to the ball at position- position"
            x,y = position
            AdjacentSameBalls=[]
            for m,n in [(0,1),(0,-1),(1,0),(-1,0)]:
                if 0<=x+m<self.width and 0<=y+n<self.height:
                    if self.balls[x][y] and self.balls[x+m][y+n]:
                        if self.balls[x][y].colour==self.balls[x+m][y+n].colour:
                            AdjacentSameBalls.append((x+m,y+n))
            return AdjacentSameBalls

    def findAdjacentBalls(self,ballposition):
        """returns a list of all the balls of the same colour adjacent to ballposition"""
        x,y = ballposition
        stack = [ballposition]
        visited = [[False for i in xrange(self.height)] for j in xrange(self.width) ]
        #print x,y
        visited[x][y] = True
        connectedballs = [ballposition]
        while stack:
            ballposition = stack.pop()
            for position in self.adjacent(ballposition):
                x1,y1 = position
                if not visited[x1][y1]:
                    
                    stack.append(position)
                    connectedballs.append(position)
                    visited[x1][y1] = True
            #print stack 
        return connectedballs
        
    def joiningSquares(self,side):
        
        squareballs = set()
        for x in range(self.width):
            for y in range(self.height):
                for m,n in [(0,1),(0,-1),(1,0),(-1,0)]:
                        if 0<=x+m<self.width and 0<=y+n<self.height:
                            if self.balls[x][y] and self.balls[x+m][y+n]:
                                if self.balls[x][y].colour==self.balls[x+m][y+n].colour and self.balls[x][y].colour!=WHITE:

                                    square = Square(self.balls[x][y].colour, (x+m/2.0,y+n/2.0))
                                    squareballs.add(square)
                        
        return squareballs

    def markBalls(self,position):
        connectedballs = self.findAdjacentBalls(position)
        if len(connectedballs)==1: #means that it has no similarly coloured balls as neighbors
            return
        self.score+=len(connectedballs)**2+100
        self.nmoves+=1
        for ballposition in connectedballs:
            x,y = ballposition
            self.balls[x][y]=None
            self.nballsleft-=1
    
    def clearBalls(self):
        "gravity. Balls fall into space vacated by removed balls"
        for i in xrange(self.width):
            for j in xrange(self.height):
                if self.balls[i][j] is None:
                    for k in reversed(xrange(j)):
                        self.balls[i][k+1] = self.balls[i][k]
                    self.balls[i][0]= None
        #shift to the left when the last row has an empty column     
        for i in reversed(xrange(self.width)): #through columns
            if self.balls[i][-1] is None:
                for j in xrange(self.height): 
                    for k in (xrange(i,self.width-1)): 
                        self.balls[k][j] = self.balls[k+1][j]
                    self.balls[-1][j]= None
        if self.score>self.highScore:
            self.highScore = self.score




    def isGameOver(self):
        def adjacent(position):
            "returns the list of balls of the same colour adjacent to the ball at position- position"
            x,y = position
        for x in xrange(self.width):
            for y in xrange(self.height):
                if len(self.adjacent((x,y)))>0 and self.balls[x][y].colour!=WHITE:
                    return False
        if self.score>=self.highScore:
            self.highScore = self.score
            f = open(basedir + os.sep +'TopScores.txt','w')
            score = f.write(str(self.score))
        return True
