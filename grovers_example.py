import matplotlib.pyplot as plt
import numpy as np
import string
import hashlib
from math import sqrt, pi
from collections import OrderedDict
from statistics import mean


def ShowGraph(amplitude_value, n):
    y_position = np.arange(n)
    plt.bar(y_position, amplitude_value.values(), align='center', color='g')
    plt.xticks(y_position, amplitude_value.keys())
    plt.ylabel('Amplitude Value')
    plt.title('Grovers Algorithm')
    plt.show()

def GetOracle(xvalue):
    return hashlib.sha256(bytes(xvalue, 'utf-8')).hexdigest()

def ExecuteGrover(target, objects, nvalue, rounds, oracleCount):
    y_pos = np.arange(nvalue)
    amplitude = OrderedDict.fromkeys(objects, 1/sqrt(nvalue))
    for i in range(0, rounds, 2):
        for k, v in amplitude.items():
            if GetOracle(k) == target:
                amplitude[k] = v * -1
                oracleCount += 1
        average = mean(amplitude.values())
        for k, v in amplitude.items():
            if GetOracle(k) == target:
                amplitude[k] = (2 * average) + abs(v)
                oracleCount += 1
                continue
            amplitude[k] = v-(2*(v-average))
    print("number of calls to oracle: " + str(oracleCount))
    return amplitude

target_algorithm = '0010'
objects_grover = ('1111', '1011', '1010', '0101', '0110', '1111', '0010')
number = len(objects_grover)
amplitude_grover = OrderedDict.fromkeys(objects_grover, 1/sqrt(number))

amplitude_grover[target_algorithm] = amplitude_grover[target_algorithm] * -1
print(amplitude_grover)
average_grover = mean(amplitude_grover.values())
print("Mean is {}".format(average_grover))
for k, v in amplitude_grover.items():
    if k == target_algorithm:
        amplitude_grover[k] = (2 * average_grover) + abs(v)
        continue
    amplitude_grover[k] = v-(2*(v-average_grover))
print(amplitude_grover)


lst = ['0100', '1101', '1110', '0100', '1101', '0111', '0001', '0110', '0101', '1011', '1111', '1011', '1010', '0101', '0110', '1111', '0010','10101','01101','10102','1010101','101010','101010101','11111','1234','9876']
needle_value = "5e7b571a60a7c187d6a4cb8bbedbe4e69d4caa49b51d9ddf3320afd793f146bf"
haystack_value = lst
num_rounds = int((pi / 4) * sqrt(num))
print("number of rounds are {}".format(num_rounds))
ShowGraph(ExecuteGrover(needle_value, haystack_value, num, num_rounds,0), num)
