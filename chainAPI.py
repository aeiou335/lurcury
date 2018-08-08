import requests 
import json 
import pickle
import pysql
import queue
import threading
from collections import defaultdict
import sys
sys.path.append('trie')
import db as db
import MerklePatriciaTrie as MPT 
from chainRPC import bitcoinRPC, ethRPC

que = queue.Queue()
for i in range(300000,300101):
	que.put(i)

#_hash, height, merkleroot, tx, _time, previousblockhash, difficulty, reward
class thread(threading.Thread):
	def __init__(self, threadID, name, sql, conn, threadLock, _type):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.sql = sql
		self.conn = conn
		self.lock = threadLock
		self.type = _type
	def run(self):
		while que.qsize() > 0:
			num = que.get()
			#self.lock.acquire()
			if self.type == "btc":
				info = json.loads(bitcoinRPC().blockInfo(str(num)))
				parseBtcBlock(info["result"], self.sql, self.conn)
			elif self.type == "eth":
				info = json.loads(ethRPC().getBlockbyNum(num))
				parseEthBlock(info["result"], self.sql, self.conn)
			#self.lock.release()
"""
tran: blockHash, blockNumber, from, gas, gasPrice, hash, input, nonce, to, value
tranRe: blockHash, blockNumber, contractAddress, cumulativeGasUsed, from, gasUsed, logs, logsBloom, status, to, transactionHash, transactionIndex
"""
def parseEthTran(transaction):
	#print("tran:",transaction)
	blockHash = transaction["blockHash"]
	blockNumber = transaction["blockNumber"]
	_from = transaction["from"]
	gas = transaction["gas"]
	gasPrice = transaction["gasPrice"]
	_hash = transaction["hash"]
	_input = transaction["input"]
	nonce = transaction["nonce"]
	to = transaction["to"]
	value = transaction["value"] 
	traninfo = ethRPC().getTransaction(_hash)
	tranRe = ethRPC().getTransactionRe(_hash)
	print("RE:",tranRe)
#hash, blockNumber, parentHash, transactions
def parseEthBlock(info, sql, conn):
	_hash = info["hash"]
	blockNum = info["number"]
	parentHash = info["parentHash"]
	transactions = info["transactions"]
	#pysql.updateBlockStatus(conn, _hash, blockNum, parentHash, tx)
	#print(info)
	if not transactions:
		return 0
	for tran in transactions:
		parseEthTran(tran)
		



#hash blockNumber parentHash transactions
def parseBtcBlock(info, sql, conn):
	print(info)

	_hash = info['hash']
	blockNum = info["height"]
	txs = info['tx']
	tx = ""
	for t in txs:
		tx += t
	try:
		parentHash = info['previousblockhash']
	except:
		parentHash = ""
	pysql.updateBlockStatus(conn, _hash, blockNum, parentHash, tx)
	#hex, txid, hash, blockhash 
	for t in txs:
		tran = json.loads(bitcoinRPC().transaction(t))["result"]
		print("tran:", tran)
		if tran == None:
			break
		
		_hex = tran["hex"]
		txid = tran['txid']
		blockhash = tran['blockhash']
		tranhash = tran["hash"]
		vins = tran['vin']
		vouts = tran['vout']
		print("vins:",vins)
		print("vouts:",vouts)
		pysql.updateTxStatus(conn, _hex, txid, tranhash, blockhash)
		#unspendtxid, txid, vout, coinbase
		for vin in vins:
			vin_vout = 0; coinbase = ''; scriptSig_asm = ''; scriptSig_hex = ''; unspendtxid = ''
			if 'coinbase' in vin:
				coinbase = vin['coinbase']
				sequence = vin['sequence']
				#n = vin['n']
			else:
				unspendtxid = vin['txid']
				vin_vout = vin['vout']
				"""
				sequence = vin['sequence']
				scriptSig = json.loads(vin['scriptSig'])
				scriptSig_asm = scriptSig['asm']
				scriptSig_hex = scriptSig['hex']
				"""
			pysql.updateVinStatus(conn, unspendtxid, txid, vin_vout, coinbase)
			#print(vin)
			#print(vout)
		for vout in vouts:
			value = vout['value']
			n = vout['n']
			"""
			#scriptPubKey = json.loads(vout['scriptPubKey'])
			scriptPubKey = vout['scriptPubKey']
			scriptPubKey_asm = scriptPubKey['asm']
			scriptPubKey_hex = scriptPubKey['hex']
			scriptPubKey_type = scriptPubKey['type']
			scriptPubKey_addresses = scriptPubKey['addresses']
			if 'scriptPubKey_reqSigs' in scriptPubKey:
				scriptPubKey_reqSigs = scriptPubKey['scriptPubKey_reqSigs']
			else:
				scriptPubKey_reqSigs = ""
			"""
			#txid, value, n
			pysql.updateVoutStatus(conn, txid, value, n)		
 
def main():
	sql,conn = pysql.sqlcon('192.168.51.11','bc_developer','d!tRv36B','BlockChain')
	num = 10
	
	threads = []
	threadLock = threading.Lock()
	for i in range(1):
		threads.append(thread(i, "thread_{}".format(i), sql, conn, threadLock, "eth"))
	for t in threads:
		t.start()
	print("Current Threads:", threading.active_count())
	#print(pysql.selectStatus(sql, "block"))
	#print(pysql.selectStatus(sql, "transaction"))
	#print(pysql.selectStatus(sql, "transaction_vin"))
	#print(pysql.selectStatus(sql, "transaction_vout"))

if __name__ == '__main__':
	main()


#blockInfo("100") 
#print(bitcoinInfo.blockTransaction("5756ff16e2b9f881cd15b8a7e478b4899965f87f553b6210d0f8e5bf5be7df1d")) 
#print(bitcoinInfo.parseTransaction("272a3d7fb113d05f7adf211f5bb5fe7e3b52d814870bb5a0e194e4c1dad2fbfc"))