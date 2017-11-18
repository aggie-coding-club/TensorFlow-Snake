import tkinter as tk
import time
from random import randint
#import numpy as np
import sys


''' Changes:
-Deleted Luis F
'''
# Program generates Game with given constraints and allows user to move randomly placed white box with WASD

# Game is a class that inherits Tkinter Frame. It not only implements the GUI, but as of now handles game mechanics
class Game(tk.Frame):
    # The following function is the Game Class constructor. It overloads the constructor for the Tkinter Frame
    # self is a reference to the particular instance of Game
    # parent is the parent, or "root", that the Game will be placed on
    # *args is a dictionary, or list, representing the non-keyworded arguments passed into Game
    # **kwargs is a dictionary, or list, representing the keyworded arguments passed into Game
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)  # Initializes Game as a frame
        self.place(x=0, y=0)
        self.parent = parent  # local instance of Game parameter parent
        self.moveXDot = 0  # Integer that represents relative horizontal movement
        self.moveYDot = 0  # Integer that represents relative vertical movement
        self.pixelsize = 50
        if 'height' in kwargs and 'width' in kwargs:
            self.pixelsWide = kwargs.get('width')//self.pixelsize  # How wide the board is. Default size of each is set to 50
            # int(value) effectively works as floor(value) for our needs. We do not deal with negative numbers, ...
            # ...so truncation is fine
            self.pixelsHigh = kwargs.get('height')//self.pixelsize  # How tall the board is. Default size of each is set to 50
        # else: fixme throw error if width or height are non existent or invalid(maybe before frame initialization)
        self.xDot = randint(0, self.pixelsWide-1)  # Represents random initial horizontal location of moving box for now
        self.yDot = randint(0, self.pixelsHigh-1)  # Represents random initial vertical location of moving box for now
        self.pixels = []  # Array of Tkinter Labels that represent the individual pixels/tiles/spots/boxes
        for x in range(self.pixelsWide):
            self.pixels.append([])
            for y in range(self.pixelsHigh):
                self.pixels[x].append(tk.Label(self, borderwidth="2", relief="groove", background='black'))
                self.pixels[x][y].place(x=x*self.pixelsize, y=y*self.pixelsize, height=self.pixelsize, width=self.pixelsize)
        self.pixels[self.xDot][self.yDot].configure(background='white')

    # The following function sets the relative movement parameters for right movement of the moving box
    def moveRight(self, event):
        if self.moveXDot == 0: # Blocks the snake from doing 180 degree turns
            self.moveXDot = 1
            self.moveYDot = 0

    # The following function sets the relative movement parameters for for left movement the moving box
    def moveLeft(self, event):
        if self.moveXDot == 0:
            self.moveXDot = -1
            self.moveYDot = 0

    # The following function sets the relative movement parameters for for upwards movement the moving box
    def moveUp(self, event):
        if self.moveYDot == 0:
            self.moveXDot = 0
            self.moveYDot = -1

    # The following function sets the relative movement parameters for for downwards movement the moving box
    def moveDown(self, event):
        if self.moveYDot == 0:
            self.moveXDot = 0
            self.moveYDot = 1


    # The following function moves the box
    def move(self):
        xbound = self.xDot + self.moveXDot  # Represents the new horizontal position the moving box will take
        ybound = self.yDot + self.moveYDot  # Represents the new vertical position the moving box will take
        if 0 <= xbound < self.pixelsWide and 0 <= ybound < self.pixelsHigh:
            self.pixels[self.xDot][self.yDot].configure(background='black')
            self.pixels[xbound][ybound].configure(background='white')
            self.xDot += self.moveXDot
            self.yDot += self.moveYDot
      """  else:
            self.close() """

    # The following function closes the window
   """ def close(self, event):
        self.destroy()
        #sys.exit()
    def close(self):
        self.destroy()
        #sys.exit() """


def main():
    root = tk.Tk()  # The root or parent window of the game board
    GAME_WIDTH = 1000  # Represents the width in pixels of the game board and window
    GAME_HEIGHT = 1000  # Represents the height in pixels of the game board and window
    GAME_SPEED = .2  # Represents the "speed" of movement. Be warned, lower speed increases input lag as of now.
    root.geometry('{}x{}'.format(GAME_WIDTH, GAME_HEIGHT))
    root.resizable(width=False, height=False)
    root.title("Snake")
    board = Game(root, background='red',  width=GAME_WIDTH, height=GAME_HEIGHT)  # The instantiation of the Game Board
    root.bind('<Escape>', sys.exit)
    root.bind('<d>', board.moveRight)
    root.bind('<a>', board.moveLeft)
    root.bind('<w>', board.moveUp)
    root.bind('<s>', board.moveDown)
    while True:
        board.move()
        root.update()
        time.sleep(GAME_SPEED)
    root.mainloop()


if __name__ == '__main__':
    main()


