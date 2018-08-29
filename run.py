from core.database import Database
from core.transaction import Transaction
from core.block import Block
from core.genesis import Genesis
import time
import json
import threading
import multiprocessing as mp
import queue

"""
class process(Process):
	def __init__(self, threadID, verifiedPTQue, conn):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.verifiedPTQue = verifiedPTQue
		self.que = conn["pt"]
		self.conn = conn
"""

def parsePT(pendingTran, conn):
	if not Transaction.verifyTransaction(pendingTran):
		return False
	#print("verifyTranTime:", time.time()-t)
	#t = time.time()
	#balance verify and nonce
	if not Database.verifyBalanceAndNonce(pendingTran, conn, "run"):
		#print("verify balance and nonce error")
		return False
	#print("verifyBalnceTime:", time.time()-t)
	#t = time.time()
	if not Database.updateBalanceAndNonce(pendingTran, conn):
		#print("update error")
		return False
	#print("updateBalanceTime:", time.time()-t)
	return True

def run(conn, threadID, lock):
	que = conn["pt"]
	#currentBlockNum = Database.getBlockNumber(conn)
	#print('getBlockNumber:', currentBlockNum, "threadid:", threadID)
	#if currentBlockNum == 0:
	#	genesisBlock = Genesis.genesis()
	#	Database.createBlock([genesisBlock], conn)
	while True:
		t = time.time()
		newBlock = Block.block()
		transactions = []
		while len(que[threadID]) != 0:
		#while time.time()-t < 2:
			#print(time.time()-t, self.threadID)

			#print("current size:", len(que[threadID]))
			#print("current que:", que[threadID])
			pendingTran = que[threadID].pop(0)
			#print("blabla:",pendingTran["sign"])
			if parsePT(pendingTran, conn):
				#print("pendingTran:", pendingTran)
				newBlock = Block.pushTransactionToArray(newBlock, pendingTran)
				transactions.append(pendingTran)
				print("transactions:", transactions)
			print("time:", time.time()-t)
		print("23456789:",Database.getBlockByID(1, conn), threadID)	
		if len(transactions) == 0:
			continue
		print("234:",Database.getBlockByID(1, conn))
		lock.acquire()
		print("--------------------------")
		print("123:",Database.getBlockByID(1, conn))
		print(threadID)
		print("blabla", transactions)
		#print("lock", self.threadID)
		currentBlockNum = Database.getBlockNumber(conn)
		print("curr:", currentBlockNum)
		parentBlock = Database.getBlockByID(currentBlockNum-1, conn)
		key = '97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a'
		#print('parent', parentBlock)
		newBlock = Block.newBlock_POA(newBlock, parentBlock, key)
		print("block number:", newBlock["blockNumber"])
		#print("newBlock_POATime:", time.time()-t)
		#t = time.time()
		try:
			Database.createBlock([newBlock], conn)
			print("after:", Database.getBlockNumber(conn), threadID)
		except:
			print('Error occurs when saving block into db.')
			lock.release()
			continue
		#print("createBlockTime:", time.time()-t)
		#t = time.time()
		try:
			Database.createTransaction(transactions, conn)
		except:
			lock.release()
			print("Error occurs when saving transaction into db.")
			continue				
		lock.release()
		print("23456789:",Database.getBlockByID(1, conn))

class lurcury:
	def main(conn):
		processes = []
		lock = mp.Lock()
		#print("qqq:",conn["pt"])
		#a = mp.Process(target=run, args=(conn,7,lock))
		#a.start()	
		
		for i in range(8):
			p = mp.Process(target=run, args=(conn,i,lock))
			processes.append(p)
		for p in processes:
			p.start()
		
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

