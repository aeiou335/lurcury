import sys
import time
import pickle
from config import config
sys.path.append('trie')
import db
sys.path.append('core')
from database import Database 

d = db.DB("trie/transactionDB")
print(pickle.loads(d.get("36C6C16E16EAC6C88DAC83651A8B72EFF28A1CC165A4346098FF5A3B570480CB".encode())))

"""
key = con["currBTCRelayBlock"]
block = db.DB("trie/configDB")
block.put(key.encode(), pickle.dumps(533402))
"""
