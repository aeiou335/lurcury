
# coding: utf-8

# In[1]:


#import leveldb
import plyvel
import time
# In[ ]:


class DB:
    def get(name, key):
        try:
            db = plyvel.DB(name, create_if_missing=True)
        except:
            print("wait")
            time.sleep(1)
            v = DB.get(name, key)
            return v
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
            time.sleep(1)
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
