import sys
import pickle
sys.path.append('trie')
import db

balance = db.DB("trie/balanceDB")
key = '1Dg3QPR2o9bkeNo1cbaMLBDEgcHAkW4wwc'
print(pickle.loads(balance.get(key.encode())))
