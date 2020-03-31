#import libraries
import matplotlib.pyplot as plt
import numpy as np
import string
import hashlib
from math import sqrt, pi
from collections import OrderedDict
from statistics import mean

#define hex to binary conversion function
def hex_to_bin(ini_string):
    n = int(ini_string, 16)
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    res = bStr
    return res.zfill(4)

#create a function that hashes a value
def hash(n):
    h = hashlib.sha256()
    h.update(
    str(n).encode('utf-8')
    )
    return h.hexdigest()

###Define Variables###
target_algorithm = '0010'
lst = []
#set up list of nonced hash values to be iterated over
for i in range(0,30):
    lst.append(hex_to_bin(str(hash(i)[0])))
objects_grover = tuple(lst)
number = len(objects_grover)
amplitude_grover = OrderedDict.fromkeys(objects_grover, 1/sqrt(number))
oracleCall = 0
num_rounds = int((pi / 4) * sqrt(number))

###Grover's Algorithm###

#setup intial step for grovers algorithm (invert amplitudes)
amplitude_grover[target_algorithm] = amplitude_grover[target_algorithm] * -1

#print initial almplitude
print(amplitude_grover)

#take the average
average_grover = mean(amplitude_grover.values())

#print the mean
print("Mean is {}".format(average_grover))

#cycle through the values
for k, v in amplitude_grover.items():
    if k == target_algorithm:
        amplitude_grover[k] = (2 * average_grover) + abs(v)
        continue
    amplitude_grover[k] = v-(2*(v-average_grover))
    oracleCall += 1

###print outputs###

print("number of rounds are {}".format(num_rounds))


print(amplitude_grover)

#print value with amplitude over 0.5
for k,v in amplitude_grover.items():
    if v >= 0.5:
        print(k)
