import requests 
import json 
import pickle
import sys
sys.path.append('trie')
import db as db
import MerklePatriciaTrie as MPT 

class bitcoinInfo: 
	def blockInfo(num): 
		r = requests.get("https://blockexplorer.com/api/block-index/"+num) 
		z = json.loads(r.text[:1000000000]) 
		#print(z["blockHash"]) 
		t = requests.get("https://blockexplorer.com/api/block/"+z["blockHash"]) 
		#print(t.text[:1000000000]) 
		return t.text[:1000000000]

	def pendingBTCRelay(transactions):
		transactionDB = db.DB("trie/transactionDB")
		key = b"btcrelay"
		try:
			pending = pickle.loads(transactionDB.get(key))
		except:
			pending = []
		for t in transactions:
			pending.append(t)
		try:
			transactionDB.put(key, pickle.dumps(pending))
			return True
		except:
			return False
			
	def parseTransaction(has): 
		ourAccount = "19vAwujzTjTzJhQQtdQFKeP5u3msLusgWs"
		r = requests.get("https://blockexplorer.com/api/tx/"+has) 
		t = json.loads(r.text[:1000000000])
		#print(t)
		transactions = t['vout']
		flag = False
		value = 0
		try:
			address = t["vin"][0]["addr"]
		except:
			return False, 0, ""
		for i, transaction in enumerate(transactions):
			#print(transaction)
			if i < len(transactions)-1:
				if transaction["scriptPubKey"]["addresses"][0] != ourAccount:
					continue
				else:
					value = transaction['value']
					flag = True
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
			account = {'address':receiver,'balance':defaultdict(int),'nonce':0}
		
		account['balance']['btcRelay'] += value

		try:
			balanceDB.put(address.encode(), pickle.dumps(account))
			return True
		except:
			return False

	def blockTransaction(): 
		r = bitcoinInfo.blockInfo("300000") 
		#print(r) 
		z = json.loads(r) 
		#print('haha',z["tx"])
		"""
		btcRelayDB = db.DB("trie/btcRelayDB")
		rootDB = db.Db("trie/rootDB")
		try:
			root =  rootDB.get(b"btcRelaytrie")
		except:
			root = ""
		trie = MPT.MerklePatriciaTrie(btcRelayDB, root)
		"""
		transactions = []
		for y in z["tx"]: 
			print(y)
			flag, value, address = bitcoinInfo.parseTransaction(y) 
			if flag:
				transaction = {
					"to": address,
					"out": {"cic": str(value)},
					"reviewer": [],
					"sign": []
				}
				print("transaction:", transaction)
				transactions.append(transaction)
		pendingBTCRelay(transactions)
				#res = bitcoinInfo.btcRelay(value, address)
			#if res:
			#	trie.update(y['txid'], y)
		#new_root = trie.root_hash()
		#rootDB.put(b"btcRelaytrie", new_root)

	

print(bitcoinInfo.blockTransaction())
"""
{ 
	"to": "1DoZKq5EwmRpSEGqaZZJWKQ35ncPHDLGD4", 
	"out": {"cic":"100"},
	"reviewer":["cx"],
	"sign":[""]
}
"""
