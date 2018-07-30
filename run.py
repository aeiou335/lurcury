from core.database import Database
from core.transaction import Transaction
from core.block import Block
from core.genesis import Genesis

import time
import json

class lurcury:
	def main(conn):
		#fntdb = Database()
		currentBlockNum = Database.getBlockNumber(conn)
		print('getBlockNumber:', currentBlockNum)
		if currentBlockNum == 0:
			genesisBlock = Genesis.genesis()
			Database.createBlock(genesisBlock, conn)
		else:
			while True:
			#for j in range(3):
				#time.sleep(2)
				newBlock = Block.block()
				transactions = []
				#while True:
				t = time.time()
				for i in range(1000):
					#pendingTran = Database.getPendingTransaction(conn)
					pendingTran = conn["pt"].pop(0)
					print("getPendingTranTime:", time.time()-t)
					t = time.time()
					if pendingTran == []:
						print('There is no pending transaction now.')
						continue
					else:
						if not Transaction.verifyTransaction(pendingTran):
							continue
						print("verifyTranTime:", time.time()-t)
						t = time.time()
						#balance verify and nonce
						if not Database.verifyBalanceAndNonce(pendingTran, conn):
							print("verify balance and nonce error")
							continue
						rint("verifyBalnceTime:", time.time()-t)
						t = time.time()
						if not Database.updateBalanceAndNonce(pendingTran, conn):
							print("update error")
							continue
						print("updateBalanceTime:", time.time()-t)
						t = time.time()
					newBlock = Block.pushTransactionToArray(newBlock, pendingTran)
					transactions.append(pendingTran)
				print("time:", time.time()-t)
				#print("newBlock:", newBlock)
				parentBlock = Database.getBlockByID(currentBlockNum-1, conn)
				key = '97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a'
				#print('parent', parentBlock)
				newBlock = Block.newBlock_POA(newBlock, parentBlock, key)
				try:
					Database.createBlock(newBlock, conn)
				except:
					print('Error occurs when saving block into db.')
					continue
				#fntdb.updateDBAccountStatus(newBlock)
				
				#transactions = newBlock['transaction']
				if len(transactions) == 0:
					continue
				for transaction in transactions:
					try:
						Database.createTransaction(transaction, conn)
					except:
						print("Error occurs when saving transaction into db.")
						continue

#lurcury.main()	
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


#if __name__ == "__main__":
	#main()

