from random import randint
from collections import OrderedDict

'''
probability(X, 20, Y, 10, Z, 70)
'''

def random_with_prob(*args):

    if len(args) == 0:
        return None
    
    if len(args) == 1:
        args = args[0]

    if len(args)%2 == 1:
        return None


    probabilty_pairs = []

    for i in range(len(args)//2):
        probabilty_pairs.append([args[i*2+1], args[i*2]])

    probabilty_pairs = sorted(probabilty_pairs, key=lambda x: x[0])

    for i in range(1, len(probabilty_pairs)):
        probabilty_pairs[i][0] += probabilty_pairs[i-1][0]

    x = randint(0, probabilty_pairs[-1][0]-1)

    for pair in probabilty_pairs:
        if x < pair[0]:
            return pair[1]

    return None