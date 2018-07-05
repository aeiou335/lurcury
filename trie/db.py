
# coding: utf-8

# In[1]:


import leveldb


# In[ ]:


class DB:
    def __init__(self,name):
        self.db = leveldb.LevelDB(name)
        
    def get(self, key):
        try:
            value = self.db.Get(key)
        except KeyError:
            print('There is no such key!', key)
        except Exception as e:
            raise str(e)
        return value
    
    def put(self, key, value):
        self.db.Put(key, value)
            
    def delete(self, key):
        self.db.Delete(key)
        
    def isInTree(self, key):
        try:
            self.db.Get(key)
            return True
        except KeyError:
            return False
    
    def deleteAll(self):
        for key, value in self.db.RangeIter():
            self.db.Delete(key)