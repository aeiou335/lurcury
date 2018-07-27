import threading
#from run import *
#from server import *
import plyvel 
from config import config 

#db = plyvel.DB('testdb/', create_if_missing=True) 
#con = config.config()
if __name__ == '__main__':
    db = plyvel.DB('testdb/', create_if_missing=True)
    con = config.config()

def lurcurymain():
    #for x in range(0, 300):
        #db.put(b'cat', b'dog')
        #print(db.get(b'cat'))
    lurcury.main(db)
'''
def servermain():
    for x in range(0, 300):
        db.put(b'cat', b'dog')
        print(db.get(b'cat'))
        #Server_run.run()
'''
#for selectmain():
    #for x in range()

t1 = threading.Thread(target=lurcurymain)
t1.start()
t2 = threading.Thread(target=servermain)
t2.start()

