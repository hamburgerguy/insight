#import libraries
import datetime
import operator
import hashlib
import math
from math import sqrt, pi
from collections import OrderedDict
from statistics import mean
from pylab import plot, ylim, xlim, show, xlabel, ylabel, grid, legend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#define lists for plotting later
c_hash = []
q_hash = []

#function for returning self values for the grover function
def GetOracle(xvalue):
    return xvalue

#Define function that runs grovers algorithm and prints out how many iterations would be required on a quantum computer
def ExecuteGrover(target, objects, nvalue, rounds,oracleCount):
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
    print("Hashes using Grover's algorithm: " + str(oracleCount))
    return amplitude



#create block class
class Block:
    #setup block variables
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    diff = 10
    target = 2**(256-diff)
    previous_hash = 0x0
    timestamp = datetime.datetime.now()

    #initialize object
    def __init__(self, data):
        self.data = data

    #utilize hashlib library, encode block values.
    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')+
        str(self.target).encode('utf-8')
        )
        return h.hexdigest()

class Blockchain:

    #define blockchain variables
    diff = 10
    maxNonce = 2**32
    target = 2**(256-diff)
    lst = []

    block = Block("Genesis")
    dummy = head = block

    #define add method to add blocks to blockchain
    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

        #setup up mining method that employs both grovers algorithm and the normal mining strategy
    def mine(self, block):
        #instantiate list variable to be used in grovers algorithm
        list = []
        #setup special use case for blocks that require no revision of nonce space
        if int(str(block.hash()),16) <= self.target:
            nohash = "\nBlockHash: " + block.hash() + "\nBlockNo: " + str(block.blockNo) + \
                      "\nBlock Data: "+ str(Block.data) + "\nHashes: " + str(block.nonce) + \
                      "\nDifficulty: " + str(block.diff) + "\n--------------"
            print(nohash)
            print('0 hashes required')
            return

        #Iterate through nonce values in order to find winning nonce
        for n in range(self.maxNonce):
            if int(str(block.hash()), 16) <= self.target:
                self.add(block)
                hashstr = "\nBlockHash: " + list[-1] + "\nBlockNo: " + str(block.blockNo) + \
                          "\nBlock Data: "+ str(Block.data) + "\nHashes: " + str(block.nonce) + \
                          '\nDifficulty: ' + str(block.diff) + "\n--------------"
                print(hashstr)
                c_hash.append(block.nonce)
                ### Grovers Algorithm ###
                length_lst = len(list)
                calls = int((pi/4)*math.sqrt(length_lst))
                q_hash.append(calls)
                #execute grovers algorithm on list of hash values, find same value classically
                grov_data = max(ExecuteGrover(min(list),list,length_lst,calls,0).items(), key=operator.itemgetter(1))
                print('BlockHash: ' + str(grov_data[0]))
                print('Corresponding amplitude: ' + str(grov_data[1]))
                print('Nonce value for this amplitude: ' + str(length_lst))
                print('_____________________________________________________________________________')
                break
            else:
                #increase nonce value by 1
                block.nonce += 1
                list.append(block.hash())

#create blockchain variable
blockchain = Blockchain()

#Mine 10 blocks on blockchain variable
blocks = 10
for n in range(blocks):
    blockchain.mine(Block("Block " + str(n+1)))

x = np.arange(blocks)

plt.scatter(x,c_hash,label = 'Hashes classically', color = 'r')
plt.scatter(x,q_hash,label = 'Hashes on a QC',color = 'b')
ylabel('Hashes required')
xlabel('Block number')
plt.legend()
#plt.show()



#counted = count_elements(q_hash)
#print(counted)
