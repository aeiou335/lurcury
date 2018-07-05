import random
import unittest
import MerklePatriciaTrie as MPT
import time
from hashlib import sha256
import string
import leveldb
import pickle
class TestingClass(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestingClass, self).__init__(*args, **kwargs)
		self.test = MPT.MerklePatriciaTrie("trie/testdb","")
		self.db = leveldb.LevelDB("trie/rootDB")
	def test_all(self):
		
		start = time.time()
		keys = []
		values = []
		for j in range(5):
			s = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
			val = ''.join(random.choice(string.digits) for _ in range(8))
			#key = sha256(s.encode('utf-8')).hexdigest()
			key = s
			keys.append(key)
			values.append(val)
			self.test.update(key, val)
			#print("Insert {} datas with time {}".format((j+1)*250000,time.time()))
			for i in range(250):
				s = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
				val = ''.join(random.choice(string.digits) for _ in range(8))
				key = sha256(s.encode('utf-8')).hexdigest()
				self.test.update(key, val)
		end = time.time()
		print("Insert time:", end-start)
		print(self.test.id)
		"""
		for i in range(10):
			start = time.time()
			self.assertEqual(self.test.search(keys[i]), values[i])
			end = time.time()
			print("Search time:", end-start)
		"""
		#print("Key count:", self.test.count_key_num())
		print("Current root:", self.test.root_hash())
		self.db.Put(b"BlockTrie", self.test.root_hash())
		print(self.db.Get(b"BlockTrie"))
		#print(self.db.Get(b"BlockTrie")[0:])
		print(keys[0], values[0])
		print(keys[1], values[1])
		"""
Aa98w43xfu
llAOyh5rrs
DbvtXrhkPk
NI1WE03dio
yjo0ZeJlzS
opD5GQKfwN
qsZLKUpjwK
tC2nmSnTPg
COYEsba1Ff
SF8HzHMFiP
		self.assertTrue(self.test.node_type(self.test.root), "Blank")
		self.test.update('\x01\x02\x57',"dog")
		k, v = self.test.root
		self.assertEqual(v, "dog")
		self.test.update('\x01\x02\x58', "dig")
		self.assertTrue(self.test.node_type(self.test.root), "Extension")
		k, v = self.test.root
		node = self.test.decode(v)
		self.assertTrue(self.test.node_type(node), "Branch")
		k, v = self.test.decode(node[7])
		self.assertEqual(v,"dog")
		k, v = self.test.decode(node[8])
		self.assertEqual(v,"dig")
		print(node)
		self.test.update('\x01\x02', "dag")
		
		k, v = self.test.root
		node = self.test.decode(v)
		print(node)
		self.assertEqual(node[-1], "dag")
		node = self.test.decode(node[5])
		self.assertTrue(self.test.node_type(node), "Branch")
		self.test.update('\x01\x02', "dagg")
		k, v = self.test.root
		node = self.test.decode(v)
		self.assertEqual(node[-1], "dagg")
		self.test.update('\x01\x02\x57\x57', "dogg")
		self.test.update('\x01\x02\x57\x57', "doggg")
		k, v = self.test.root
		node = self.test.decode(v)
		k, v = self.test.decode(self.test.decode(self.test.decode(node[5])[7])[5])
		self.assertEqual(v, "doggg")
		print("-------------------------------------------------------")
		self.assertEqual(self.test.search('\x01\x02\x57'), "dog")
		self.assertEqual(self.test.search('\x01\x02\x58'), "dig")
		self.assertEqual(self.test.search('\x01\x02\x57\x57'), "doggg")
		self.assertEqual(self.test.search('\x01\x02'), "dagg")
		print("-------------------------------------------------------")
		self.test.delete('\x01\x02')
		k, v = self.test.root
		node = self.test.decode(v)
		self.test.delete('\x01\x02\x58')
		k,v = self.test.root
		node = self.test.decode(v)
		self.test.delete('\x01\x02\x57')
		k,v = self.test.root
		self.assertEqual(v, "doggg")
		self.test.delete('\x01\x02\x57\x57')
		print("-----------------------------------------------------")
		self.test.update('\x01\x02\x57',"dog")
		self.test.update('\x01\x02\x58', "dig")
		self.test.update('\x01\x02', "dag")
		self.test.update('\x01\x02\x57\x57', "dogg")
		print("Root before delete all:", self.test.root)
		self.test.delete_all()
		print("Root after delete all:",self.test.root)
		self.assertEqual(self.test.search('\x01\x02\x57'), "")
		self.assertEqual(self.test.search('\x01\x02\x58'), "")
		self.assertEqual(self.test.search('\x01\x02\x57\x57'), "")
		self.assertEqual(self.test.search('\x01\x02'), "")
		"""
	#def test_delete_all(self):


if __name__ == '__main__':
	unittest.main()