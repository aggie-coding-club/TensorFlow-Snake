from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import QTimer, Qt
import sys, random

# This Program is the game of Snake

# Function that defines an returns a dictionary of a box's grid coordinates
# Probably would be more straightforward if defined as a class, but I was experiencing issues tedious to work around.
# Specifically, "in" did not work for me as expected when defined as class (i.e box in bits, x in list)
# If my issue is not unique, I suppose box could be converted to a class, but at the cost of additional code
# Basically, I'm pretty sure we would have to perform linear searches on the snake and compare each of box's members
# A dictionary serves as a "compromise" for now because it gives us more readable syntax (e.g. Accessing 'x')
def box(x, y):
    return {
        'x': x,
        'y': y
    }

# Class that contains the Snake and all its behaviors
# A snake is comprised of a series of boxes, in this case a list of boxes named bits
# The snake maintains its velocity (vel) and moves with respect to it
# It receives/decodes commands that ask it to change its velocity
# Also, it grows when it is required to grow
class Snake:

    # A dictionary that maps specific key presses to a tuple of velocities x and y respectively.
    moveSet = {
        'W': (0, -1),
        'A': (-1, 0),
        'S': (0, 1),
        'D': (1, 0)
    }

    # Constructor for the Snake Class
    # It assigns an initial box to bits and sets its velocity (and next velocity) to 0
    def __init__(self):

        self.bits = []  # List that maintains all boxes in the snake. bits[0] is the head
        self.bits.append(box(0, 0))
        self.vel = (0, 0)  # A tuple of the current relative x and y velocities
        self.nextVel = (0, 0)  # A tuple of the next velocities. Used to restrict illegal moves

    # Adds a box to bits, and thus lengthens the snake
    def addBit(self):
        self.bits.append(box(self.bits[0]['x']-self.vel[0], self.bits[0]['y']-self.vel[1]))

    # Returns true and moves the snake if possible, else simply returns false (and ends the game by extension)
    # boardWidth is one over the furthest right position of the head
    # boardHeight is one over the furthest downward position of the head
    # Both boardWidth and boardHeight are used to check if the snake has tried to move out of bounds
    # Comment: Not really an elegant solution. Please replace/move if you think you have a better idea.
    def tryMove(self, boardWidth, boardHeight):
        self.vel = self.nextVel
        if self.bits[0]['x'] + self.vel[0] == boardWidth or self.bits[0]['x'] + self.vel[0] == -1:
            return False
        if self.bits[0]['y'] + self.vel[1] == boardHeight or self.bits[0]['y'] + self.vel[1] == -1:
            return False
        for i in range(len(self.bits) - 1, 0, -1):
            self.bits[i]['x'] = self.bits[i-1]['x']
            self.bits[i]['y'] = self.bits[i-1]['y']
        self.bits[0]['x'] += self.vel[0]
        self.bits[0]['y'] += self.vel[1]

        return False if self.bits[0] in self.bits[1:] else True

    # Assigns nextVel to a potential velocity if it is a legal move
    # potVel is the command given for the potential velocity
    def setVel(self, potVel):
        if self.moveSet[potVel][0] == -self.vel[0] and self.moveSet[potVel][1] == -self.vel[1]:
            return
        if self.moveSet[potVel] == self.nextVel:
            return
        self.nextVel = self.moveSet[potVel]

# Class that contains the majority of GUI Elements and operates the game
# It extends QWidget, which is a pretty basic Element in Qt. It does a lot of stuff, look it up in the API if curious
class Window(QWidget):

    # Constructor for the Window Class
    # **kwargs is a dictionary of all named arguments passed
    def __init__(self, **kwargs):
        super().__init__()  # Calls the parent class (QWidget) constructor

        # The relative width of the board. Assigned by default to 8
        self.boardWidth = kwargs['boardWidth'] if 'boardWidth' in kwargs else 8
        # The relative height of the board. Assigned by default to 8
        self.boardHeight = kwargs['boardHeight'] if 'boardHeight' in kwargs else 8
        # The absolute width & height of any box of the board in pixels. By default, a box is 50x50 pixels
        self.boxSize = kwargs['boxSize'] if 'boxSize' in kwargs else 50
        # The interval at which the GUI refreshes, and thus the snake moves
        interval = kwargs['interval'] if 'interval' in kwargs else 500

        # Instantiation of the Snake class. Creates the snake necessary for the game
        self.snake = Snake()
        self.placeApple()

        self.time = QTimer(self)  # A timer that sends a signal whenever the interval has been reached
        self.time.setInterval(interval)

        # Uses the concept of signals and slots integral to Qt
        # Basically, calls whatever function (slot) I connect whenever a signal is sent by another function (signal)
        # In this case time.timeout is the signal. It sends a signal whenever the interval has been reached
        # It calls update, which is a method defined inside QWidget
        # update does many things, but in this case effectively serves to refresh GUI and call paintEvent implicitly
        self.time.timeout.connect(self.update)
        self.time.start()

        self.init_ui()

    # Initialize all GUI components
    def init_ui(self):
        self.setStyleSheet('Background: grey')

        width = self.boardWidth*self.boxSize
        height = self.boardHeight*self.boxSize
        self.setGeometry(0, 30, width, height)
        self.show()

    # paintEvent serves to call drawBoard on interval. It overrides the same method found within QWidget
    # e is a QPaintEvent passed into paintEvent. I'm not sure what it does, but is required to properly override
    def paintEvent(self, e):
        paintr = QPainter()  # Object used to actually draw the board
        paintr.begin(self)
        self.drawBoard(paintr)
        paintr.end()

    # Draws the new game-state by calling supporting methods and checking if an apple has been eaten
    # paintr is a QPainter object that is used to actually draw the board
    def drawBoard(self, paintr):
        self.drawApple(paintr)
        self.drawSnake(paintr)

        if self.apple in self.snake.bits:
            self.snake.addBit()
            self.placeApple()
            self.drawApple(paintr)

    # Draws the snake. Also ends the game if the snake has collided with an obstacle
    # paintr is a QPainter object that is used to actually draw the board
    def drawSnake(self, paintr):
        paintr.setPen(QPen(QColor(0, 255, 0), 2, Qt.SolidLine))
        paintr.setBrush(QBrush(QColor(80, 0, 0), Qt.SolidPattern))

        size = self.boxSize

        if self.snake.tryMove(self.boardWidth, self.boardHeight):
            for b in self.snake.bits:
                paintr.drawRect(b['x']*size, b['y']*size, size, size)
        else:
            self.time.stop()
            for b in self.snake.bits[1:]:
                paintr.drawRect(b['x']*size, b['y']*size, size, size)
            paintr.setBrush(QBrush(QColor(255, 0, 0), Qt.SolidPattern))
            paintr.drawRect(self.snake.bits[0]['x']*size, self.snake.bits[0]['y']*size, size, size)
        self.printState()

    # Draws the apple
    # paintr is a QPainter object that is used to actually draw the board
    def drawApple(self, paintr):

        size = self.boxSize

        paintr.setBrush(QBrush(QColor(191, 97, 0), Qt.SolidPattern))
        paintr.setPen(QPen(QColor(0, 255, 0), 2, Qt.SolidLine))
        paintr.drawRect(self.apple['x']*size, self.apple['y']*size, size, size)

    # Places the apple until it is not inside snake (brute force, definitely better ways. Bad if large)
    def placeApple(self):
        self.apple = box(random.randint(0, self.boardWidth-1), random.randint(0, self.boardHeight-1))
        while self.apple in self.snake.bits:
            self.apple = box(random.randint(0, self.boardWidth-1), random.randint(0, self.boardHeight-1))

    # Prints the current state of the game
    # Preliminary attempt to represent the game-state for use in machine learning
    def printState(self):
        boardList = [(['*']*self.boardWidth) for i in range(self.boardHeight)]
        for b in self.snake.bits[1:]:
            boardList[b['y']][b['x']] = 'o'
        boardList[self.snake.bits[0]['y']][self.snake.bits[0]['x']] = 'O'
        boardList[self.apple['y']][self.apple['x']] = 'x'

        for l in boardList:
            print(l[:])
        print('----------------------------------------------')

    # Overrides method found within QWidget
    # It is called whenever any key is pressed
    # QKeyEvent is the ASCII code of the key pressed
    def keyPressEvent(self, QKeyEvent):
        key = chr(QKeyEvent.key())
        if key in set('WASD'):
            self.snake.setVel(key)


if __name__ == '__main__':
    app = QApplication(sys.argv)  # Instantiation of QApplication required for Qt. It is the backbone.
    w = Window(boardWidth=15, boardHeight=15)  # Instantiation of the Window class. Implicitly placed on app
    sys.exit(app.exec_())  # Exits the game when app has terminated
