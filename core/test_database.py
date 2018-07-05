from database import database
import time
import json
import string
import random
import sys
sys.path.append('../trie')
import db
import MerklePatriciaTrie as MPT
"""
transaction = {
    "to":"cxfcb42deca97e4e8339e0b950ba5efa368fe71a55",
    "out":{"cic":"10","now":"100"},
    "nonce":"1",
    "fee":"1"
    "txid":
    "sign":
    "publicKey":
}
"""
database = database()
start = time.time()
txid = 0
for i in range(10):
	if i % 1000 == 0:
		print(time.time()-start)
	transaction = {}
	transaction['to'] = 'cx' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
	transaction['out'] = {'cic':random.randint(1,1000),'now':random.randint(1,1000)}
	transaction['nonce'] = '1'
	transaction['fee'] = random.randint(1,10000)
	transaction['sign'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
	transaction['publicKey'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
	transaction['txid'] = 'tx' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
	#if not db.pendingTransaction(transaction):
	#	print('something wrong', transaction)
	print(transaction)
	database.createTransaction(transaction)
	txid = transaction['txid']
end = time.time()
print(end-start)
del database
rootDB = db.DB('rootDB')
root = rootDB.get(b'TransactionTrie')
trie = MPT.MerklePatriciaTrie('testdb', root)
print(trie.search(txid))

