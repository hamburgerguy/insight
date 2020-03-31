import datetime
import hashlib
import math

# define hex to binary function
def hex_to_bin(ini_string):
    n = int(ini_string, 16)
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    res = bStr
    return res

#define classical grovers algorithm
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


#block class
class Block:
    #setup block variables
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    diff = 253
    target = 2**(256-diff)
    previous_hash = 0x0
    timestamp = datetime.datetime.now()

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

#display strings of values.
    def __str__(self):
        return "\nBlockHash: " + str(self.hash()[:1]) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\nTarget: " + str(self.target) + "\n--------------"

class Blockchain:

    diff = 253
    maxNonce = 2**32
    target = 2**(256-diff)

    block = Block("Genesis")
    dummy = head = block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

    def mine(self, block):
        print('this is the time before mining a block'+ str(datetime.datetime.now()))
        for n in range(self.maxNonce):
            first_element_hash = block.hash()[:1]
            print('This is the first element hash {} and back to int {}'.format(first_element_hash, int(first_element_hash,16)))
            print("This is target {}".format(self.target))
            if int(str(first_element_hash), 16) <= self.target:
                self.add(block)
                print(self.block)
                print('this is the time after mining a block' + str(datetime.datetime.now()))
                break
            else:
                print("In else statment")
                block.nonce += 1
                print(block.nonce)


blockchain = Blockchain()

for n in range(10):
    blockchain.mine(Block("Block " + str(n+1)))

while blockchain.head != None:
    print(blockchain.head)
    blockchain.head = blockchain.head.next
