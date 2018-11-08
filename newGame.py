from random import randint
import numpy as np

class Game:
    '''Class that contains the game and produces data for training'''
    def __init__(self, boardSize, maxMoves):
        '''Game initializer'''
        self.boardSize = boardSize # Size of the board
        self.maxMoves = maxMoves # Number of 'idle' moves allowed before losing
        self.bodyList = [] # List containing the coordinates of every part of the snake
        
    def makeMove(self, move):
        '''Recieves a move, plays it, and returns the reward of that move
        The format of the moves is: 0:turn left, 1:go straight, 2:turn right'''
        pass
    def machinePrint(self):
        '''Prints a numerical representation of the board'''
        pass
    def humanPrint(self):
        '''Prints a human readable respresentation of the board'''
        pass
    def playGame(self):
        '''Function that runs the game'''
        pass

class Buffer:
    '''Class that stores the states, actions, and rewards of the game''' 
    pass
    