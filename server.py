from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import cgi
import json
import pickle
import leveldb
import sys
sys.path.append('trie')
import MerklePatriciaTrie as MPT
import db
sys.path.append('core')
from database import Database
from transaction import Transaction

class BlockTrie(object):
	def __init__(self, root_hash):
		blockDB = db.DB("trie/blockDB")
		self.trie = MPT.MerklePatriciaTrie(blockDB, root_hash) 
	def search(self, key):
		value = self.trie.search(key)
		root_hash = self.trie.root_hash()
		return root_hash, value

class TransactionTrie(object):
	def __init__(self, root_hash):
		transactionDB = db.DB("trie/transactionDB")
		self.trie = MPT.MerklePatriciaTrie(transactionDB, root_hash) 

	def search(self, key):
		value = self.trie.search(key)
		root_hash = self.trie.root_hash()
		return root_hash, value

class Handler(BaseHTTPRequestHandler):

	#def __init__(self):
		#self.blockDB = leveldb.LevelDB("testdb")
		#self.tranDB = leveldb.LevelDB("test2db")
	def do_OPTIONS(self):
		self.send_response(200, "ok")
		self.send_header('Access-Control-Allow-Credentials', 'true')
		self.send_header('Access-Control-Allow-Origin', 'http://192.168.0.125:8888')
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
	 
	def do_GET(self):
		rootDB = db.DB("trie/rootDB")
		try:
			method, param = urlparse(self.path).path.split('/')[1:]
		except:
			self.send_error(400, "Too much parameters")
			return

		if method == "getBlock":
			try:
				root = rootDB.get(b"BlockTrie")
			except:
				root = ""
			print("root:", root)
			trie = BlockTrie(root)
			root, value = trie.search(param)
			print("value:", value)
			rootDB.put(b"BlockTrie", root)	

		elif method == "getBlockbyID":
			idx_db = leveldb.LevelDB("trie/blockDB")
			try:
				value = pickle.loads(idx_db.Get(str(param).encode()))
			except:
				value = "No such id."
			#print("value:", value)

		elif method == "getTransaction":
			try:
				root = rootDB.get(b"TransactionTrie")
			except:
				root = ""
			print('root:', root)
			trie = TransactionTrie(root)
			root, value = trie.search(param)
			
			rootDB.put(b"TransactionTrie", root)

		elif method == "getAccount":
			balanceDB = leveldb.LevelDB("trie/balanceDB")
			value = pickle.loads(balanceDB.Get(param.encode()))

		else:
			self.send_error(415, "No such method.")	

		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.send_header('Access-Control-Allow-Credentials', 'true')
		self.send_header('Access-Control-Allow-Origin', 'http://192.168.0.125:8888')
			
		self.end_headers()
		post_return = {}
		post_return['method'] = method
		post_return['result'] = value
		self.wfile.write(json.dumps(post_return).encode())

	def do_POST(self):
		db = leveldb.LevelDB("trie/rootdb")
		#ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
		#if ctype == 'application/json':
		length = int(self.headers['content-length'])
		#print(self.rfile.read(length).decode())            
		post_values = json.loads(self.rfile.read(length).decode())
		print(post_values)
		method = post_values.get('method')
		#assert isinstance(method, str), "Method must be a string!"

		param = post_values.get('param')
		#print(method, param)
		#assert isinstance(param, str)
		#idx = post_values.get('id')
		#assert isinstance(idx, int), "ID must be an integer!"
		
		if method == "signTransaction":
			transaction = param[0]
			key = param[1]
			
			value = Transaction.newTransaction(transaction, key)
		elif method == 'sendTransaction':
			"""
			param:[{
    		"to":"cxfcb42deca97e4e8339e0b950ba5efa368fe71a55",
    		"out":{"cic":"10","now":"100"},
    		"nonce":"1",
   			"fee":"1",
   			"sign":"",
    		"publicKey":"",
    		"txid":""
			}]
			"""
			transaction = param[0]
			#print(method)
			required = {'to','out','nonce','fee','sign','publicKey','txid'}
			if required <= transaction.keys():
				database = Database()
				if database.pendingTransaction(transaction):
					#print(transaction)
					value = True
				else:
					value = False
			else:
				value = False
		else:
			self.send_error(415, "No such method.")				

		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.send_header('Access-Control-Allow-Credentials', 'true')
		self.send_header('Access-Control-Allow-Origin', 'http://192.168.0.125:8888')
			
		self.end_headers()
		#print("post_values:", post_values)
		print(value)
		post_return = {}
		post_return['method'] = method
		post_return['result'] = value
		self.wfile.write(json.dumps(post_return).encode())
if __name__ == '__main__':
	from http.server import HTTPServer
	server = HTTPServer(("192.168.0.125", 9000), Handler)
	print("Starting server, use <Ctrl-C> to stop")
	server.serve_forever()  