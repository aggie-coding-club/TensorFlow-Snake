import numpy as np

class Maze:
    def __init__(self, dims):
        # Creates a new maze
        self.maze = np.ones((dims,dims))
        self.dims = dims

        tiles = [(np.random.randint(self.dims), np.random.randint(self.dims))]
        numTiles = np.random.randint((self.dims**2)//3,3*(self.dims**2)//5)
        self.maze[tiles[0]] = 0
        count = 0

        while count < numTiles:
            opt = np.random.randint(4)
            x = tiles[np.random.randint(len(tiles))]
            # 0-up, 1-right, 2-down, 3-left
            if opt == 0 and x[0] > 0:
                newTile = (x[0]-1, x[1])
            elif opt == 1 and x[1] < self.dims-1:
                newTile = (x[0], x[1]+1)
            elif opt == 2 and x[0] < self.dims-1:
                newTile = (x[0]+1, x[1])
            elif opt == 3 and x[1] > 0:
                newTile = (x[0], x[1]-1)
            else:
                continue

            if self.maze[newTile] != 0:
                tiles.append(newTile)
                self.maze[newTile] = 0
                count += 1

        self.goalPos = (np.random.randint(self.dims), np.random.randint(self.dims))
        while self.maze[self.goalPos] == 1:
            self.goalPos = (np.random.randint(self.dims), np.random.randint(self.dims))

        self.pos = (np.random.randint(self.dims), np.random.randint(self.dims))
        while self.maze[self.pos] == 1 or self.pos == self.goalPos:
            self.pos = (np.random.randint(self.dims), np.random.randint(self.dims))

    def mazeState(self):
        # Outputs a tensor containing the position of the player, the obstacles and the goal
        state = np.zeros((3,self.dims, self.dims))
        state[0] = self.maze
        state[1, self.pos[0], self.pos[1]] = 1
        state[2, self.goalPos[0], self.goalPos[1]] = 1
        return state.ravel()
    
    def printMaze(self):
        #Prints a human readable representation of the maze
        board = np.array([[' ']*self.dims]*self.dims)
        for i in range(self.dims):
            for j in range(self.dims):
                if self.maze[i,j] == 1:
                    board[i,j] = 'X'
                elif (i,j) == self.goalPos:
                    board[i,j] = 'O'
                elif (i,j) == self.pos:
                    board[i,j] = 'P'
        print(board)

    def reset(self, changeGoal=False):
        # Resets the maze
        if changeGoal ==True:
            self.goalPos = (np.random.randint(self.dims), np.random.randint(self.dims))
            while self.maze[self.goalPos] == 1:
                self.goalPos = (np.random.randint(self.dims), np.random.randint(self.dims))

        self.pos = (np.random.randint(self.dims), np.random.randint(self.dims))
        while self.maze[self.pos] == 1 or self.pos == self.goalPos:
            self.pos = (np.random.randint(self.dims), np.random.randint(self.dims))
    
    def isWin(self):
        #Checks if the player has reached the goal
        return self.pos == self.goalPos
    
    def move(self, action):
        # Moves the player
        # Returns: New position, instant reward
        # Position: current (y,x) coordinates. Top left corner is (0,0)
        # Actions: 0-up, 1-right 2-down, 3-left

        goalReward = 500 # Reward for reaching the goal
        invalidReward = -1000 # Reward for doing an invalid action

        if action == 0:
            newpos = (self.pos[0]-1, self.pos[1])
        elif action == 1:
            newpos = (self.pos[0], self.pos[1]+1)
        elif action == 2:
            newpos = (self.pos[0]+1, self.pos[1])
        elif action == 3:
            newpos = (self.pos[0], self.pos[1]-1)
        
        if (0 <= newpos[0] < self.dims) and (0 <= newpos[1] < self.dims):
            if newpos == self.goalPos:
                reward = goalReward
            elif self.maze[newpos] == 1:
                reward = invalidReward
            else:
                reward = 0
            
        else: 
            # Moving out of bounds
            reward = invalidReward

        if reward != invalidReward: 
            self.pos = newpos
        return reward