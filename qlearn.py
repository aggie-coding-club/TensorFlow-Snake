import numpy
from random import randint
q = numpy.zeros((6, 6))
gamma = 0.8
r = numpy.matrix('-1,-1,-1, -1, 0, -1; -1, -1, -1, 0, -1, 100;'
                 '-1, -1, -1, 0, -1, -1; -1, 0, 0, -1, 0, -1;'
                 '0, -1, -1, 0, -1, 100; -1, 0, -1, -1, 0, 100')
print(r)

for i in range(0,1000):
    state = randint(0, 5)
    print(state) # Which room the program starts in; doesn't matter.
    # For whichever row we're in, find which actions are viable (i.e. are any
    # value except -1. Choose a random one.
    action = randint(0, 5)
    while (r[state, action] == -1):
        action = randint(0, 5)
    print(action)
    nextstate = action

    # Pretend we're in the room we just calculated. What are the options from
    # this room? Now use the formula
    q[state,action]=r[state,action] + gamma* max(q[nextstate,:])
    print(q)

print(q/500)
