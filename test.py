import plyvel

db = plyvel.DB('testdb2/', create_if_missing=True)
#db.put(b'cat', b'dog')
print(db.get(b'cat'))
db.close()
