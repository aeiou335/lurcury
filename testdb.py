import trie.db
import pickle
import random
import string
db = trie.db.DB('acoountdb')
"""
for i in range(500001):
	
	fakeAccount = {}
	fakeAccount['balance'] = {'cic':random.randint(1,1000000),'now':random.randint(1,1000000)}
	fakeAccount['nonce'] = random.randint(1,10000)
	fakeAccount['address'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
	db.put(fakeAccount['address'].encode(), pickle.dumps(fakeAccount))
	if i % 200000 == 0:
		print(fakeAccount)
"""
print(pickle.loads(db.get('95vtNjih7jYZuuOa9jNkD4xoz41wnLRk'.encode())))