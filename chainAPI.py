import requests 
import json
import time 
import pickle
import pysql
import queue
import threading
from collections import defaultdict
import sys
sys.path.append('trie')
import db as db
import MerklePatriciaTrie as MPT 
from chainRPC import bitcoinRPC, ethbybRPC

que = queue.Queue()
for i in range(500000,500101):
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
def parseEthTran(conn, transaction, rpc, _type):
	#print("tran:",transaction)
	blockHash, blockNumber, _from, gas = transaction["blockHash"], transaction["blockNumber"], transaction["from"], transaction["gas"]
	gasPrice, _hash, _input, nonce = transaction["gasPrice"], transaction["hash"], transaction["input"], transaction["nonce"]
	to, value = transaction["to"], transaction["value"]
	blockNumber, gas, gasPrice, nonce = int(blockNumber, 0), int(gas, 0), int(gasPrice, 0), int(nonce, 0)
	pysql.updateEthTxStatus(conn, blockHash, blockNumber, _from, gas, gasPrice, _hash, _input, nonce, to, value, _type)
	#traninfo = ethRPC().getTransaction(_hash)
	tranRe = rpc.getTransactionRe(_hash)
	#print("RE:",tranRe)
	re = json.loads(tranRe)["result"]
	contractAddress, cumulativeGasUsed, gasUsed, logs = re["contractAddress"], re["cumulativeGasUsed"], re["gasUsed"], json.dumps(re["logs"])
	logsBloom, to, transactionHash, transactionIndex = re["logsBloom"], re["to"], re["transactionHash"], re["transactionIndex"]
	cumulativeGasUsed, gasUsed, transactionIndex = int(cumulativeGasUsed, 0), int(gasUsed, 0), int(transactionIndex, 0)
	pysql.updateEthTxReStatus(conn, blockHash, blockNumber, contractAddress, cumulativeGasUsed, _from, gasUsed, logs, logsBloom, to, transactionHash, transactionIndex, _type)
#hash, blockNumber, parentHash, transactions
def parseEthBlock(info, sql, conn, rpc, _type):
	_hash = info["hash"]
	blockNum = int(info["number"], 0)
	parentHash = info["parentHash"]
	transactions = info["transactions"]
	tx = json.dumps(transactions)
	pysql.updateBlockStatus(conn, _hash, blockNum, parentHash, tx, _type)
	if not transactions:
		return 0
	for tran in transactions:
		parseEthTran(conn, tran, rpc, _type)



#hash blockNumber parentHash transactions
def parseBtcBlock(info, sql, conn):
	_hash = info['hash']
	blockNum = info["height"]
	txs = info['tx']
	tx = json.dumps(txs)
	try:
		parentHash = info['previousblockhash']
	except:
		parentHash = ""
	pysql.updateBlockStatus(conn, _hash, blockNum, parentHash, tx, "btc")
	#hex, txid, hash, blockhash 
	for t in txs:
		tran = json.loads(bitcoinRPC().transaction(t))["result"]
		if tran == None:
			break
		
		_hex = tran["hex"]
		txid = tran['txid']
		blockhash = tran['blockhash']
		tranhash = tran["hash"]
		vins = tran['vin']
		vouts = tran['vout']
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
	readBtcBlock = 0
	readEthBlock = 0
	readBybBlock = 0
	ethRPC = ethbybRPC("https://mainnet.infura.io/")
	bybRPC = ethbybRPC("http://10.0.7.16:9500")
	while True:
		currBtcBlock = json.loads(bitcoinRPC().blocknumber())["result"]
		currEthBlock = int(json.loads(ethRPC.getBlockNum())["result"],0)
		print(bybRPC.getBlockNum())
		currBybBlock = int(json.loads(bybRPC.getBlockNum())["result"],0)
		print("readBtcBlock:", readBtcBlock)
		print("currBtcBlock", currBtcBlock)
		print("readEthBlock:", readEthBlock)
		print("currEthBlock:", currEthBlock)
		print("readBybBlock:", readBybBlock)
		print("currBybBlock:", currBybBlock)
		if readBtcBlock+5 >= currBtcBlock and readEthBlock+5 >= currEthBlock:
			time.sleep(60)
			continue
		"""
		while readEthBlock+5 < currEthBlock:
			info = json.loads(ethRPC.getBlockbyNum(readEthBlock))
			parseEthBlock(info["result"], sql, conn, ethRPC, "eth")
			readEthBlock += 1
			print("readEthBlock:", readEthBlock)
		"""
		while readBybBlock+5 < currBybBlock:
			info = json.loads(bybRPC.getBlockbyNum(readBybBlock))
			parseEthBlock(info["result"], sql, conn, bybRPC, "byb")
			readBybBlock += 1
			print("readBybBlock:", readBybBlock)
		while readBtcBlock+5 < currBtcBlock:
			info = json.loads(bitcoinRPC().blockInfo(str(readBtcBlock)))
			parseBtcBlock(info["result"], sql, conn)
			readBtcBlock += 1
			print("readBtcBlock:", readBtcBlock)
	"""
	que = queue.Queue()
	for i in range(500000,500101):
		que.put(i)
	
	threads = []
	threadLock = threading.Lock()
	for i in range(1):
		threads.append(thread(i, "thread_{}".format(i), sql, conn, threadLock, "btc"))
		threads.append(thread(i, "thread_{}".format(i), sql, conn, threadLock, "eth"))
	for t in threads:
		t.start()
	print("Current Threads:", threading.active_count())
	#print(pysql.selectStatus(sql, "block"))
	#print(pysql.selectStatus(sql, "transaction"))
	#print(pysql.selectStatus(sql, "transaction_vin"))
	#print(pysql.selectStatus(sql, "transaction_vout"))
	"""
if __name__ == '__main__':
	main()


#blockInfo("100") 
#print(bitcoinInfo.blockTransaction("5756ff16e2b9f881cd15b8a7e478b4899965f87f553b6210d0f8e5bf5be7df1d")) 
#print(bitcoinInfo.parseTransaction("272a3d7fb113d05f7adf211f5bb5fe7e3b52d814870bb5a0e194e4c1dad2fbfc"))