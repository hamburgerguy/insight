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
    return res.zfill(4)

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
    diff = 255
    target = 2**(256-diff)
    previous_hash = 0x0
    #timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data

    #utilize hashlib library, encode block values.
    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        #str(self.timestamp).encode('utf-8') +
        str(self.blockNo).encode('utf-8')+
        str(self.target).encode('utf-8')
        )
        return h.hexdigest()

class Blockchain:

    diff = 255
    maxNonce = 2**32
    target = 2**(256-diff)
    lst = []

    block = Block("Genesis")
    dummy = head = block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next


    def mine(self, block):
        lst = []
        for n in range(self.maxNonce):
            first_element_hash = block.hash()[0]
            lst.append(hex_to_bin(str(first_element_hash)))
            print('This is the first element hash {} and back to int {}'.format(first_element_hash, int(first_element_hash,16)))
            print("This is target {}".format(self.target))
            if int(str(first_element_hash), 16) == self.target:
                self.add(block)
                hashstr = "\nBlockHash: " + str(hex_to_bin(str(first_element_hash))) + "\nBlockNo: " + str(block.blockNo) + \
                          "\nBlock Data: "+ str(Block.data) + "\nHashes: " + str(block.nonce) + "\nTarget: " + \
                          str(hex_to_bin(str(Block.target))) + "\n--------------"
                print(hashstr)
                print(lst)
                break
            else:
                block.nonce +=1



blockchain = Blockchain()

for n in range(10):
    blockchain.mine(Block("Block " + str(n+1)))
