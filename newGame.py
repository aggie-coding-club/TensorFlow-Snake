import numpy as np


class Game:
    '''Class that contains the game and produces data for training'''
    def __init__(self, boardSize, maxMoves, startingSize, losingReward=-100, moveReward=-1, appleReward=100):
        '''Game initializer'''
        assert(startingSize <= boardSize) #check that the starting snake is not too long

        self.boardSize = boardSize # Size of the board
        self.maxMoves = maxMoves # Number of 'idle' moves allowed before losing
        self.startingSize = startingSize # Length of the starting Snake
        
        self.losingReward = losingReward # Reward value when the snake loses
        self.moveReward = moveReward # Reward value when the snake moves
        self.appleReward = appleReward # Reward value when an apple is obtained

        self.bodyList = [] # Squares occupied by the snake
        self.direction = 1 # Up:0, Right:1, Down:2, Left:3
        self.isOver = False # Whether the game is over or not
        self.moveCounter = 0 # Counter of idle moves

        self.state = np.zeros((3, boardSize, boardSize), dtype=float)
        #Representation of the board consisting of 3 layers with a boardsize x boardsize matrix
        #The zeroth layer contains a 1 if there is a snake part and 0 otherwise
        #The first layer contains a 2 in the position of the head of the snake a 1 in the prehead block and 0 otherwise
        #The second layer contains a 1 in the position of the apple and 0 otherwise

        for n in range(self.startingSize):
            self.bodyList.append((0,n))
            self.state[0, 0, n] = 1
        self.state[1, 0, startingSize-1] = 2
        self.state[1, 0, startingSize-2] = 1
        self.placeApple()

    def resetBoard(self):
        '''Sets the board to the initial state'''
        self.moveCounter = 0
        self.direction = 1
        self.state[:] = 0
        self.bodyList.clear()
        self.isOver = False

        for n in range(self.startingSize):
            self.bodyList.append((0,n))
            self.state[0, 0, n] = 1
        self.state[1, 0, self.startingSize-1] = 2
        self.state[1, 0, self.startingSize-2] = 1
        self.placeApple()

    def placeApple(self):
        '''Places an apple on the board
        It assumes that there are no apples on the board'''
        while True:
            x_apple = np.random.randint(0,self.boardSize) 
            y_apple = np.random.randint(0,self.boardSize)
            if self.state[0, y_apple, x_apple] == 0:
                self.state[2, y_apple, x_apple] = 1
                return

    def makeMove(self, move):
        '''Recieves a move, plays it, and returns the reward of that move
        The format of the moves is: 0:turn left, 1:go straight, 2:turn right'''

        prehead = self.bodyList[-2]
        head =  self.bodyList[-1]
        self.state[1][head] = 1
        self.state[1][prehead] = 0

        self.direction = (self.direction + move -1) % 4

        if self.direction == 0:
            newhead = (head[0]-1, head[1])
        elif self.direction == 1:
            newhead = (head[0], head[1]+1)
        elif self.direction == 2:
            newhead = (head[0]+1, head[1])
        elif self.direction == 3:
            newhead = (head[0], head[1]-1)

        tail = self.bodyList[0]
        self.state[0][tail] = 0

        if (0 > newhead[0]) or (newhead[0] >= self.boardSize) or (0 > newhead[1]) or (newhead[1] >= self.boardSize) or (self.state[0][newhead] == 1):
            # Checks if the snake crashed
            self.isOver = True
            return self.losingReward

        self.bodyList.append(newhead)
        self.state[0][newhead] = 1
        self.state[1][newhead] = 2

        if self.state[2][newhead] == 1:
            # Check if the snake got to an apple
            if len(self.bodyList) == self.boardSize*self.boardSize:
                # Checks if the snake has won
                self.isOver = True
                return self.appleReward

            self.moveCounter = 0
            self.state[2][newhead] = 0
            self.state[0][tail] = 1
            self.placeApple()
            return self.appleReward

        # The snake just moves
        self.moveCounter += 1
        self.bodyList.pop(0)
        return self.moveReward

    def getState(self):
        '''Returns a numerical representation of the board'''
        return np.copy(self.state.ravel())

    def printBoard(self):
        '''Prints a human readable respresentation of the board'''
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.state[1,i,j] == 2:
                    print(' H ',end='')
                elif self.state[0,i,j] == 1:
                    print(' O ',end='')
                elif self.state[2,i,j] == 1:
                    print(' A ',end='')
                else:
                    print(' _ ', end='')
            print()

    def getHumanMove(self):
        '''Gets a move from a source(human or computer) and returns it
        We will only implement a human input for now'''
        self.printBoard()
        while True:
            try:
                move = int(input("What move should we make? (0 left, 1 straight, 2 right)\n"))
                if(0 <= move <= 2):
                    return move
                print("Error: invalid move")
            except ValueError:
                print("Error: invalid move")

    def playGame(self, buffer):
        '''Function that runs the game. Returns the snake's 
        final length for statistical purposes'''

        while not self.isOver:
            oldState = self.getState()
            move = self.getHumanMove()
            reward = self.makeMove(move)

            buffer.addData(oldState, self.getState(), move, reward)
            if(self.moveCounter >= self.maxMoves):
                break
        return len(self.bodyList)

class Buffer:
    '''Class that stores the states, actions, and rewards of the game''' 
    def __init__(self, maxSize):
        self.maxSize = maxSize
        self.oldStates = []
        self.newStates = []
        self.actions = []
        self.rewards = []

    def addData(self, oldState, newState, action, reward):
        '''Adds a new data point to the buffer.
        If the buffer is full, then replaces a random element'''
        if len(self.oldStates) >= self.maxSize:
            self.replace(oldState, newState, action, reward)
        else:
            self.oldStates.append(oldState)
            self.newStates.append(newState)
            self.actions.append(action)
            self.rewards.append(reward)

    def replace(self, oldState, newState, action, reward):
        '''Replaces a random element of the buffer'''
        i = np.random.randint(0, self.maxSize)
        self.oldStates[i] = oldState
        self.newStates[i] = newState
        self.actions[i] = action
        self.rewards[i] = reward

    def clearData(self):
        self.oldStates.clear()
        self.newStates.clear()
        self.actions.clear()
        self.rewards.clear()
