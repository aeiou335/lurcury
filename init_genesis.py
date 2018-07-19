from core.database import Database
from core.transaction import Transaction
from core.block import Block
from core.genesis import Genesis
import json
import time
import pickle
import random
import string
import requests
from collections import defaultdict
from crypto.basic import *
genesisBlock = Genesis.genesis()
firstTransaction = genesisBlock['transaction'][0]
#print(firstTransaction["to"], firstTransaction["out"])

db = Database()
db.blockDB.deleteAll()
db.transactionDB.deleteAll()
db.rootDB.deleteAll()
db.balanceDB.deleteAll()
genesisAccount = {"address":'cxa65cfc9af6b7daae5811836e1b49c8d2570c9387', "balance":defaultdict(int), "nonce":0}
genesisAccount['balance']['cic'] = 5000000000000000000000000000
db.balanceDB.put('cxa65cfc9af6b7daae5811836e1b49c8d2570c9387'.encode(), pickle.dumps(genesisAccount))
feeAccount = {"address": "cx68c59720de07e4fdc28efab95fa04d2d1c5a2fc1", "balance":defaultdict(int), "nonce":0}
feeAccount['balance']['cic'] = 1000
db.balanceDB.put('cx68c59720de07e4fdc28efab95fa04d2d1c5a2fc1'.encode(), pickle.dumps(feeAccount))
db.balanceDB.put('name'.encode(), pickle.dumps(['cic', 'now']))
db.createBlock(genesisBlock)
print('block 0:',db.getBlockByID(0))
#key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(38))

key = '97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a'

#print(key)

t = time.time()
for i in range(9):
	transactions = []
	transaction = {}
	transaction['fee'] = '10'
	transaction['to'] = 'cx' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(38))
	transaction['out'] = {'cic':str(random.randint(10,20))}
	transaction['nonce'] = str(i+1)
	transaction['type'] = 'cic'
	transaction['input'] = ''
	transaction = Transaction.newTransaction(transaction, key)
	#print(transaction)
	
	#print(transaction['txid'])
	transactions.append(transaction)
	data = {'method':'sendTransaction', 'param':[transaction]}
	headers = {'Content-Type':'application/json'}
	r = requests.post('http://192.168.0.178:9000', headers = headers, data = json.dumps(data))
	#print(r.text)
#newKey = '975c778b9d3cb2f40539dea7a5b75ee6973f72bf46ec83130b0255cb467879aa'

transaction = {
	'fee': '100',
	'to': 'cx68c59720de07e4fdc28efab95fa04d2d1c5a2fc1',
	'out': {'cic':'100'},
	'nonce': '10',
	'type': 'cic',
	'input': '90f4god100000000'
}

transaction = Transaction.newTransaction(transaction, key)
data = {'method':'sendTransaction', 'param':[transaction]}
headers = {'Content-Type':'application/json'}
r = requests.post('http://192.168.0.178:9000', headers = headers, data = json.dumps(data))
print((time.time()-t))

"""
{'privateKey': '8c1eba13a46fd0e18ee22e5e3da7cf139977090040622a83', 'version': '1', 
'address': 'cx6e3d4550ef058740705ebc7fcf392379c72f11fc', 'type': 'cic', 
'publicKey': 'bbc60d5af15a41d01323a22e43bbdcd1b2045b6d931c877cef8dd2153fdf4617b4839ad71e083da8d6dae8b0aff0c058'}
"""