import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

#Maze map
board = np.array([ 
    [0,    0,    0,    0, 0],
    [0,    0, 1000, -100, 0],
    [0, -100,    0, -100, 0],
    [0, -100,    0,    0, 0],
    [0,    0,    0,    0, 0]])

def move(board, position, action): 
    # Moves the player
    # Returns: New position, instant reward
    # Position: current (y,x) coordinates. Top left corner is (0,0)
    # Actions: 0-up, 1-right 2-down, 3-left
    # 0's are floor tiles, -100's are wall tiles, and 100 is the goal
    
    if action == 0:
        newpos = (position[0]-1, position[1])
    elif action == 1:
        newpos = (position[0], position[1]+1)
    elif action == 2:
        newpos = (position[0]+1, position[1])
    elif action == 3:
        newpos = (position[0], position[1]-1)
    
    if (0 <= newpos[0] <= 4) and (0 <= newpos[1] <= 4):
        reward = board[newpos]
    else: 
        # Moving out of bounds
        reward = -100

    if reward == -100: # Invalid move
        newpos = position
    return newpos, reward

def formatData(data): 
    for i in range(len(data)):
        # Combines the ordered pairs of the position into a single number
        data[i,0] = 5*data[i,0][0] + data[i,0][1]
        data[i,1] = 5*data[i,1][0] + data[i,1][1]
    return data

def choose(pos, eps):
    #Uses the network to choose an ction and has a chance of doing a random action
    a = np.random.rand()
    p = 5*pos[0] + pos[1]
    if a < eps:
        opt = np.random.randint(0,4)
    else:
        opt = np.argmax(sess.run(layerFinal, feed_dict={inputState:[p]}))
    return opt

gamma = 0.9 # Discount factor - Tells the network how much it should prioritize future rewards
alpha = 0.8 # Learning rate - Tells the network how fast it should learn

#Neural Network
inputState = tf.placeholder(tf.int32)
newQ = tf.placeholder(tf.float32)

oneHot = tf.one_hot(inputState, 25)

weight1 = tf.Variable(tf.random_normal([25, 50]))
bias1 = tf.Variable(tf.random_normal([50]))
layer1 = tf.nn.sigmoid(tf.matmul(oneHot, weight1) + bias1)

weight2 = tf.Variable(tf.random_normal([50, 50]))
bias2 = tf.Variable(tf.random_normal([50]))
layer2 = tf.nn.sigmoid(tf.matmul(layer1, weight2) + bias2)

weightFinal = tf.Variable(tf.random_normal([50, 4]))
biasFinal = tf.Variable(tf.random_normal([4]))
layerFinal = tf.matmul(layer2, weightFinal) + biasFinal

cost = tf.reduce_sum(tf.square(newQ - layerFinal))
optimizer = tf.train.AdamOptimizer(0.05).minimize(cost)
init = tf.global_variables_initializer()

#Training the network
with tf.Session() as sess:
    sess.run(init)
    eps = 1 # Chance of random Action
    t = []
    for i in range(1000):
        n = 0
        data = []
        # Random starting position
        pos = (np.random.randint(0,5), np.random.randint(0,5))
        while board[pos] != 0:
            pos = (np.random.randint(0,5), np.random.randint(0,5))
        
        while board[pos] != 1000: # Run loop until reaching the goal
            if n == 200: # If player does too many steps then end simulation
                break
            action = choose(pos, eps)
            newpos, rew = move(board, pos, action)
            data.append([pos, newpos, rew, action])
            # Adds new row of data
            # Each row has the previous position, the new position, the instant reward and the action performed
            pos = newpos
            n += 1
        t.append(n)
        data = formatData(np.array(data))

        if i % 100 == 0: # Checkpoints for debugging
            print('Epoch: ',i)
            print('eps', eps)
            eps *= 0.73
        
        q = sess.run(layerFinal, feed_dict={inputState:data[:,0]})
        for i in range(len(q)):
            # Combines the old Q-values with new information
            q2 = sess.run(layerFinal, feed_dict={inputState:[data[i,1]]})
            q[i,data[i,3]] = (1-alpha)*q[i,data[i,3]] + alpha*(data[i,2]+gamma*np.max(q2))
        sess.run(optimizer, feed_dict={inputState:data[:,0], newQ:q})


print('Final Data:\n', data)
plt.plot(t)
plt.title('Time to complete maze')
plt.xlabel('Epoch')
plt.ylabel('Moves to finish')
plt.show()
