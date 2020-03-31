#import libraries
from __future__ import division
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
from pylab import plot, ylim, xlim, show, xlabel, ylabel, grid, legend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#declare lists for later use in indexing
classic_hash = []
quantum_hash = []

# define hex to binary function
def hex_to_bin(ini_string):
    n = int(ini_string, 16)
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    res = bStr
    return res.zfill(4)

#define classical grovers algorithm, mostly for reference
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

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


#block class
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

#blockchain class
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

    #setup up mining method that employs both grovers algorithm and the normal mining strategy
    def mine(self, block):
        lst = []
        for n in range(self.maxNonce):
            #define first element in block hash
            first_element_hash = block.hash()[0]

            #define variables for use in grovers algorithm
            lst.append(hex_to_bin(str(first_element_hash)))
            objects_grover = tuple(lst)
            number = len(objects_grover)
            amplitude_grover = OrderedDict.fromkeys(objects_grover, 1/sqrt(number))
            num_rounds = int((pi / 4) * sqrt(number))
            target_algorithm = '0010'

            #add block to blockchain or add nonce value to ledger if hash of function is equal to target
            if int(str(first_element_hash), 16) == self.target:
                self.add(block)
                classic_hash.append(str(block.nonce))
                hashstr = "\nBlockHash: " + str(hex_to_bin(str(first_element_hash))) + "\nBlockNo: " + str(block.blockNo) + \
                          "\nBlock Data: "+ str(Block.data) + "\nHashes: " + str(block.nonce) + "\nTarget: " + \
                          str(hex_to_bin(str(Block.target))) + "\n--------------"
                print(hashstr)
                ###Grover's Algorithm###

                #setup intial step for grovers algorithm (invert amplitudes)
                amplitude_grover[target_algorithm] = amplitude_grover[target_algorithm] * -1
                average_grover = mean(amplitude_grover.values())
                print("Mean is {}".format(average_grover))
                print('Number of hashes using Grovers algorithm: ' + str(num_rounds))
                #cycle through key values and run Grovers algorithm loop
                for k, v in amplitude_grover.items():
                    if k == target_algorithm:
                        amplitude_grover[k] = (2 * average_grover) + abs(v)
                        continue
                    amplitude_grover[k] = v-(2*(v-average_grover))
                #print out the nonce value found by running successive iterations of Grover's algorithm
                print(str(max(amplitude_grover.items(), key=operator.itemgetter(1))[0:2]) + "- Nonce value for this amplitude: " + str(block.nonce))
                quantum_hash.append(str(num_rounds))
                break
            else:
                block.nonce +=1



blockchain = Blockchain()

#set the number of blocks to mine
numblocks = 100

for n in range(numblocks):
    blockchain.mine(Block("Block " + str(n+1)))

#convert string values to int values
c_hash = []
q_hash = []

for i in classic_hash:
    c_hash.append(int(i))
for i in quantum_hash:
    q_hash.append(int(i))

#print the average number of hashes for each method.
av_classical = mean(c_hash)
av_quantum = mean(q_hash)

print('----------------')
print('Average number of hashes required for classical mining: ' + str(av_classical))
print('Average number of hashes required for quantum mining: '+ str(av_quantum))


x = np.arange(numblocks)


#plot running average

plot(x,c_hash)
plot(x,q_hash)
q_av = movingaverage(q_hash,100)
c_av = movingaverage(c_hash,100)
plot(x,c_av,"r",label = 'Average # of hashes required classically')
plot(x,q_av,'b',label = 'Average # of hashes required on a QC')
ylabel('hashes required')
xlabel('block number')
legend()
grid(True)
show()

'''

#############################
###4-Qubit Grovers Circuit###
#############################

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

### Oracle for 0010 ###
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

#draw circuit
#print (qc.draw())

# Execute job
backend_sim = Aer.get_backend('statevector_simulator')
job_sim = execute(qc, backend_sim)


# Results
statevec = job_sim.result().get_statevector()
print(statevec)
backend = BasicAer.get_backend('qasm_simulator')
shots = 8192
results = execute(qc, backend=backend, shots=shots).result()
answer = results.get_counts()

#Display data
plot_histogram(answer)
plt.show()

final = (max(answer.items(),key=operator.itemgetter(1))[0:2])
print(final[0])


'''
