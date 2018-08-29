from core.database import Database
from core.transaction import Transaction
from core.block import Block
from core.genesis import Genesis
from config import config
import plyvel
import json
import time
import pickle
import random
import string
import requests
from collections import defaultdict
from crypto.basic import *
sys.path.append('trie')
from db import DB as db 
genesisBlock = Genesis.genesis()
firstTransaction = genesisBlock['transaction'][0]
#print(firstTransaction["to"], firstTransaction["out"])
config = config.config()
#balanceDB = db.DB("trie/balanceDB")
#configDB = db.DB("trie/configDB")
def deleteAll(db):
    for key, value in db:
        db.delete(key)

def clearAllDB(db):
	for key in db:
		if key != "pt":
			deleteAll(db[key])
	"""
	db["blockDB"].deleteAll()
	db["transacionDB"].deleteAll()
	db["rootDB"].deleteAll()
	db["balanceDB"].deleteAll()
	db["configDB"].deleteAll()
	"""
def init_account(db, keys):
	for key in keys:
		addr = key["address"]
		account = {"address": addr, "balance":defaultdict(int), "nonce":0, "transactions":[]}
		account['balance']['cic'] = 5000000000000000000000000000
		account['balance']['btr'] = 5000000000000000000000000000
		db["balanceDB"].put(addr.encode(), pickle.dumps(account))

	mikeAccount = {"address":'cx8e954b8209951c23b7d92bf91acb7a4ea582faaa', "balance":defaultdict(int), "nonce":0, "transactions":[]}
	mikeAccount['balance']['cic'] = 5000000000000000000000000000
	mikeAccount['balance']['btr'] = 5000000000000000000000000000
	db["balanceDB"].put('cx8e954b8209951c23b7d92bf91acb7a4ea582faaa'.encode(), pickle.dumps(mikeAccount))
	deadAccount = {"address":"cx3a869e21b99e8259ed9f4a180729cd3d2e08c37b", "balance":defaultdict(int), "nonce":0, "transactions":[]}
	deadAccount["balance"]["cic"] = 5000000000000000000000000000
	deadAccount['balance']['btr'] = 5000000000000000000000000000
	db["balanceDB"].put("cx3a869e21b99e8259ed9f4a180729cd3d2e08c37b".encode(), pickle.dumps(deadAccount))
	genesisAccount = {"address":'cxa65cfc9af6b7daae5811836e1b49c8d2570c9387', "balance":defaultdict(int), "nonce":0, "transactions":[]}
	genesisAccount['balance']['cic'] = 5000000000000000000000000000
	genesisAccount['balance']['btr'] = 5000000000000000000000000000
	db["balanceDB"].put('cxa65cfc9af6b7daae5811836e1b49c8d2570c9387'.encode(), pickle.dumps(genesisAccount))
	feeAddr = config["feeAddress"]
	feeAccount = {"address": feeAddr, "balance":defaultdict(int), "nonce":0, "transactions":[]}
	feeAccount['balance']['cic'] = 10000000
	feeAccount['balance']['cry'] = 21000000
	db["balanceDB"].put(feeAddr.encode(), pickle.dumps(feeAccount))
	db["balanceDB"].put(config["tokenName"].encode(), pickle.dumps(['cic', 'now']))
	Database.createBlock([genesisBlock], db)

	CCRNonceKey = config["currNonceCCR"]
	beginBlockNum = config["currBTCRelayBlock"]
	db["configDB"].put(CCRNonceKey.encode(), pickle.dumps(0))
	db["configDB"].put(beginBlockNum.encode(), pickle.dumps(536724))
#key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(38))


#print(key)
def init_transaction(db, keys):
	feeAddr = config["feeAddress"]
	key = "97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a"
	key2 = "ec8a6f7b268804bc2bd5b3af390e7ae1eb244b54511ee6bf4f1e86d1f05aaeac"
	t = time.time()
	for i in range(1):
		print(time.time()-t)
		transactions = []
		transaction = {}
		transaction['fee'] = '10'
		transaction['to'] = 'cx' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(38))
		transaction['out'] = {'cic':str(random.randint(10,20))}
		transaction['nonce'] = str(i)#str(i+1)
		transaction['type'] = 'cic'
		transaction['input'] = ''

		for k in keys:
			newtransaction = Transaction.newTransaction(transaction, k["privateKey"])
			#print("new:", db["pt"][0])
			flag = Database.pendingTransaction(newtransaction, db)	
			#print("newtran:", newtransaction)
		
		#print(transaction['txid'])
		#transactions.append(transaction)
		#print("$+++++++++++++++++",transaction)
		
			if not flag:
				print("Pending Something wrong!")
		#print("-----------------------------------------")
		#print("pt:",db["pt"])
		"""
		data = {'method':'sendTransaction', 'param':[transaction]}
		headers = {'Content-Type':'application/json'}
		r = requests.post('http://127.0.0.1:9000', headers = headers, data = json.dumps(data))
		#print(r.text)
		"""
	
	#newKey = '975c778b9d3cb2f40539dea7a5b75ee6973f72bf46ec83130b0255cb467879aa'
	feeKey = '4f269e92bde3b00f9b963d665630445b297e2e8d29987b1d50d1e8785372e393'
	transaction = {
		'fee': '100',
		'to': feeAddr,
		'out': {'cic':'1000'},
		'nonce': '0',
		'type': 'btcc',
		'input': '90f4btr2100000000000000'
	}

	transaction = Transaction.newTransaction(transaction, feeKey)
	#print("+++++++++++++++++++",transaction)
	flag = Database.pendingTransaction(transaction, db)
	if not flag:
		print("Something wrong!")
	"""
	data = {'method':'sendTransaction', 'param':[transaction]}
	headers = {'Content-Type':'application/json'}
	r = requests.post('http://127.0.0.1:9000', headers = headers, data = json.dumps(data))
	#print(r.text)
	
	print((time.time()-t))
	"""
def main(db):
	print("Clear All")
	clearAllDB(db)
	print("Init Account")
	init_account(db, keys)
	print("Init Transaction")
	init_transaction(db, keys)

if __name__ == "__main__":
	#con = config()
	blockDB = plyvel.DB(config["blockDB"], create_if_missing=True)
	transactionDB = plyvel.DB(config["transactionDB"], create_if_missing=True)
	rootDB = plyvel.DB(config["rootDB"], create_if_missing=True)
	balanceDB = plyvel.DB(config["balanceDB"], create_if_missing=True)
	configDB = plyvel.DB(config["configDB"], create_if_missing=True)      
	top = {
            "blockDB":blockDB,
            "transactionDB":transactionDB,
            "rootDB":rootDB,
            "balanceDB":balanceDB,
            "configDB":configDB  
          }
	keys = [{			
	"privateKey": "3cbf4081d2763b0dd6172e4ebb4bf6b03c3b51523c22d07a59f014019de81c83",
	"address": "cx561de3cfa60c756afc906d0e2c5dcce6481ed159"
	},{
	"privateKey": "53c4993d30203571f4907eaa4fbfac90592ccefed9857375075348a54505211f",
	"address": "cxf25a5021ad72515676e77278264ed4f3ff1a958d"
	},{
	"privateKey": "43ac845b27aa04265b998adcef2cacf2f0392e356d059500695a4b40821b60a2",
	"address": "cxa92f918d66be8c7d496f5146251a4cfd001a3741"
	},{
	"privateKey": "ade9aacc69f1a944dbd8338791dbc8552929ec114d43856583e01d2b31b41a2f",
	"address": "cx1d56b7e828f47be684961ae1fe8a9d07354da50d"
	},{
	"privateKey": "507a6b202be4da03e2b314b2a1c5d25538908ba61f7b1f97137a1e430d89ab2c",
	"address": "cxcd94d4c80ddd18754f6980f26ad5544a8dbbc0df"
	},{
	"privateKey": "81aeb84a369a5ced9c7e338fdb252018e0009f0c13b5bf8ba730c9d9660de5d5",
	"address": "cx04c25cac9ad3fcc94731e5e1ecaf89a028cb9a1a"
	},{
	"privateKey": "1ffce4a2fbad30e368f9684cab246a4f4c9bad6f0e6694d0dedcd7d923082e46",
	"address": "cxc1eb0eab697593b200cc5e1833af08e7d131da4d"
	},{
	"privateKey": "99aa83e1397378e43f82b676d52e32eafdfa12c21b57dfeb9c62dde2b2e75092",
	"address": "cx7fce5d1593f96a01eb9cdd7b169beab90310953d"
	},{
	"privateKey": "bd1f34860ee8c592b5a2f5ac519b22ac3ba6b350b856a1cf3f3ea725aaf4cb40",
	"address": "cxeb230c487b281c32633d91ebee92ae6dd2ba6304"
	},{
	"privateKey": "4663a96cb6e05a81b450bfadaa69b3a6be5c5f3388969bee9e8707f98bc45f4a",
	"address": "cx85859a89e0e0fb072ea62411c5ae2e052239aa31"
	},{
	"privateKey": "d236fc4628ef506718990063e6ef06721dde44fa05efe78aedf51702b7e25ef0",
	"address": "cx1dd0730ff63e7fc72407a2b364ca8bee403f455f"
	},{
	"privateKey": "b4f698d3c5ca0aa48a8d4e1a96158cfe5594793e482d8e936e2b5fd61de21088",
	"address": "cx821c17d7c2942218e0d7a931d0205fe0414a1872"
	}]
	main(top, keys)

"""
{'privateKey': '8c1eba13a46fd0e18ee22e5e3da7cf139977090040622a83', 'version': '1', 
'address': 'cx6e3d4550ef058740705ebc7fcf392379c72f11fc', 'type': 'cic', 
'publicKey': 'bbc60d5af15a41d01323a22e43bbdcd1b2045b6d931c877cef8dd2153fdf4617b4839ad71e083da8d6dae8b0aff0c058'}
"""


