import sys
import json
import pickle
import random
import string
from collections import defaultdict
sys.path.append('trie')
import db as db
import MerklePatriciaTrie as MPT
sys.path.append("crypto")
#from crypto import basic
from basic import *
#from crypto import basic

class Database:
	def __init__(self):
		#self.pendingTransactionDB = db.DB('pendingTransactionDB')
		self.balanceDB = db.DB('trie/balanceDB')
		self.transactionDB = db.DB('trie/transactionDB')
		self.blockDB = db.DB('trie/blockDB')
		self.rootDB = db.DB('trie/rootDB')
		
	def pendingTransaction(self, newTransaction):
		#Insert newTransaction which hasn't verified into the database
		key = b'1234567'
		try:
			pending = pickle.loads(self.transactionDB.get(key))
		except:
			pending = []
		#print(len(pending))
		requireFee = 5
		if int(newTransaction['fee']) > requireFee: 
			#print('new:',newTransaction)
			pending.append(newTransaction)
			#print('pending after append:', pending)
		else: 
			return False
		"""
		flag = False
		#print(newTransaction)
		for idx, transaction in enumerate(pending):
			if newTransaction['fee'] < transaction['fee']:
		if not flag:
			pending.append(newTransaction)
		"""
		try:
			#print('dumps',pickle.dumps(pending))
			self.transactionDB.put(key, pickle.dumps(pending))
			#print(self.transactionDB.get(key))
			return True
		except:
			return False

	def getPendingTransaction(self):
		#Return the pending transaction with the largest fee
		key = b'1234567'
		pendingTransaction = pickle.loads(self.transactionDB.get(key))
		if len(pendingTransaction) == 0:
			return {}
		else:
			newTransaction = pendingTransaction.pop(0)
		print(len(pendingTransaction))
		self.transactionDB.put(key, pickle.dumps(pendingTransaction))
		return newTransaction

	def verifyBalanceAndNonce(self, transaction):
		#Verify whether the balance of the account is enough and the nonce is correct
		#Return true if everything is correct, else false
		try:
			if transaction.type == "btc":
				address = Key_c.bitcoinaddress(transaction["publicKey"])
			elif transaction.type == "eth":
				address = Key_c.ethereumaddress(transaction["publicKey"])
			else:
				address = Key_c.address(transaction["publicKey"])
		except:
			address = Key_c.address(transaction["publicKey"])
		#print('address:',address)
		#address = 'ilwOop'
		try:
			accountData = pickle.loads(self.balanceDB.get(address.encode()))
			print('account:', accountData)
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
		print(accountData['nonce'], int(transaction['nonce']))
		if accountData['nonce']+1 != int(transaction['nonce']):
			return False

		return True

	def updateBalanceAndNonce(self, transaction):
		#Update the balance after if the transaction has been verified

		feeAddress = 'cx68c59720de07e4fdc28efab95fa04d2d1c5a2fc1'
		fee = transaction['fee']
		feeAccount = pickle.loads(self.balanceDB.get(feeAddress.encode()))

		receiver = transaction["to"]
		try:
			receiverAccount = pickle.loads(self.balanceDB.get(receiver.encode()))
		except:
			receiverAccount = {'address':receiver,'balance':defaultdict(int),'nonce':0}
		
		sender = Key_c.address(transaction["publicKey"])
		#sender = 'ilwOop'
		try:
			senderAccount = pickle.loads(self.balanceDB.get(sender.encode()))
		except:
			return False

		senderAccount['balance']['cic'] -= int(fee)
		feeAccount['balance']['cic'] += int(fee)

		for coin in transaction['out']:
			senderAccount['balance'][coin] -= int(transaction['out'][coin])
			receiverAccount['balance'][coin] += int(transaction['out'][coin])
		senderAccount['nonce'] += 1
		
		currName = pickle.loads(self.balanceDB.get('name'.encode()))
		if 'input' in transaction:
			print('input:',transaction['input'])
			if len(transaction['input']) > 7:
				msg = transaction['input']
				print('msg:', msg)
				if msg[:4] == '90f4':
					name = msg[4:7]
					amount = int(msg[7:])
					requiredFee = 10
					if int(transaction['out']['cic']) < requiredFee:
						return False
					if transaction['to'] != feeAddress:
						return False
					if name in currName:
						return False
				currName.append(name)
				senderAccount['balance'][name] += amount

		print("senderAccount:", senderAccount)
		print("currName:", currName)		
		try:
			self.balanceDB.put(sender.encode(), pickle.dumps(senderAccount))
			self.balanceDB.put(receiver.encode(), pickle.dumps(receiverAccount))
			self.balanceDB.put('name'.encode(), pickle.dumps(currName))
			return True
		except:
			return False

	def createTransaction(self, transaction):
		#Push transaction into database
		#Todo: Transaction Trie
		try:
			root = self.rootDB.get(b'TransactionTrie')
		except:
			root = ""
		trie = MPT.MerklePatriciaTrie(self.transactionDB, root)
		trie.update(transaction['txid'], transaction)
		new_root = trie.root_hash()
		self.rootDB.put(b'TransactionTrie', new_root)
	"""
	def addTransactionToBlock(blockData, transaction):
		#Push verified transaction into blockData
		blockData['transaction'].append(transaction)
		return blockData
	"""
	def createBlock(self, blockData):
		#Push block into database
		#Todo: Block Trie
		try:
			root = self.rootDB.get(b'BlockTrie')
		except:
			root = ""
		print('root:', root)
		trie = MPT.MerklePatriciaTrie(self.blockDB, root)
		trie.update(blockData['hash'], blockData)
		new_root = trie.root_hash()
		#print('new root:', new_root)
		self.rootDB.put(b'BlockTrie', new_root)

	def getBlockNumber(self):
		#Return current block number
		try:
			root = self.rootDB.get(b"BlockTrie")
			print(root)
		except:
			root = ""
		trie = MPT.MerklePatriciaTrie(self.blockDB, root)
		return trie.id

	def getBlockByID(self, idx):
		try:
			block = self.blockDB.get(str(idx).encode())
		except:
			return ""
		return pickle.loads(block)


