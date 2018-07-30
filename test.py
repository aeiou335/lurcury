import threading
#from run import *
from server import *
import plyvel 
from config import config
from run import lurcury 
#db = plyvel.DB('testdb/', create_if_missing=True) 
#con = config.config()
import time
if __name__ == '__main__':
    db = plyvel.DB('testdb/', create_if_missing=True)
    con = config.config()
    blockDB = plyvel.DB(con["blockDB"], create_if_missing=True)
    transactionDB = plyvel.DB(con["transactionDB"], create_if_missing=True)
    rootDB = plyvel.DB(con["rootDB"], create_if_missing=True)
    balanceDB = plyvel.DB(con["balanceDB"], create_if_missing=True)
    configDB = plyvel.DB(con["configDB"], create_if_missing=True)
    top = {
            "testdb":db,
            "blockDB":blockDB,
            "transactionDB":transactionDB,
            "rootDB":rootDB,
            "balanceDB":balanceDB,
            "configDB":configDB,
            "run":"go"
          }
    top["testdb"].put(b'cat', b'dog')
def lurcurymain():
    lurcury.main(top)
    #Server_run.run(top)
    '''
    for x in range(0, 1000000):
        st = str(x)+"cat"
        st = bytes(st, encoding = "utf8")
        top["testdb"].put(st, st)
        print(top["testdb"].get(st))
    '''
def servermain():
    Server_run.run(top)
    """
    for x in range(0, 1000000):
        st = str(x)+"dog"
        st = bytes(st, encoding = "utf8")
        top["testdb"].put(st, st)
        print(top["testdb"].get(st))
    """
def topmain():
    for x in range(0, 1000000):
        print(123)
        print(top["run"])

def runmain():
    for x in range(0, 1000000):
        print(top["run"])
"""
print(time.time())
t1 = threading.Thread(target=lurcurymain)
t1.start()

t2 = threading.Thread(target=servermain)
t2.start()
"""
t3 = threading.Thread(target=topmain)
t3.start()
t4 = threading.Thread(target=runmain)
t4.start()

