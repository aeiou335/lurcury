import threading
from collections import defaultdict
#from run import *
from server import *
import plyvel 
import asyncio
import queue
from config import config
from run import lurcury 
#db = plyvel.DB('testdb/', create_if_missing=True) 
#con = config.config()
import time
from top2 import *
from init_genesis import clearAllDB, init_account, init_transaction
from _tornado import Server
from btc_relay import bitcoinInfo
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
            "pt":{0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[]}
          }
    keys = [{			
	"privateKey": "3cbf4081d2763b0dd6172e4ebb4bf6b03c3b51523c22d07a59f014019de81c83",
	"address": "cx561de3cfa60c756afc906d0e2c5dcce6481ed159"
	},{
	"privateKey": "53c4993d30203571f4907eaa4fbfac90592ccefed9857375075348a54505211f",
	"address": "cxf25a5021ad72515676e77278264ed4f3ff1a958d"
	},{
	"privateKey": "43ac845b27aa04265b998adcef2cacf2f0392e356d059500695a4b40821b60a2",
	"address": "cxa92f918d66be8c7d496f5146251a4cfd001a3741"
	},{
	"privateKey": "ade9aacc69f1a944dbd8338791dbc8552929ec114d43856583e01d2b31b41a2f",
	"address": "cx1d56b7e828f47be684961ae1fe8a9d07354da50d"
	},{
	"privateKey": "507a6b202be4da03e2b314b2a1c5d25538908ba61f7b1f97137a1e430d89ab2c",
	"address": "cxcd94d4c80ddd18754f6980f26ad5544a8dbbc0df"
	},{
	"privateKey": "81aeb84a369a5ced9c7e338fdb252018e0009f0c13b5bf8ba730c9d9660de5d5",
	"address": "cx04c25cac9ad3fcc94731e5e1ecaf89a028cb9a1a"
	},{
	"privateKey": "1ffce4a2fbad30e368f9684cab246a4f4c9bad6f0e6694d0dedcd7d923082e46",
	"address": "cxc1eb0eab697593b200cc5e1833af08e7d131da4d"
	},{
	"privateKey": "99aa83e1397378e43f82b676d52e32eafdfa12c21b57dfeb9c62dde2b2e75092",
	"address": "cx7fce5d1593f96a01eb9cdd7b169beab90310953d"
	},{
	"privateKey": "bd1f34860ee8c592b5a2f5ac519b22ac3ba6b350b856a1cf3f3ea725aaf4cb40",
	"address": "cxeb230c487b281c32633d91ebee92ae6dd2ba6304"
	},{
	"privateKey": "4663a96cb6e05a81b450bfadaa69b3a6be5c5f3388969bee9e8707f98bc45f4a",
	"address": "cx85859a89e0e0fb072ea62411c5ae2e052239aa31"
	},{
	"privateKey": "d236fc4628ef506718990063e6ef06721dde44fa05efe78aedf51702b7e25ef0",
	"address": "cx1dd0730ff63e7fc72407a2b364ca8bee403f455f"
	},{
	"privateKey": "b4f698d3c5ca0aa48a8d4e1a96158cfe5594793e482d8e936e2b5fd61de21088",
	"address": "cx821c17d7c2942218e0d7a931d0205fe0414a1872"
	}]
    top["testdb"].put(b'cat', b'dog')
    print("Reset DB")
    clearAllDB(top)
    print("Init Account")
    init_account(top, keys)
    print("Init Transaction")
    init_transaction(top, keys)
    print("alalala:", top["pt"][0])
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
    asyncio.set_event_loop(asyncio.new_event_loop())
    Server.run(top)
    #Server_run.run(top)
    """
    for x in range(0, 1000000):
        st = str(x)+"dog"
        st = bytes(st, encoding = "utf8")
        top["testdb"].put(st, st)
        print(top["testdb"].get(st))
    """
def btcrelaymain():
    bitcoinInfo.blockTransaction(top)

def runmain():
    for x in range(0, 1000000):
        print(top["run"])

print(time.time())

t1 = threading.Thread(target=lurcurymain)
t1.start()

t2 = threading.Thread(target=servermain)
t2.start()

#t3 = threading.Thread(target=btcrelaymain)
#t3.start()
#t4 = threading.Thread(target=runmain)
#t4.start()

