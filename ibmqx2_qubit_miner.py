#import libraries
import datetime
import operator
import hashlib
import math
from math import sqrt, pi
from collections import OrderedDict
from statistics import mean
from qiskit import IBMQ, BasicAer, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#instantiate variables
ibmqx2_result_answer = {'1001': 523, '1100': 263, '0101': 439, '0110': 562, '0001': 677, '0010': 493, '1010': 458, '1011': 469, '0111': 759, '1000': 535, '0011': 591, '1110': 469, '1111': 554, '0100': 374, '1101': 341, '0000': 685}

#define 4 qubit grover function
def q_grover(Oracle):
    #define variables
    pi = math.pi
    qr = QuantumRegister(4)
    cr = ClassicalRegister(4)
    qc = QuantumCircuit(qr, cr)

    ######## init 4 qubits #########
    qc.h(qr[0])
    qc.h(qr[1])
    qc.h(qr[2])
    qc.h(qr[3])

    ### Oracle for 0000 ###
    if Oracle == 0:
        qc.x(qr[0])
        qc.x(qr[1])
        qc.x(qr[2])
        qc.x(qr[3])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[0])
        qc.x(qr[1])
        qc.x(qr[2])
        qc.x(qr[3])

    ### Oracle for 0001 ###
    elif Oracle == 1:
        qc.x(qr[1])
        qc.x(qr[2])
        qc.x(qr[3])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[1])
        qc.x(qr[2])
        qc.x(qr[3])

    ### Oracle for 0010 ###
    elif Oracle == 2:
        qc.x(qr[0])
        qc.x(qr[2])
        qc.x(qr[3])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[0])
        qc.x(qr[2])
        qc.x(qr[3])

    ### Oracle for 0011 ###
    elif Oracle == 3:
        qc.x(qr[2])
        qc.x(qr[3])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[2])
        qc.x(qr[3])

    ### Oracle for 0100 ###
    elif Oracle == 4:
        qc.x(qr[0])
        qc.x(qr[1])
        qc.x(qr[3])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[0])
        qc.x(qr[1])
        qc.x(qr[3])

    ### Oracle for 0101 ###
    elif Oracle == 5:
        qc.x(qr[1])
        qc.x(qr[3])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[1])
        qc.x(qr[3])

    ### Oracle for 0110 ###
    elif Oracle == 6:
        qc.x(qr[0])
        qc.x(qr[3])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[0])
        qc.x(qr[3])

    ### Oracle for 0111 ###
    elif Oracle == 7:
        qc.x(qr[3])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[3])

    ### Oracle for 1000 ###
    elif Oracle == 8:
        qc.x(qr[0])
        qc.x(qr[1])
        qc.x(qr[2])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[0])
        qc.x(qr[1])
        qc.x(qr[2])

    ### Oracle for 1001 ###
    elif Oracle == 9:
        qc.x(qr[1])
        qc.x(qr[2])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[1])
        qc.x(qr[2])

    ### Oracle for 1010 ###
    elif Oracle == 10:
        qc.x(qr[0])
        qc.x(qr[2])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[0])
        qc.x(qr[2])

    ### Oracle for 1011 ###
    elif Oracle == 11:
        qc.x(qr[2])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[2])

    ### Oracle for 1100 ###
    elif Oracle == 12:
        qc.x(qr[0])
        qc.x(qr[1])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[0])
        qc.x(qr[1])

    ### Oracle for 1101 ###
    elif Oracle == 13:
        qc.x(qr[1])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[1])

    ### Oracle for 1110 ###
    elif Oracle == 14:
        qc.x(qr[0])

        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

        qc.x(qr[0])


    ### Oracle for 1111 ###
    elif Oracle == 15:
        qc.cu1(pi/4, qr[0], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(-pi/4, qr[1], qr[3])
        qc.cx(qr[0], qr[1])
        qc.cu1(pi/4, qr[1], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])
        qc.cx(qr[1], qr[2])
        qc.cu1(-pi/4, qr[2], qr[3])
        qc.cx(qr[0], qr[2])
        qc.cu1(pi/4, qr[2], qr[3])

    else:
        print('Nonce value falls outside of range of quantum circuit')
        return None

    #### Amplification ####
    qc.h(qr[0])
    qc.h(qr[1])
    qc.h(qr[2])
    qc.h(qr[3])
    qc.x(qr[0])
    qc.x(qr[1])
    qc.x(qr[2])
    qc.x(qr[3])

    ####### cccZ #########
    qc.cu1(pi/4, qr[0], qr[3])
    qc.cx(qr[0], qr[1])
    qc.cu1(-pi/4, qr[1], qr[3])
    qc.cx(qr[0], qr[1])
    qc.cu1(pi/4, qr[1], qr[3])
    qc.cx(qr[1], qr[2])
    qc.cu1(-pi/4, qr[2], qr[3])
    qc.cx(qr[0], qr[2])
    qc.cu1(pi/4, qr[2], qr[3])
    qc.cx(qr[1], qr[2])
    qc.cu1(-pi/4, qr[2], qr[3])
    qc.cx(qr[0], qr[2])
    qc.cu1(pi/4, qr[2], qr[3])

    ####### end cccZ #######
    qc.x(qr[0])
    qc.x(qr[1])
    qc.x(qr[2])
    qc.x(qr[3])
    qc.h(qr[0])
    qc.h(qr[1])
    qc.h(qr[2])
    qc.h(qr[3])

    ####### Barrier & Measures ########
    qc.barrier(qr)
    qc.measure(qr[0], cr[0])
    qc.measure(qr[1], cr[1])
    qc.measure(qr[2], cr[2])
    qc.measure(qr[3], cr[3])
    qc.measure(qr,cr)

    backend_sim = Aer.get_backend('statevector_simulator')
    job_sim = execute(qc, backend_sim)


    # Results
    statevec = job_sim.result().get_statevector()
    backend = BasicAer.get_backend('qasm_simulator')
    shots = 8192
    results = execute(qc, backend=backend, shots=shots).result()
    answer = results.get_counts()
    final = (max(answer.items(),key=operator.itemgetter(1))[0:2])

    plot_histogram(answer)
    plt.show()


    return final[0]


input = (max(ibmqx2_result_answer.items(), key = operator.itemgetter(1))[0:2])


#Hex to bin function
def hex_to_bin(ini_string):
    n = int(ini_string, 16)
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    res = bStr
    return res.zfill(4)

#Instantiate the Block class
class Block:
    #setup block variables
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    diff = 255
    target = 2**(256-diff)
    previous_hash = 0x0

    #initialize object, declare data variable
    def __init__(self, data):
        self.data = 63939098953915

    #utilize hashlib library, encode block values.
    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.blockNo).encode('utf-8')+
        str(self.target).encode('utf-8')
        )
        return h.hexdigest()

#Instantiate the blockchain class
class Blockchain:

    #define blockchain variables
    diff = 255
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

    def q_mine(self, block):
        for n in range(self.maxNonce):
            first_element_hash = block.hash()[:1]
            block.nonce = int(input[0],2)
            if int(str(first_element_hash), 16) == self.target:
                self.add(block)
                hashstr = "\nMining with qubits: " + "\nBlockHash: " + str(hex_to_bin(str(first_element_hash))) + "\nBlockNo: " + str(block.blockNo) + \
                          "\nBlock Data: "+ str(block.data) + "\nHashes: " + str(2) + "\nTarget: " + \
                          str(hex_to_bin(str(Block.target))) + "\n--------------"
                print(hashstr)
                break
    def c_mine(self,block):
        for n in range(self.maxNonce):
            first_element_hash = block.hash()[:1]
            if int(str(first_element_hash),16) == self.target:
                self.add(block)
                hashstr = "\nMining on a classical computer: " + "\nBlockHash: " + str(hex_to_bin(str(first_element_hash))) + "\nBlockNo: " + str(1) + \
                          "\nBlock Data: "+ str(block.data) + "\nHashes: " + str(block.nonce) + "\nTarget: " + \
                          str(hex_to_bin(str(Block.target))) + "\n--------------"
                print(hashstr)
                break
            else:
                block.nonce += 1


blockchain = Blockchain()

for n in range(1):
    blockchain.q_mine(Block("Block " + str(n+1)))

for n in range(1):
    blockchain.c_mine(Block("Block " + str(n+1)))

plot_histogram(ibmqx2_result_answer)
plt.show()
