import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

#Network
gamma = 0.8 #discount factor
eps = 1.25 #Chance of random action
alpha = 0.9# learning rate
numRooms = 7

inputState = tf.placeholder(tf.int32)
inputAction = tf.placeholder(tf.int32)
newQ = tf.placeholder(tf.float32)

oneHota = tf.one_hot(inputState, numRooms)
oneHotb = tf.one_hot(inputAction, numRooms)

weight1a = tf.Variable(tf.random_normal([numRooms, 40]))
weight1b = tf.Variable(tf.random_normal([numRooms, 40]))
bias1 = tf.Variable(tf.random_normal([40]))
layer1 = tf.nn.sigmoid(tf.matmul(oneHota, weight1a) + tf.matmul(oneHotb, weight1b) + bias1) 

weight2 = tf.Variable(tf.random_normal([40, 1]))
bias2 = tf.Variable(tf.random_normal([1]))
layer2 = tf.matmul(layer1, weight2) + bias2

cost = tf.reduce_sum(tf.square(newQ - layer2))
optimizer = tf.train.AdamOptimizer(0.5).minimize(cost)
init = tf.global_variables_initializer()

def choose(state):
    #Returns predicted best action for the current state
    if np.random.rand() <= eps:
        return np.random.randint(0, numRooms)
    qValues = []
    for i in range(numRooms):
        qValues.append(sess.run(layer2, feed_dict={inputState: [state], inputAction:[i]})) #Returns the Q-Values of each action
    return np.argmax(qValues)

def train(oldState, action, state, rew):
    oldQ = (1-alpha)*sess.run(layer2, feed_dict={inputState: [oldState], inputAction: [action]})# Q-value of previous action
    if state != numRooms:
        qValues = []
        for i in range(numRooms):
            qValues.append(sess.run(layer2, feed_dict={inputState: [state], inputAction:[i]})) #Returns the Q-Values of each action
    else:
        qValues = [0]

    q =  oldQ + alpha*(rew + gamma * np.max(qValues))# Updated Q-value
    sess.run(optimizer, feed_dict={inputState: [oldState], inputAction: [action], newQ: [q]}) #Trains the network

#Game
def move(state, action):
    # Tries to change the state, returns the reward value
    r = np.array([
        [-1,  0, -1, -1, -1,  0, -1],
        [ 0, -1,  0, -1, -1, -1, -1],
        [-1,  0, -1,  0, -1, -1, -1],
        [-1, -1,  0, -1,  0, -1, -1],
        [-1, -1, -1,  0, -1,  0, 10],
        [ 0, -1, -1, -1,  0, -1, -1],
        [ 0,  0,  0,  0,  0,  0,  0]])
        # Reward for each move between rooms
    if r[state, action] != -1:
        return action, r[state, action] #Changes posiiton
    return state, -1

with tf.Session() as sess:
    #Training the network
    sess.run(init)
    values = []
    for i in range(750):
        x = 0
        pos = np.random.randint(0, numRooms-1)
        while pos != numRooms-1:
            x += 1
            oldPos = pos
            act = choose(pos)
            pos, reward = move(pos, act)
            train(oldPos, act, pos, reward)
        values.append(x)
        x = 0

        if i % 50 == 0:
            eps *= 0.8
            print(i)

    #Testing the Network

    print('Test')
    eps = 0
    for i in range(numRooms-1):
        print('In room ', i, 'The AI would choose ', choose(i))
print()
plt.plot(values)
plt.show()
