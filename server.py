from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import cgi
import json
import pickle
import sys
sys.path.append('trie')
import MerklePatriciaTrie as MPT
from db import DB as db
sys.path.append('core')
from database import Database
from transaction import Transaction
from config import *

class BlockTrie(object):
	def __init__(self, root_hash, db):
		#blockDB = db.DB("trie/blockDB")
		self.trie = MPT.MerklePatriciaTrie(db["blockDB"], root_hash) 
	def search(self, key):
		value = self.trie.search(key)
		root_hash = self.trie.root_hash()
		return root_hash, value

class TransactionTrie(object):
	def __init__(self, root_hash, db):
		#transactionDB = db.DB("trie/transactionDB")
		self.trie = MPT.MerklePatriciaTrie(db["transactionDB"], root_hash) 

	def search(self, key):
		value = self.trie.search(key)
		root_hash = self.trie.root_hash()
		return root_hash, value
def handlerwithdb(db):	
	#print("db",db)
	class Handler(BaseHTTPRequestHandler):
		#print("db",db)
		#def __init__(self, *args, **kargs):
		#	super(Handler, self).__init__(*args, **kargs)
			
			
		def do_OPTIONS(self):
			self.send_response(200, "ok")
			self.send_header('Access-Control-Allow-Credentials', 'true')
			self.send_header('Access-Control-Allow-Origin', 'http://192.168.0.125:8888')
			self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
			self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type") 
		def do_GET(self):
		
			print(123)
			#rootDB = db.DB("trie/rootDB")
			try:
				method, param = urlparse(self.path).path.split('/')[1:]
			except:
				self.send_error(400, "Too much parameters")
				return

			if method == "getBlock":
				try:
					root = db["rootDB"].get(b"BlockTrie")
				except:
					root = ""
				print("root:", root)
				trie = BlockTrie(root)
				root, value = trie.search(param)
				print("value:", value)
				db["rootDB"].put(b"BlockTrie", root)	

			elif method == "getBlockbyID":
				#idx_db = db.DB("trie/blockDB")
				try:
					value = pickle.loads(db["blockDB"].get(str(param).encode()))
				except:
					value = "No such id."
				print("value:", value)

			elif method == "getTransaction":
				try:
					root = db["rootDB"].get(b"TransactionTrie")
				except:
					root = ""
				print('root:', root)
				trie = TransactionTrie(root)
				root, value = trie.search(param)
				
				db["rootDB"].put(b"TransactionTrie", root)

			elif method == "getAccount":
				#balanceDB = db.DB("trie/balanceDB")
				#try:
				print(db["balanceDB"].get(param.encode()))
				value = pickle.loads(db["balanceDB"].get(param.encode()))
				#except:
				#self.send_error(400, "Account doesn't exist!")
				#return 0

			else:
				self.send_error(415, "No such method.")
				return 0	

			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.send_header('Access-Control-Allow-Credentials', 'true')
			#self.send_header('Access-Control-Allow-Origin', 'http://192.168.0.125:8888')
				
			self.end_headers()
			post_return = {}
			post_return['method'] = method
			post_return['result'] = value
			self.wfile.write(json.dumps(post_return).encode())

		def do_POST(self):
			length = int(self.headers['content-length'])            
			post_values = json.loads(self.rfile.read(length).decode())
			print(post_values)
			method = post_values.get('method')

			param = post_values.get('param')
			
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
					if Database.pendingTransaction(transaction, db):
						print(transaction)
						value = True
					else:
						value = False
				else:
					print("second error")
					value = False
			#param: []

			else:
				self.send_error(415, "No such method.")
				return 0				

			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.send_header('Access-Control-Allow-Credentials', 'true')
				
			self.end_headers()
			#print("post_values:", post_values)
			#print('test')
			post_return = {}
			post_return['method'] = method
			post_return['result'] = value
			self.wfile.write(json.dumps(post_return).encode())
	return Handler	

class Server_run():
    def run(db):
        from http.server import HTTPServer
        handler = handlerwithdb(db)
        server = HTTPServer(("192.168.51.201", 9000), handler)
        print("Starting server, use <Ctrl-C> to stop")
        server.serve_forever()  
#Server_run.run()
