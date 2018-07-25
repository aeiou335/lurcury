import requests 
import json
import time
import pickle
import sys
from config import config
sys.path.append('trie')
import db as db
import MerklePatriciaTrie as MPT
sys.path.append('core')
from transaction import Transaction
from bitcoinRPC import *


class bitcoinInfo: 
	def pendingBTCRelay(transactions):
		transactionDB = db.DB("trie/transactionDB")
		con = config.config()
		key = con["pendingTransaction"]
		try:
			pending = pickle.loads(transactionDB.get(key.encode()))
		except:
			pending = []
		for t in transactions:
			pending.append(t)
		try:
			transactionDB.put(key.encode(), pickle.dumps(pending))
			print("pending:",pickle.loads(transactionDB.get(key.encode())))
			return True
		except:
			return False
			
	def parseTransaction(has): 
		ourAccount = "1Pi1Spap6vdfAWJPfMkYUCtG4EYM5fPWeR"
		
		#r = requests.get("https://blockexplorer.com/api/tx/"+has) 
		t = bitcoinRPC().transaction(has)
		t = json.loads(t)["result"]
		#try:
		#	t = json.loads(r.text[:1000000000])
		#except:
		#	return False, 0, ""
		#print(t)
		transactions = t['vout']
		flag = False
		value = 0
		address = ""
		for i, transaction in enumerate(transactions):
			#print(transaction)
			try:
				if transaction["scriptPubKey"]["addresses"][0] != ourAccount:
					continue
				else:
					value = transaction['value']
					flag = True
					txid = t["vin"][0]["txid"]
					out = t["vin"][0]["vout"]
					print(txid, out)
					originalt = json.loads(bitcoinRPC().transaction(txid))["result"]
					
					address = originalt["vout"][out]["scriptPubKey"]["addresses"][0]
			except:
				continue
			#elif i == len(transactions)-1 and flag:
			#	address = transaction['scriptPubKey']['asm'][10:]
		return flag, value, address

	def btcRelay(transaction):
		balanceDB = db.DB('trie/balanceDB')
		value = int(transaction['out']['cic'])
		address = transaction['to']
		try:
			account = pickle.loads(balanceDB.get(address.encode()))
		except:
			account = {'address':receiver,'balance':defaultdict(float),'nonce':0}
		
		account['balance']['btcRelay'] += value

		try:
			balanceDB.put(address.encode(), pickle.dumps(account))
			return True
		except:
			return False

	def blockTransaction():
		con = config.config()
		configDB = db.DB("trie/configDB")
		currBlockkey = con["currBTCRelayBlock"]
		confirmation = con["CCRConfirmation"]
		currNonceKey = con["currNonceCCR"]
		while True:
			currBlockRead = pickle.loads(configDB.get(currBlockkey.encode()))
			blockNum = json.loads(bitcoinRPC().blocknumber())["result"]
			print("blockNum:", blockNum)
			print("currBlockRead:", currBlockRead)
			if blockNum < currBlockRead+confirmation:
				time.sleep(60)
				continue
			else:
				currNonce = pickle.loads(configDB.get(currNonceKey.encode()))
				r = bitcoinRPC().blockInfo(currBlockRead)
				z = json.loads(r) 
				transactions = []
				key = "4f269e92bde3b00f9b963d665630445b297e2e8d29987b1d50d1e8785372e393"
				for y in z["result"]["tx"]: 
					#print(y)
					flag, value, address = bitcoinInfo.parseTransaction(y) 
					if flag:
						print(flag, value, address)
						currNonce += 1
						transaction = {
							"to": address,
							"out": {"btr": str(int(float(value)*10e7))},
							"nonce":str(currNonce),
						    "fee":"10",
						    "type":"btc",
						    "input":""
						}
						transaction = Transaction.newTransaction(transaction, key)
						print("transaction:", transaction)
						transactions.append(transaction)
						
				a = bitcoinInfo.pendingBTCRelay(transactions)
				print(a)
				currBlockRead += 1
				configDB.put(currBlockkey.encode(), pickle.dumps(currBlockRead))
				configDB.put(currNonceKey.encode(), pickle.dumps(currNonce))
						#res = bitcoinInfo.btcRelay(value, address)
			#if res:
			#	trie.update(y['txid'], y)
		#new_root = trie.root_hash()
		#rootDB.put(b"btcRelaytrie", new_root)

	

print(bitcoinInfo.blockTransaction())
