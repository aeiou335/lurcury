from core.database import Database
from core.transaction import Transaction
from core.block import Block
from core.genesis import Genesis

import time
import json
#def createFakeTransaction():
#	fakeTransaction = 
"""
def updateDBAccountStatus(block):
	transactions = block['transaction']
	if len(transactions) == 0:
		return 0
	for transaction in transactions:
		if not updateBalanceAndNonce(transaction):
			print('Something wrong when updating account status.')
			return False
	return True
"""
def main():
	fntdb = Database()

	currentBlockNum = fntdb.getBlockNumber()
	print('getBlockNumber:', currentBlockNum)
	if currentBlockNum == 0:
		genesisBlock = Genesis.genesis()
		fntdb.createBlock(genesisBlock)
	else:
		#while True:
		for j in range(2):
			time.sleep(2)
			newBlock = Block.block()
			for i in range(5):
				pendingTran = fntdb.getPendingTransaction()
				print(pendingTran)
				if pendingTran == {}:
					print('There is no pending transaction now.')
					continue
				else:
					if not Transaction.verifyTransaction(pendingTran):
						continue
					#balance verify and nonce
					if not fntdb.verifyBalanceAndNonce(pendingTran):
						print("verify balance and nonce error")
						continue
					
					if not fntdb.updateBalanceAndNonce(pendingTran):
						print("update error")
						return False
					
				newBlock = Block.pushTransactionToArray(newBlock, pendingTran)
			#print("newBlock:", newBlock)
			parentBlock = fntdb.getBlockByID(currentBlockNum-1)
			key = '97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a'
			#print('parent', parentBlock)
			newBlock = Block.newBlock_POA(newBlock, parentBlock, key)
			try:
				fntdb.createBlock(newBlock)
			except:
				print('Error occurs when saving block into db.')
				continue
			#fntdb.updateDBAccountStatus(newBlock)
			
			transactions = newBlock['transaction']
			if len(transactions) == 0:
				continue
			for transaction in transactions:
				try:
					fntdb.createTransaction(transaction)
				except:
					print("Error occurs when saving transaction into db.")
					continue

#getBlockNumber
#if(blockNumber == null):
#--getBlockNumber
#genesisBlock
#genesisBlockInsertToDB
#--createGenesisBlock()
#updateGenesisAccountBalance
#else:
#getPendingTransaction
#verifyTransaction
#pushTransactionToArray
#getparentblock
#--getBlock()
#newBlock_POA(blockData,parentblock,key)
#blockStoreToDB
#updateDBAccountStatus
#pack transaction
#stay time


if __name__ == "__main__":
	main()

