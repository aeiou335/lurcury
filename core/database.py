import sys
import json
import pickle
import random
import string
from collections import defaultdict
#sys.path.append('core')
from config import config
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
		self.configDB = db.DB('trie/configDB')
	def pendingTransaction(self, newTransaction):
		#Insert newTransaction which hasn't verified into the database
		con = config.config()
		key = con['pendingTransaction']
		print("pendingKey:", key)
		try:
			pending = pickle.loads(self.transactionDB.get(key.encode()))
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
		#try:
			#print('dumps',pickle.dumps(pending))
		self.transactionDB.put(key.encode(), pickle.dumps(pending))
		print(self.transactionDB.get(key.encode()))
		return True
		#except:
		#	return False

	def getPendingTransaction(self):
		#Return the pending transaction with the largest fee
		con = config.config()
		key = con['pendingTransaction']
		#print(key)
		pendingTransaction = pickle.loads(self.transactionDB.get(key.encode()))
		#print("pendingTransaction:", pendingTransaction)
		if len(pendingTransaction) == 0:
			return {}
		else:
			newTransaction = pendingTransaction.pop(0)
		#print(len(pendingTransaction))
		self.transactionDB.put(key.encode(), pickle.dumps(pendingTransaction))
		return newTransaction

	def verifyBalanceAndNonce(self, transaction):
		#Verify whether the balance of the account is enough and the nonce is correct
		#Return true if everything is correct, else false
		try:
			if transaction['type'] == "btc":
				address = Key_c.bitcoinaddress(transaction["publicKey"])
			elif transaction['type'] == "eth":
				address = Key_c.ethereumaddress(transaction["publicKey"])
			else:
				address = Key_c.address(transaction["publicKey"])
		except:
			address = Key_c.address(transaction["publicKey"])
		print('address:',address)
		#address = 'ilwOop'
		try:
			accountData = pickle.loads(self.balanceDB.get(address.encode()))
			print('account:', int(accountData['balance']['cic']))
		except:
			print('accounterror')
			return False
		#try:
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
				
		#except:
		#	print('idk')
		#	return False
		print(accountData['nonce'], int(transaction['nonce']))
		if accountData['nonce']+1 != int(transaction['nonce']):
			return False

		return True

	def updateBalanceAndNonce(self, transaction):
		#Update the balance after if the transaction has been verified
		con = config.config()
		feeAddress = con["feeAddress"]
		fee = transaction['fee']
		feeAccount = pickle.loads(self.balanceDB.get(feeAddress.encode()))
		feeAccount['balance']['cic'] += int(fee)
		print("feeAccount:", feeAccount)
		try:
			self.balanceDB.put(feeAddress.encode(), pickle.dumps(feeAccount))
		except:
			return False

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
			senderAccount = pickle.loads(self.balanceDB.get(sender.encode()))
			#print("senderAccount:", senderAccount)
		except:
			return False
		#sender part
		senderAccount['balance']['cic'] -= int(fee)
		

		for coin in transaction['out']:
			senderAccount['balance'][coin] -= int(transaction['out'][coin])
		senderAccount['nonce'] += 1
		
		currName = pickle.loads(self.balanceDB.get(con["tokenName"].encode()))
		if 'input' in transaction:
			print('input:',transaction['input'])
			if len(transaction['input']) > 7:
				msg = transaction['input']
				print('msg:', msg)
				if msg[:4] == '90f4':
					name = msg[4:7]
					try:
						amount = int(msg[7:])
					except:
						return False
					requiredFee = 10
					if int(transaction['out']['cic']) < requiredFee:
						return False
					if transaction['to'] != feeAddress:
						return False
					if name in currName:
						return False
				currName.append(name)
				senderAccount['balance'][name] += amount
		print("senderAccount:", int(senderAccount['balance']['cic']))
		print("currName:", currName)
		receiver = transaction["to"]
		try:
			self.balanceDB.put(sender.encode(), pickle.dumps(senderAccount))
			self.balanceDB.put(con["tokenName"].encode(), pickle.dumps(currName))
		except:
			return False
		try:
			receiverAccount = pickle.loads(self.balanceDB.get(receiver.encode()))
		except:
			receiverAccount = {'address':receiver,'balance':defaultdict(int),'nonce':0}
		print("receiverAccount:", receiverAccount)
		#receiver part
		for coin in transaction['out']:
			receiverAccount['balance'][coin] += int(transaction['out'][coin])		
		try:
			self.balanceDB.put(receiver.encode(), pickle.dumps(receiverAccount))
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


