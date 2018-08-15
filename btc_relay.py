import requests 
import json
import time
import pickle
import sys
from config import config
sys.path.append('trie')
from db import DB as db 
import MerklePatriciaTrie as MPT
sys.path.append('core')
from transaction import Transaction
from chainRPC import *


class bitcoinInfo: 
	def pendingBTCRelay(transactions, db):
		#transactionDB = db.DB("trie/transactionDB")
		con = config.config()
		key = con["pendingTransaction"]
		for t in transactions:
			db["pt"].append(t)
		return True
	def parseTransaction(has): 
		con = config.config()
		ourAccount = con["receiveAddress"]
		
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
		addressKey = "c2cccccc0000000000000001"
		for i, transaction in enumerate(transactions):
			#print(transaction)
			try:
				if i == len(transactions)-1:
					if transaction["scriptPubKey"]["asm"][:9] == "OP_RETURN" and transaction["scriptPubKey"]["asm"][10:34] == addressKey and value != 0:
						address = transaction["scriptPubKey"]["asm"][34:]
						flag = True
						print("params:",flag, vlaue, address)
						return flag, value, address

				if transaction["scriptPubKey"]["addresses"][0] == ourAccount:
					print("params",transactions)
					value += transaction['value']
					"""
					txid = t["vin"][0]["txid"]
					out = t["vin"][0]["vout"]
					print(txid, out)
					originalt = json.loads(bitcoinRPC().transaction(txid))["result"]
					address = originalt["vout"][out]["scriptPubKey"]["addresses"][0]
					"""

			except:
				continue
			#elif i == len(transactions)-1 and flag:
			#	address = transaction['scriptPubKey']['asm'][10:]
		return flag, value, address

	def blockTransaction(db):
		con = config.config()
		#configDB = db.DB("trie/configDB")
		currBlockkey = con["currBTCRelayBlock"]
		confirmation = con["CCRConfirmation"]
		currNonceKey = con["currNonceCCR"]
		while True:
			currBlockRead = pickle.loads(db["configDB"].get(currBlockkey.encode()))
			blockNum = json.loads(bitcoinRPC().blocknumber())["result"]
			print("blockNum:", blockNum)
			print("currBlockRead:", currBlockRead)
			if blockNum < currBlockRead+confirmation:
				time.sleep(60)
				continue
			else:
				currNonce = pickle.loads(db["configDB"].get(currNonceKey.encode()))
				#currNonce = currNonce -2
				#if currNonce < 0:
					#currNonce = 0
				#currNonce = currNonce+6
				print("2currNonce:",currNonce)
				r = bitcoinRPC().blockInfo(currBlockRead)
				z = json.loads(r) 
				transactions = []
				key = "14ea887907e1c00d905f61712b48ccc43cb02e452662ac8cd8a0e2d13845e5a2"
				for y in z["result"]["tx"]: 
					#print(y)
					flag, value, address = bitcoinInfo.parseTransaction(y) 
					if flag:
						print(flag, value, address)
						print("++++++++++++++++++currNonce:",currNonce)
						currNonce -= 1
						transaction = {
							"to": "cx"+address,
							"out": {"btr": str(int(float(value)*10e7))},
							"nonce":str(currNonce),
						    "fee":"10",
						    "type":"cic",#"btcc",
						    "input":""
						}
						currNonce += 2
						transaction = Transaction.newTransaction(transaction, key)
						print("transaction:", transaction)
						transactions.append(transaction)
						
				a = bitcoinInfo.pendingBTCRelay(transactions, db)

				currBlockRead += 1
				db["configDB"].put(currBlockkey.encode(), pickle.dumps(currBlockRead))
				db["configDB"].put(currNonceKey.encode(), pickle.dumps(currNonce))
						#res = bitcoinInfo.btcRelay(value, address)
			#if res:
			#	trie.update(y['txid'], y)
		#new_root = trie.root_hash()
		#rootDB.put(b"btcRelaytrie", new_root)


#print(bitcoinInfo.blockTransaction(top))
