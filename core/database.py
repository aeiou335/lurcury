import sys
import json
import pickle
import random
import string
from collections import defaultdict
#sys.path.append('core')
from config import config
sys.path.append('trie')
#from db import DB as db
import MerklePatriciaTrie as MPT
sys.path.append("crypto")
#from crypto import basic
from basic import *
#from crypto import basic

class Database():

	def pendingTransaction(newTransaction, db):
		#Insert newTransaction which hasn't verified into the database
		#transactionDB = db.DB("trie/transactionDB")
		con = config.config()
		requireFee = con["requiredFee"]
		con = config.config()
		feeAddress = con["feeAddress"]
		fee = newTransaction['fee']
		feeAccount = pickle.loads(db["balanceDB"].get(feeAddress.encode()))
		feeAccount['balance']['cic'] += int(fee)
		try:
			db["balanceDB"].put(feeAddress.encode(), pickle.dumps(feeAccount))
		except:
			return False 
		if int(newTransaction['fee']) >= int(requireFee): 
			db["pt"].append(newTransaction)
		#if Database.verifyBalanceAndNonce(newTransaction, db):
		#	db["pt"].append(newTransaction)
	
	def getPendingTransaction(db):
		#Return the pending transaction with the largest fee
		#transactionDB = db.DB("trie/transactionDB")
		con = config.config()
		key = con['pendingTransaction']
		#print(key)
		pendingTransaction = pickle.loads(db["transactionDB"].get(key.encode()))
		#print("pendingTransaction:", pendingTransaction)
		if len(pendingTransaction) == 0:
			return {}
		else:
			newTransaction = pendingTransaction.pop(0)
		#print(len(pendingTransaction))
		db["transactionDB"].put(key.encode(), pickle.dumps(pendingTransaction))
		return newTransaction

	def verifyBalanceAndNonce(transaction, db):
		#Verify whether the balance of the account is enough and the nonce is correct
		#Return true if everything is correct, else false
		#balanceDB = db.DB("trie/balanceDB")
		try:
			if transaction['type'] == "btc":
				print("btc")
				address = Key_c.bitcoinaddress(transaction["publicKey"])
			elif transaction['type'] == "btcc":
                                print("btcc")
                                address = Key_c.bitcoinaddress_compress(transaction["publicKey"])
			elif transaction['type'] == "eth":
				print("eth")
				address = Key_c.ethereumaddress(transaction["publicKey"])
			else:
				print("else")
				address = Key_c.address(transaction["publicKey"])
		except:
			print("except")
			address = Key_c.address(transaction["publicKey"])
		print('address:',address)
		#address = 'ilwOop'
		try:
			accountData = pickle.loads(db["balanceDB"].get(address.encode()))
			print('account:', int(accountData['balance']['cic']))
		except:
			print('accounterror')
			return False
		try:
			for coin in transaction['out']:
				if accountData['balance'][coin] < int(transaction['out'][coin]):
					print('coinerror')
					return False
			if 'cic' in transaction['out']:
				cic = int(transaction['out']['cic'])
			else:
				cic = 0
			if accountData['balance']['cic'] < cic + int(transaction['fee']):
				print('feeerror')
				return False
				
		except:
			print('idk')
			return False
		if len(transaction['input']) > 7 and transaction["input"][:4] == "90f4":
                        name = transaction['input'][4:7]
                        con = config.config()
                        feeAddress = con["feeAddress"]
                        try:
                                amount = int(transaction["input"][7:])
                        except:
                                return False
                        requiredFee = 10
                        if int(transaction['out']['cic']) < requiredFee:
                                return False
                        if transaction['to'] != feeAddress:
                                return False
                        if name in currName:
                                return False
		print(accountData['nonce'], int(transaction['nonce']))
		if accountData['nonce']+1 != int(transaction['nonce']):
			return False

		return True

	def updateBalanceAndNonce(transaction, db):
		#Update the balance after if the transaction has been verified
		#balanceDB = db.DB("trie/balanceDB")
		con = config.config()
		feeAddress = con["feeAddress"]
		"""
		fee = transaction['fee']
		feeAccount = pickle.loads(db["balanceDB"].get(feeAddress.encode()))
		feeAccount['balance']['cic'] += int(fee)
		print("feeAccount:", feeAccount)
		try:
			db["balanceDB"].put(feeAddress.encode(), pickle.dumps(feeAccount))
		except:
			return False
		"""
		try:
			if transaction['type'] == "btc":
				sender = Key_c.bitcoinaddress(transaction["publicKey"])
			elif transaction['type'] == "eth":
				sender = Key_c.ethereumaddress(transaction["publicKey"])
			else:
				sender = Key_c.address(transaction["publicKey"])
		except:
			sender = Key_c.address(transaction["publicKey"])
		#sender = 'ilwOop'
		#print('address', address)
		try:
			senderAccount = pickle.loads(db["balanceDB"].get(sender.encode()))
			#print("senderAccount:", senderAccount)
		except:
			return False
		#sender part
		senderAccount['balance']['cic'] -= int(fee)
		
		for coin in transaction['out']:
			senderAccount['balance'][coin] -= int(transaction['out'][coin])
		senderAccount['nonce'] += 1
		
		currName = pickle.loads(db["balanceDB"].get(con["tokenName"].encode()))
		if len(transaction['input']) > 7 and transaction["input"][:4] == "90f4":
			name = transaction['input'][4:7]
			try:
				amount = int(transaction["input"][7:])
			except:
				return False
			currName.append(name)
			senderAccount['balance'][name] += amount
		print("senderAccount:", int(senderAccount['balance']['cic']))
		print("currName:", currName)
		receiver = transaction["to"]
		try:
			db["balanceDB"].put(sender.encode(), pickle.dumps(senderAccount))
			db["balanceDB"].put(con["tokenName"].encode(), pickle.dumps(currName))
		except:
			return False
		try:
			receiverAccount = pickle.loads(db["balanceDB"].get(receiver.encode()))
		except:
			receiverAccount = {'address':receiver,'balance':defaultdict(int),'nonce':0}
		print("receiverAccount:", receiverAccount)
		#receiver part
		for coin in transaction['out']:
			receiverAccount['balance'][coin] += int(transaction['out'][coin])		
		try:
			db["balanceDB"].put(receiver.encode(), pickle.dumps(receiverAccount))
			return True
		except:
			return False

	def createTransaction(transaction, db):
		#Push transaction into database
		#Todo: Transaction Trie
		#rootDB = db.DB("trie/rootDB")
		#transactionDB = db.DB("trie/transactionDB")
		try:
			root = db["rootDB"].get(b'TransactionTrie')
		except:
			root = ""
		trie = MPT.MerklePatriciaTrie(db["transactionDB"], root)
		trie.update(transaction['txid'], transaction)
		new_root = trie.root_hash()
		db["rootDB"].put(b'TransactionTrie', new_root)
	"""
	def addTransactionToBlock(blockData, transaction):
		#Push verified transaction into blockData
		blockData['transaction'].append(transaction)
		return blockData
	"""
	def createBlock(blockData, db):
		#Push block into database
		#Todo: Block Trie
		#rootDB = db.DB("trie/rootDB")
		#blockDB = db.DB("trie/blockDB")
		try:
			root = db["rootDB"].get(b'BlockTrie')
		except:
			root = ""
		print('root:', root)
		trie = MPT.MerklePatriciaTrie(db["blockDB"], root)
		trie.update(blockData['hash'], blockData)
		new_root = trie.root_hash()
		#print('new root:', new_root)
		db["rootDB"].put(b'BlockTrie', new_root)

	def getBlockNumber(db):
		#Return current block number
		#rootDB = db.DB("trie/rootDB")
		#blockDB = db.DB("trie/blockDB")
		try:
			root = db["rootDB"].get(b"BlockTrie")
			print(root)
		except:
			root = ""
		trie = MPT.MerklePatriciaTrie(db["blockDB"], root)
		return trie.id

	def getBlockByID(idx, db):
		#blockDB = db.DB("trie/blockDB")
		try:
			block = db["blockDB"].get(str(idx).encode())
		except:
			return ""
		return pickle.loads(block)


