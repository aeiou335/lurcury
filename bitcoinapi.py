import requests 
import json 
import pickle
import pysql
from collections import defaultdict
import sys
sys.path.append('trie')
import db as db
import MerklePatriciaTrie as MPT 


#_hash, height, merkleroot, tx, _time, previousblockhash, difficulty, reward
class thread(threading.Thread):
	def __init__(self, threadID, name, sql, conn, threadLock):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.sql = sql
		self.conn = conn
		self.lock = threadLock
	def run(self):
		while SHARED_Q.qsize() > 0:
			num = SHARED_Q.get()
			self.lock.acquire()
			info = json.loads(bitcoinInfo.blockInfo(str(num)))
			self.lock.release()
			parseBlock(info, self.sql, self.conn)

def parseBlock(info, sql, conn):
	print(info['height'])
	#print(blocknum)
	#try:
	#print(bitcoinInfo.blockInfo(str(blocknum)))
	#info = json.loads(bitcoinInfo.blockInfo(str(blocknum)))
	#except:
	#	parseBlock(blocknum, sql, conn)
	#	return 0
	_hash = info['hash']
	height = info['height']
	merkleroot = info['merkleroot']
	tx = info['tx']
	time = info['time']
	previousblockhash = info['previousblockhash']
	difficulty = info['difficulty']
	#print(_hash, height, merkleroot, tx, time, previousblockhash, difficulty)
	pysql.updateBlockStatus(conn, _hash, height, merkleroot, tx, time, previousblockhash, difficulty)
	for t in tx:
		r = requests.get("https://blockexplorer.com/api/tx/"+t)
		#print(r.text)
		if 'Not found' not in r.text[:1000000000]:
			tran = json.loads(r.text[:1000000000])
			txid = tran['txid']
			blockhash = tran['blockhash']
			txtime = tran['time']
			vins = tran['vin']
			vouts = tran['vout']
			pysql.updateTxStatus(conn, txid, blockhash, txtime)
			for vin in vins:
				vin_vout = 0; coinbase = ''; scriptSig_asm = ''; scriptSig_hex = ''; unspendtxid = ''
				if 'coinbase' in vin:
					coinbase = vin['coinbase']
					sequence = vin['sequence']
					#n = vin['n']
				else:
					unspendtxid = vin['txid']
					vin_vout = vin['vout']
					sequence = vin['sequence']
					scriptSig = json.loads(vin['scriptSig'])
					scriptSig_asm = scriptSig['asm']
					scriptSig_hex = scriptSig['hex']
				pysql.updateVinStatus(conn, unspendtxid, txid, coinbase, vin_vout, scriptSig_asm, scriptSig_hex, sequence)
			#print(vin)
			#print(vout)
			#txid,[value],n,scriptPubKey_asm,scriptPubKey_hex,scriptPubKey_type,scriptPubKey_reqSigs,scriptPubKey_addresses
			for vout in vouts:
				value = vout['value']
				n = vout['n']
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
				pysql.updateVoutStatus(conn, txid,value,n,scriptPubKey_asm,scriptPubKey_hex,scriptPubKey_type,scriptPubKey_reqSigs,scriptPubKey_addresses)
 		
 
def main():
	sql,conn = pysql.sqlcon('','','','')
	num = 10
	
	threads = []
	threadLock = threading.Lock()
	for i in range(1):
		threads.append(thread(i, "thread_{}".format(i), sql, conn, threadLock))
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
