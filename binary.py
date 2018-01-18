import tensorflow as tf
import numpy as np

def binary(n,bits):
    #Given a vector of numbers, output a matrix where the Nth column is
    #the binary representation of the Nth number in the vector'''
    a = np.zeros((bits, len(n)), dtype=float)
    for j in range(len(n)):
        s = n[j]
        for i in range(bits):
            a[-i-1, j] = s%2
            s = s // 2
        
    return a.T

bit = 5 #Number of bits the numbers will have

inp = tf.placeholder(tf.int32) #Placeholder spot for input values
out = tf.placeholder(tf.float32)#Placeholder spot for expected outputs during training phase
oneHot = tf.one_hot(inp,2**bit) # One hot representation of input 
#https://en.wikipedia.org/wiki/One-hot

weight1 = tf.Variable(tf.random_normal([2**bit, 20]))# Weight Matrix
bias1 = tf.Variable(tf.random_normal([20]))#Bias Vector
layer1 = tf.nn.sigmoid(tf.matmul(oneHot, weight1) + bias1) 
#Multiplies the input matrix with the weight matrix, then adds the bias, and finally applies the sigmoid function to the result
#https://en.wikipedia.org/wiki/Sigmoid_function

weight2 = tf.Variable(tf.random_normal([20, bit]))
bias2 = tf.Variable(tf.random_normal([bit]))
layer2 = tf.nn.sigmoid(tf.matmul(layer1, weight2) + bias2)
#Same as above

cost = tf.reduce_sum(tf.square(out-layer2))
#MSE cost function. Compares expected value (out) with actual value (layer2)
#https://en.wikipedia.org/wiki/Mean_squared_error

optimizer = tf.train.AdamOptimizer(0.5).minimize(cost)
#Optimizer Algorithm: Tries to minimize the error between the expected and the actual output
#https://en.wikipedia.org/wiki/Stochastic_gradient_descent#Adam

ans = tf.round(layer2) #Rounds output for simple visualization
init = tf.global_variables_initializer() #initializer of the variables

with tf.Session() as sess:
    sess.run(init)
    for i in range(2000): #Training loop. By changing the number of iterations you can get a more trained or less trainde network
        x = np.random.randint(0,2**bit, 200) #Generates random sample of 200 numbers
        sess.run(optimizer, feed_dict={inp: x, out: binary(x, bit)})
        #Runs the optimizer

    #Prints the network output for all the numbers from 0 to 2^bits -1
    #If the network trainde properly
    test = [i for i in range(2**bit)] 
    print('Final Test:\n', sess.run(ans, feed_dict={inp: test}))