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

def handlerwithdb(db):	
	#print("db",db)
	class Handler(BaseHTTPRequestHandler):	
		def do_OPTIONS(self):
			self.send_response(200, "ok")
			self.send_header('Access-Control-Allow-Credentials', 'true')
			#self.send_header('Access-Control-Allow-Origin', 'http://192.168.0.125:8888')
			self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
			self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type") 
		def do_GET(self):
		
			#rootDB = db.DB("trie/rootDB")
			try:
				method, param = urlparse(self.path).path.split('/')[1:]
			except:
				self.send_error(400, "Too much parameters")
				return

			if method == "getBlock":
				value = Database.getBlock(param, db)
				if value == "":
					value = "No such block!"

			elif method == "getBlockbyID":
				#idx_db = db.DB("trie/blockDB")
				value = Database.getBlockByID(param, db)
				if value == "":
					value = "No such id!" 

			elif method == "getTransaction":
				value = Database.getTransaction(param, db)
				if value == "":
					value = "No such transaction!"
		
			elif method == "getAccount":
				#balanceDB = db.DB("trie/balanceDB")
				value = Database.getAccount(param, db)
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
						value = True, transaction["txid"]
					else:
						value = False, "Cannot add into pending transaction!"
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
        server = HTTPServer(("192.168.0.200", 9000), handler)
        print("Starting server, use <Ctrl-C> to stop")
        server.serve_forever()  
#Server_run.run()
