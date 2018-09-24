import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import maze

#Parameters
gamma = 0.8 # Discount factor - Tells the network how much it should prioritize future rewards
alpha = 0.9 # Learning rate - Tells the network how fast it should learn
epochs = 5000 # Number of epochs
layerSize = 75 # size of the hidden layers
dims = 4 # Size of the maze
changingMaze = False # The maze layout changes each time
changingGoal = True # The osition of the goal changes each time. If changing maze is on, it has no effect
lr = 0.012 # Optimizer learning rate. If it's too high or low it will not learn well
decay = 0.93 # Decay of random probability. Higher decay reduces the probabilites slower 
maxTurns = 200 #Number of turns before the run gets aborted

board = maze.Maze(dims)
print(board.mazeState().reshape(3,dims,dims))

def choose(board, eps):
    #Uses the network to choose an action and has a chance of doing a random action
    a = np.random.rand()
    if a < eps:
        opt = np.random.randint(0,4)
    else:
        opt = np.argmax(sess.run(layerFinal, feed_dict={inputState:[board]}))
    return opt

#Neural Network
inputState = tf.placeholder(tf.float32, shape=[None,3*dims**2])
newQ = tf.placeholder(tf.float32, shape=[None, 4])

weight1 = tf.Variable(tf.random_normal([3*dims**2, layerSize]))
bias1 = tf.Variable(tf.random_normal([layerSize]))
layer1 = tf.nn.elu(tf.matmul(inputState, weight1) + bias1)

weight2 = tf.Variable(tf.random_normal([layerSize, layerSize]))
bias2 = tf.Variable(tf.random_normal([layerSize]))
layer2 = tf.nn.elu(tf.matmul(layer1, weight2) + bias2)

weightFinal = tf.Variable(tf.random_normal([layerSize, 4]))
biasFinal = tf.Variable(tf.random_normal([4]))
layerFinal = tf.matmul(layer2, weightFinal) + biasFinal

cost = tf.reduce_sum(tf.square(newQ - layerFinal))
optimizer = tf.train.AdamOptimizer(lr).minimize(cost)
init = tf.global_variables_initializer()

#Training the network
with tf.Session() as sess:
    sess.run(init)
    eps = 1 # Chance of random Action
    time = []
   
    for i in range(epochs):
        data = np.array([[]])
        n = 0
        while board.isWin() == False: # Run loop until reaching the goal
            if n == maxTurns: # If player does too many steps then end simulation
                break
            oldState = board.mazeState()
            action = choose(oldState, eps)
            reward = board.move(action)
            data = np.append(data, [[oldState, board.mazeState(), reward, action]], axis=1)
            # Adds new row of data
            # Each row has the previous position, the new position, the instant reward and the action performed
            n += 1
        time.append(n)
        if changingMaze == False:
            board.reset(changingGoal)
        else:
            board = maze.Maze(dims)

        if i % 50 == 0: # Checkpoints for debugging
            print('Epoch: ',i)
            print('Probability of random action:', eps)
            print()
            eps *= decay
        
        inputData = np.array([i[0] for i in data])
        q = sess.run(layerFinal, feed_dict={inputState:inputData})
        
        for j in range(len(q)):
            # Combines the old Q-values with new information
            q2 = sess.run(layerFinal, feed_dict={inputState:[data[j,1]]})
            q[j,data[j,3]] = (1-alpha)*q[j,data[j,3]] + alpha*(data[j,2]+gamma*np.max(q2))
        sess.run(optimizer, feed_dict={inputState:inputData, newQ:q})


    #Evaluation runs to check AI's progress
    for i in range(3):
        if changingMaze == False:
            board.reset(changingGoal)
        else:
            board = maze.Maze(dims)
        print('Starting position:\n')
        board.printMaze()

        while board.isWin() == False: 
            if n == 20: 
                print('Game aborted.The AI did not finish on time')
                break
            action = choose(board.mazeState(), eps)
            print('The AI decides to move',{0:'up', 1:'right', 2:'down',3:'left'}[action])
            board.move(action)
            print('New position:\n')
            board.printMaze()
            n += 1
            if board.isWin():
                print('The AI has reached the goal')
        print('\n\n')

#Plots the time it takes to complete the maze
time.append(n)
plt.plot(time) 
plt.title('Time to complete maze')
plt.xlabel('Epoch')
plt.ylabel('Moves to finish')
plt.show()

