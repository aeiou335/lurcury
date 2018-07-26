
# coding: utf-8

# In[1]:


#import leveldb
import plyvel

# In[ ]:


class DB:
    def get(name, key):
        try:
            db = plyvel.DB(name, create_if_missing=True)
        except:
            DB.get(name, key)
        value = db.get(key)
        db.close()
        assert db.closed
        if value == None:
            value = ""
        #print("key:",key)
        return value
    
    def put(name, key, value):
        try:
            db = plyvel.DB(name, create_if_missing=True)
        except:
            DB.put(name, key, value)
        db.put(key, value)
        db.close()
        assert db.closed
            
    def delete(name, key):
        try:
            db = plyvel.DB(name, create_if_missing=True)
        except:
            DB.delete(name, key)
        db.delete(key)
        db.close()
        assert db.closed

    def deleteAll(name):
        try:
            db = plyvel.DB(name, create_if_missing=True)
        except:
            DB.deleteAll(name)
        for key, value in db:
            db.delete(key)
        db.close()
        assert db.closed