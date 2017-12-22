import tkinter as tk
# import time
from random import randint
import sys


# The Program allows a user to play the Snake game once until a loss.

# Pixel is a class that inherits Tkinter Label. It is a Label that allows you to store relative positions
class Pixel(tk.Label):
    # The following function is the Pixel Class constructor. It overwrites the constructor for the Tkinter Frame
    # self is a reference to the particular instance of Game
    # parent is the parent, or "root", that the Game will be placed on
    # *args is a dictionary, or list, representing the non-keyworded arguments passed into Game
    # **kwargs is a dictionary, or list, representing the keyworded arguments passed into Game
    def __init__(self, parent, *args, **kwargs):
            tk.Label.__init__(self, parent, *args, **kwargs)
            self.configure(borderwidth="2", relief="groove", background='black')
            self.xPos = 0  # Integer representation of the relative x position of the pixel
            self.yPos = 0  # Integer representation of the relative y position of the pixel

    # The following function sets the values of the xPos and yPos integers
    def setPos(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

    # The following function returns the value of xPos
    def getX(self):
        return self.xPos

    # The following function returns the value of yPos
    def getY(self):
        return self.yPos

# Game is a class that inherits Tkinter Frame. It not only implements the GUI, but as of now handles game mechanics
class Game(tk.Frame):
    # The following function is the Game Class constructor. It overwrites the constructor for the Tkinter Frame
    # self is a reference to the particular instance of Game
    # parent is the parent, or "root", that the Game will be placed on
    # *args is a dictionary, or list, representing the non-keyworded arguments passed into Game
    # **kwargs is a dictionary, or list, representing the keyworded arguments passed into Game
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs) # Initializes Game as a frame
        self.place(x=0, y=0)
        self.parent = parent  # Local instance of Game parameter parent
        self.xVel = 1  # Integer that represents relative horizontal movement
        self.yVel = 0  # Integer that represents relative vertical movement
        self.pixels = []  # Array of Pixels that represents the individual pixels/tiles/spots/boxes
        self.snake = []  # Array of Pixels that represents the pixels specifically in the Snake
        self.apple = 0  # Pixel representing the apple the snake eats to grow and gain points. Initially set to null
        if 'height' in kwargs and 'width' in kwargs:
            self.pixelsWide = kwargs.get('width') // 50
            self.pixelsHigh = kwargs.get('height') // 50
        for x in range(self.pixelsWide):
            self.pixels.append([])
            for y in range(self.pixelsHigh):
                self.pixels[x].append(Pixel(self, borderwidth="2", relief="groove", background='black'))
                self.pixels[x][y].place(x=x * 50, y=y * 50, height=50, width=50)
                self.pixels[x][y].setPos(x, y)
        self.__placeApple()

        for x in range(4):
            self.__addSnake(self.pixels[x][10])

    #  The following function places the apple in a random and valid location (not on Snake, not out of bounds, etc.)
    def __placeApple(self):
        x = randint(0, self.pixelsWide - 1)
        y = randint(0, self.pixelsHigh - 1)
        while self.pixels[x][y] in self.snake:
            x = randint(0, self.pixelsWide - 1)
            y = randint(0, self.pixelsHigh - 1)
        self.apple = self.pixels[x][y]
        self.apple.configure(background='green')

    # The following function adds pixel to snake and sets it white
    # pixel is the specific pixel that is being added to the snake
    def __addSnake(self, pixel):
        self.snake.append(pixel)
        self.snake[len(self.snake) - 1].configure(background='white')

    # The following function sets the backend of snake black and removes it from the snake. Used for movement
    def __remSnake(self):
        self.snake[0].configure(background='black')
        del self.snake[0]

    def setRight(self, event):
        if self.xVel == 0:  # Blocks the snake from doing 180 degree turns
            self.xVel = 1
            self.yVel = 0

    # The following function sets the relative movement parameters for for left movement the moving box
    def setLeft(self, event):
        if self.xVel == 0:
            self.xVel = -1
            self.yVel = 0

    # The following function sets the relative movement parameters for for upwards movement the moving box
    def setUp(self, event):
        if self.yVel == 0:
            self.xVel = 0
            self.yVel = -1

    # The following function sets the relative movement parameters for for downwards movement the moving box
    def setDown(self, event):
        if self.yVel == 0:
            self.xVel = 0
            self.yVel = 1

    # The following function prints the location of all pixels in snake
    def __printSnake(self):
        print(len(self.snake))
        for x in range(0, len(self.snake)):
            print("Snake: ", x, " - PosX: ", self.snake[x].getX(), " - PosY: ", self.snake[x].getY())

    # The following function "moves" the snake
    def move(self):
        if not (self.xVel == 0 and self.yVel == 0):
            xNext = self.snake[len(self.snake)-1].getX() + self.xVel
            yNext = self.snake[len(self.snake)-1].getY() + self.yVel
            if 0 <= xNext < self.pixelsWide and 0 <= yNext < self.pixelsHigh:

                if self.snake[len(self.snake)-1] != self.apple:
                    self.__addSnake(self.pixels[xNext][yNext])
                    self.__remSnake()
                    for x in range(0, len(self.snake)-1):
                        if self.snake[x] == self.snake[len(self.snake)-1]:
                            self.__printSnake()
                            self.snake[x].configure(background='red')
                            return

                else:
                    self.__addSnake(self.pixels[xNext][yNext])
                    self.__remSnake()
                    x = 2 * self.snake[0].getX() - self.snake[1].getX()
                    y = 2 * self.snake[0].getY() - self.snake[1].getY()
                    self.pixels[x][y].configure(background='white')
                    self.snake.insert(0, self.pixels[x][y])
                    self.__placeApple()

            else:
                # self.parent.quit() --> exits program on game over
                self.__printSnake()
                return
        self.parent.after(200, self.move) # New way to set "speed" in ms


def main():
    root = tk.Tk()  # The root or parent window of the game board
    GAME_WIDTH = 1000  # Represents the width in pixels of the game board and window
    GAME_HEIGHT = 1000  # Represents the height in pixels of the game board and window
    # GAME_SPEED = .2  # Represents the "speed" of movement. Depreciated as of now
    root.geometry('{}x{}'.format(GAME_WIDTH, GAME_HEIGHT))
    root.resizable(width=False, height=False)
    root.title("Snake")
    board = Game(root, background='red', width=GAME_WIDTH, height=GAME_HEIGHT)  # The instantiation of the Game Board
    root.bind('<Escape>', sys.exit)
    root.bind('<d>', board.setRight)
    root.bind('<a>', board.setLeft)
    root.bind('<w>', board.setUp)
    root.bind('<s>', board.setDown)
    board.move()
    root.mainloop()


if __name__ == '__main__':
    main()