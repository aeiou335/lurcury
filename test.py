import requests
import json
import threading
import queue
def getBlock(num):
    r = requests.get("https://blockexplorer.com/api/block-index/"+num) 
    print('r',r.text)
    z = json.loads(r.text[:1000000000]) 
    print('z',z["blockHash"]) 
    t = requests.get("https://blockexplorer.com/api/block/"+z["blockHash"]) 
    print('t',t.text[:1000000000]) 
    return t.text[:1000000000]

class thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):
        while SHARED_Q.qsize() > 0:
            num = SHARED_Q.get()
            info = json.loads(getBlock(str(num)))
            
SHARED_Q = queue.Queue()
for j in range(10000):
    SHARED_Q.put(j)
print(SHARED_Q.qsize())
threads = []
for i in range(2):
    threads.append(thread(i, "thread_{}".format(i)))
for t in threads:
    t.start()