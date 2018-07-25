from core.database import Database
from core.transaction import Transaction
from core.block import Block
from core.genesis import Genesis
from config import config
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
config = config.config()
db = Database()

def clearAllDB():
	db.blockDB.deleteAll()
	db.transactionDB.deleteAll()
	db.rootDB.deleteAll()
	db.balanceDB.deleteAll()
	db.configDB.deleteAll()

def init_account():
	genesisAccount = {"address":'cxa65cfc9af6b7daae5811836e1b49c8d2570c9387', "balance":defaultdict(int), "nonce":0}
	genesisAccount['balance']['cic'] = 5000000000000000000000000000
	db.balanceDB.put('cxa65cfc9af6b7daae5811836e1b49c8d2570c9387'.encode(), pickle.dumps(genesisAccount))
	feeAddr = config["feeAddress"]
	feeAccount = {"address": feeAddr, "balance":defaultdict(int), "nonce":0}
	feeAccount['balance']['cic'] = 1000
	db.balanceDB.put(feeAddr.encode(), pickle.dumps(feeAccount))
	db.balanceDB.put(config["tokenName"].encode(), pickle.dumps(['cic', 'now']))
	db.createBlock(genesisBlock)

	CCRNonceKey = config["currNonceCCR"]
	beginBlockNum = config["currBTCRelayBlock"]
	db.configDB.put(CCRNonceKey.encode(), pickle.dumps(1))
	db.configDB.put(beginBlockNum.encode(), pickle.dumps(533402))
#key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(38))


#print(key)
def init_transaction():
	feeAddr = config["feeAddress"]
	key = '97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a'
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
	feeKey = '4f269e92bde3b00f9b963d665630445b297e2e8d29987b1d50d1e8785372e393'
	transaction = {
		'fee': '100',
		'to': feeAddr,
		'out': {'cic':'100'},
		'nonce': '1',
		'type': 'btc',
		'input': '90f4btr2100000000000000'
	}

	transaction = Transaction.newTransaction(transaction, feeKey)
	data = {'method':'sendTransaction', 'param':[transaction]}
	headers = {'Content-Type':'application/json'}
	r = requests.post('http://192.168.0.178:9000', headers = headers, data = json.dumps(data))
	#print(r.text)
	print((time.time()-t))
	print("test:",int(pickle.loads(db.balanceDB.get('cxa65cfc9af6b7daae5811836e1b49c8d2570c9387'.encode()))['balance']['cic']))

def main():
	clearAllDB()
	init_account()
	init_transaction()

if __name__ == "__main__":
	main()

"""
{'privateKey': '8c1eba13a46fd0e18ee22e5e3da7cf139977090040622a83', 'version': '1', 
'address': 'cx6e3d4550ef058740705ebc7fcf392379c72f11fc', 'type': 'cic', 
'publicKey': 'bbc60d5af15a41d01323a22e43bbdcd1b2045b6d931c877cef8dd2153fdf4617b4839ad71e083da8d6dae8b0aff0c058'}
"""