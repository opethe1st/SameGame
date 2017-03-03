import random
NOCOLOUR,NRED,NBLUE,NGREEN  = 0,1,2,3
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

def numToColour(num):
    if num==NRED:
        return RED
    elif num==NBLUE:
        return BLUE
    elif num==NGREEN:
        return GREEN
    else:
        return (255, 255, 255)
class Ball:
    def __init__(self,colour = (255, 255, 255)):
        self.colour = numToColour(colour)
    def clear(self):
        self.colour = numToColour(NOCOLOUR)

class Board:
    def __init__(self, size=4):
        self.size = size
        self.balls = [[Ball() for i in range(self.size)] for j in range(self.size)]
    
    def initBoard(self):
        for i in range(self.size):
            for j in range(self.size):
                self.balls[i][j].colour = numToColour(random.randint(1,3))

        #[[ self.balls[i][j].colour = numToColour(random.randint(1,4)) for i in xrange(size)] for j in xrange(size)]

    def findAdjacentBalls(self,ballposition):
        """returns a list of all the balls of the same colour adjacent to ballposition"""
        def adjacent(position):
            "returns the list of balls of the same colour adjacent to the ball at position- position"
            x,y = position
            listposition=[]
            for m,n in [(0,1),(0,-1),(1,0),(-1,0)]:
                    if 0<=x+m<self.size and 0<=y+n<self.size and self.balls[x][y].colour==self.balls[x+m][y+n].colour:
                        listposition.append((x+m,y+n))
            return listposition

        x,y = ballposition
        stack = [ballposition]
        visited = [[False for i in xrange(self.size)] for j in xrange(self.size) ]
        #print x,y
        visited[x][y] = True
        listofballs = [ballposition]
        while stack:
            ballposition = stack.pop()
            for position in adjacent(ballposition):
                x1,y1 = position
                if not visited[x1][y1]:
                    
                    stack.append(position)
                    listofballs.append(position)
                    visited[x1][y1] = True
            #print stack 
        return listofballs
        


    def markBalls(self,position):
        for ballposition in self.findAdjacentBalls(position):
            x,y = ballposition
            self.balls[x][y].clear()
        pass
    
    def clearBalls(self):


        "gravity is to the left. Currently inefficent"
        for i in xrange(self.size):
            for j in xrange(self.size):
                if self.balls[i][j].colour==(255, 255, 255):
                    for k in reversed(xrange(j)): #,self.size-1
                        self.balls[i][k+1] = self.balls[i][k]
                        k+=1
                    self.balls[i][0]= Ball()

    def isGameOver(self):
        pass
