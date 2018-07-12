import requests 
import json 
import pickle
import pysql
from collections import defaultdict
import sys
sys.path.append('trie')
import db as db
import MerklePatriciaTrie as MPT 

class bitcoinInfo: 
	def blockInfo(num): 
		r = requests.get("https://blockexplorer.com/api/block-index/"+num) 
		z = json.loads(r.text[:1000000000]) 
		#print(z["blockHash"]) 
		t = requests.get("https://blockexplorer.com/api/block/"+z["blockHash"]) 
		#print(t.text[:1000000000]) 
		return t.text[:1000000000]

	def parseTransaction(has): 
		ourAccount = "168o1kqNquEJeR9vosUB5fw4eAwcVAgh8P"
		r = requests.get("https://blockexplorer.com/api/tx/"+has) 
		t = json.loads(r.text[:1000000000])
		#print(t)
		transactions = t['vout']
		flag = False
		value = 0
		address = ""
		for i, transaction in enumerate(transactions):
			print(transaction)
			if i < len(transactions)-1:
				if transaction["scriptPubKey"]["addresses"][0] != ourAccount:
					continue
				else:
					value = transaction['value']
					flag = True
			elif i == len(transactions)-1 and flag:
				address = transaction['scriptPubKey']['asm'][10:]
		return flag, value, address

	def btcRelay(value, address):
		balanceDB = db.DB('trie/balanceDB')
		try:
			account = pickle.loads(balanceDB.get(address.encode()))
		except:
			account = {'address':receiver,'balance':defaultdict(int),'nonce':0}
		
		account['balance']['btcRelay'] += value

		try:
			balanceDB.put(address.encode(), pickle.dumps(account))
			return True
		except:
			return False

	def blockTransaction(): 
		r = bitcoinInfo.blockInfo("300000") 
		#print(r) 
		z = json.loads(r) 
		print('haha',z["tx"])
		btcRelayDB = db.DB("trie/btcRelayDB")
		rootDB = db.Db("trie/rootDB")
		try:
			root =  rootDB.get(b"btcRelaytrie")
		except:
			root = ""
		trie = MPT.MerklePatriciaTrie(btcRelayDB, root)
		for y in z["tx"]: 
			flag, value, address = bitcoinInfo.parseTransaction(y) 
			if flag:
				res = bitcoinInfo.btcRelay(value, address)
			if res:
				trie.update(y['txid'], y)
		new_root = trie.root_hash()
		rootDB.put(b"btcRelaytrie", new_root)
#_hash, height, merkleroot, tx, _time, previousblockhash, difficulty, reward
def block():
	x
		

def main():
	sql,conn = pysql.sqlcon('192.168.51.11','bc_developer','d!tRv36B','BlockChain')
	num = 10
	
	for i in range(num):
		print(i)
		info = json.loads(bitcoinInfo.blockInfo(str(i)))
		_hash = info['hash']
		height = info['height']
		merkleroot = info['merkleroot']
		tx = info['tx']
		time = info['time']
		previousblockhash = info['previousblockhash']
		difficulty = info['difficulty']
		pysql.updateBlockStatus(conn, _hash, height, merkleroot, tx, time, previousblockhash, difficulty)
		for t in tx:
			r = requests.get("https://blockexplorer.com/api/tx/"+t)
			print(r.text)
			if 'Not found' not in r.text[:1000000000]:
				tran = json.loads(r.text[:1000000000])
				txid = tran['txid']
				blockhash = tran['blockhash']
				time = tran['time']
				vin = tran['vin']
				vout = tran['vout']
				print(vin)
				print(vout)
		
	#pysql.updateBlockStatus(conn,'00000000de1250dc2df5cf4d877e055f338d6ed1ab504d5b71c097cdccd00e13',30000,'37be054a52112c5f8d2c06d965813a63cc8bd1598133836aec883914c5cf14a7','37be054a52112c5f8d2c06d965813a63cc8bd1598133836aec883914c5cf14a7',1261007544,'00000000b3cc5384f93014f783d86d6e209ad5ca7dc5a613c4f994fa984168c6',1)
	#pysql.updateBlockStatus(conn, '1000',3,'4','5',6,'7',8)
	print(pysql.selectBlockStatus(sql))
if __name__ == '__main__':
	main()


#blockInfo("100") 
#print(bitcoinInfo.blockTransaction("5756ff16e2b9f881cd15b8a7e478b4899965f87f553b6210d0f8e5bf5be7df1d")) 
#print(bitcoinInfo.parseTransaction("272a3d7fb113d05f7adf211f5bb5fe7e3b52d814870bb5a0e194e4c1dad2fbfc"))