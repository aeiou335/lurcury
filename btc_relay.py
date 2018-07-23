import requests 
import json 
import pickle
import sys
from config import config
sys.path.append('trie')
import db as db
import MerklePatriciaTrie as MPT
sys.path.append('core')
from transaction import Transaction

class bitcoinRPC: 
    def blockInfo(num): 
        r = requests.post(url='http://192.168.51.33:8332', 
                        data='{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": ['+str(num)+'] }', 
                        headers={"content-type": "text/plain"}, 
                        auth=('bitcoinrpc', 'bitcoinrpctest') 
                        ) 
        z = json.loads(r.text[:1000000000]) 
        t = requests.post(url='http://192.168.51.33:8332', 
                        data='{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ['+str(z)+'] }', 
                        headers={"content-type": "text/plain"}, 
                        auth=('bitcoinrpc', 'bitcoinrpctest') 
                        ) 
        #print(t.text[:1000000000]) 
        return(t.text[:1000000000]) 
    def transaction(hes): 
        t = requests.post(url='http://192.168.51.33:8332', 
                        data='{"jsonrpc": "1.0", "id":"curltest", "method": "getrawtransaction", "params": ["'+hes+'", true] }', 
                        headers={"content-type": "text/plain"}, 
                        auth=('bitcoinrpc', 'bitcoinrpctest') 
                        ) 
        #print(t.text[:1000000000]) 
        return(t.text[:1000000000])

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
		con = config.config()
		key = con["pendingTransaction"]
		try:
			pending = pickle.loads(transactionDB.get(key.encode()))
		except:
			pending = []
		print("pending:", pending)
		for t in transactions:
			pending.append(t)
		try:
			transactionDB.put(key.encode(), pickle.dumps(pending))
			return True
		except:
			return False
			
	def parseTransaction(has): 
		ourAccount = "16Utt62JMF7sM8y6Amc9pPiutRecXsvxct"
		
		r = requests.get("https://blockexplorer.com/api/tx/"+has) 
		try:
			t = json.loads(r.text[:1000000000])
		except:
			return False, 0, ""
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
				try:
					if transaction["scriptPubKey"]["addresses"][0] != ourAccount:
						continue
					else:
						value = transaction['value']
						flag = True
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
			account = {'address':receiver,'balance':defaultdict(int),'nonce':0}
		
		account['balance']['btcRelay'] += value

		try:
			balanceDB.put(address.encode(), pickle.dumps(account))
			return True
		except:
			return False

	def blockTransaction(): 
		#r = bitcoinRPC.blockInfo("533192")
		r = bitcoinInfo.blockInfo("93214") 
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
		key = "4f269e92bde3b00f9b963d665630445b297e2e8d29987b1d50d1e8785372e393"
		#key = '97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a'
		for y in z["tx"]: 
			print(y)
			flag, value, address = bitcoinInfo.parseTransaction(y) 
			print(flag, type(value), address)
			if flag:
				transaction = {
					"to": address,
					"out": {"btr": str(float(value)*10e8)},
					"nonce":"2",
				    "fee":"10",
				    "type":"btc",
				    "input":""
				}
				transaction = Transaction.newTransaction(transaction, key)
				print("transaction:", transaction)
				transactions.append(transaction)
		a = bitcoinInfo.pendingBTCRelay(transactions)
		print(a)
				#res = bitcoinInfo.btcRelay(value, address)
			#if res:
			#	trie.update(y['txid'], y)
		#new_root = trie.root_hash()
		#rootDB.put(b"btcRelaytrie", new_root)

	

print(bitcoinInfo.blockTransaction())
"""
trandb = db.DB("trie/transactionDB")
con = config.config()
key = con["pendingTransaction"]

print(pickle.loads(trandb.get(key.encode())))

{ 
	"to": "1DoZKq5EwmRpSEGqaZZJWKQ35ncPHDLGD4", 
	"out": {"cic":"100"},
	"reviewer":["cx"],
	"sign":[""]
}
"""
