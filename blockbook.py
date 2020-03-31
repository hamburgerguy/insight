import json
from hashlib import sha256
import time
import datetime
import requests
from flask import render_template, redirect, Flask, request



class Block:
    def __init__(self,index,transactions,timestamp,previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(block):
        block_string = json.dumps(block.__dict__ , sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    difficulty = 2

    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0,[],time.time(),"0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self,block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0'*blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self,block,proof):
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block,proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self,block,block_hash):
        """check if block_hash is valid"""
        return (block_hash.startswith('0'*Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def add_new_transaction(self,transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index = last_block.index + 1,
                          transactions = self.unconfirmed_transactions,
                          timestamp = time.time(),
                          previous_hash = last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block,proof)
        self.unconfirmed_transactions = []
        return new_block.index

    def check_chain_validity(cls, chain):
        """helper method to check if blockchain is valid """
        result = True
        previous_hash = "0"

        #iterate through each block
        for block in chain:
            block_hash = block.hash
            delattr(block,"hash")

            if not cls.is_valid_proof(block,block.hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break
            block.hash, previous_hash = block_hash, block_hash
        return result
#code from here
def consensus():
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)

    for node in peers:
        response = requests.get('{}/chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.check_chain_validity(chain):
            #if a longer chain is found
            current_len = length
            longest_chain = chain

        if longest_chain:
            blockchain = longest_chain
            return True
        return False







###Flask code###

#init flask
app = Flask(__name__)

blockchain = Blockchain()

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author","content"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

        tx_data[timestamp] = time.time()

        block.add_new_transaction(tx_data)

        return "Success", 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

@app.route('/mine',methods = ['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    return "Block #{} is mined.".format(result)

@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)

peers = set()

@app.route('/register_node', methods = ['POST'])
def register_new_peers():

    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    #add node to the peer list
    peers.add(node_address)

    return get_chain()

@app.route('/register_with', methods=['POST'])
def register_with_existing_node():
    """
    Internally calls the `register_node` endpoint to
    register current node with the remote node specified in the
    request, and sync the blockchain as well with the remote node.
    """
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}

    # Make a request to register with remote node and obtain information
    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers
        # update chain and the peers
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return "Registration successful", 200
    else:
        # if something goes wrong, pass it on to the API response
        return response.content, response.status_code
@app.route('/add_block', methods =['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data['index'],
                  block_data['transactions'],
                  block_data['timestamp'],
                  block_data['previous_hash'])
    proof = block_data['hash']
    added = blockchain.add_block(block,proof)

    if not added:
        return 'the block was discarded by the node', 400
    return 'Block added to chain', 201

def announce_new_block(block):
    for peer in peers:
        url = "{}add_block".format(peer)
        requests.post(url, data = json.dumps(block.__dict__, sort_keys=True))
from app import app

@app.route('/mine',methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    else:
        chain_length = len(blockchain.chain)
        consensus()
        if chain_length == len(blockchain.chain):
            announce_new_block(blockchain.last_block)
        return "Block #{} is mined.".format(blockchain.last_block.index)



def create_chain_from_dump(chain_dump):
    blockchain = Blockchain()
    for idx, block_data in enumerate(chain_dump):
        block = Block(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"])
        proof = block_data['hash']
        if idx > 0:
            added = blockchain.add_block(block, proof)
            if not added:
                raise Exception("The chain dump is tampered!!")
        else:  # the block is a genesis block, no verification needed
            blockchain.chain.append(block)
    return blockchain


CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []

def fetch_posts():
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)
        global posts
        posts = sorted(content,
                       key = lambda k: k['timestamp'],
                       reverse = True)

@app.route('\submit', methods = ['POST'])
def submit_textarea():

    post_content = request.form["content"]
    author = request.form["author"]

    post_object = {
        'author': author,
        'content': post_content,
    }

    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json = post_object,
                  headers = {'Content-type': 'application/json'})
    return redirect('/')
