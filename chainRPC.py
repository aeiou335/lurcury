import requests
import json


class bitcoinRPC():
    def blockInfo(self,num):
        r = requests.post(url=self.url,
                                data='{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": ['+str(num)+'] }',
                                headers={"content-type": "text/plain"},
                                auth=(self.user, self.password)
                                )
        z = json.loads(r.text[:1000000000])
        #print(self.url)
        t = requests.post(url=self.url,
                                data='{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["'+z["result"]+'"] }',
                                headers={"content-type": "text/plain"},
                                auth=(self.user, self.password)
                                )
        return(t.text[:1000000000])
    def transaction(self,hes):
        t = requests.post(url=self.url,
                                data='{"jsonrpc": "1.0", "id":"curltest", "method": "getrawtransaction", "params": ["'+hes+'", true] }',
                                headers={"content-type": "text/plain"},
                                auth=(self.user, self.password)
                                )
        return(t.text[:1000000000])
    def bitcoinrpc(self,method,params):
        t = requests.post(url=self.url,
                                data='{"jsonrpc": "1.0", "id":"curltest", "method": "'+method+'", "params":'+params+' }',
                                headers={"content-type": "text/plain"},
                                auth=(self.user, self.password)
                                )
        return(t.text[:1000000000])
    def blocknumber(self):
        t = requests.post(url=self.url,
                                data='{"jsonrpc": "1.0", "id":"curltest", "method": "getblockcount" }',
                                headers={"content-type": "text/plain"},
                                auth=(self.user, self.password)
                                )
        return(t.text[:1000000000])
    def bitcoinrpcnoneparams(self,method):
        t = requests.post(url=self.url,
                                data='{"jsonrpc": "1.0", "id":"curltest", "method": "'+method+'" }',
                                headers={"content-type": "text/plain"},
                                auth=(self.user, self.password)
                                )
        return(t.text[:1000000000])    
    def __init__(self):
        self.url = "http://192.168.51.33:8332"
        self.user = "bitcoinrpc" 
        self.password = "bitcoinrpctest"

class ethbybRPC():
    def __init__(self, url):
        self.url = url

    def getBlockbyNum(self, num):
        h = hex(num)
        t = requests.post(url=self.url, headers = {"content-type":"application/json"}, data='{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["'+h+'", true],"id":1}')
        return t.text[:1000000000]

    def getTransaction(self, tranHash):
        t = requests.post(url = self.url, headers = {"content-type":"application/json"}, 
                            data='{"jsonrpc":"2.0","method":"eth_getTransactionByHash","params":["'+ tranHash +'"],"id":1}')
        return t.text[:1000000000]

    def getTransactionRe(self, tranHash):
        t = requests.post(url = self.url, headers = {"content-type":"application/json"}, 
                            data='{"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params":["'+ tranHash +'"],"id":1}')
        return t.text[:1000000000]

    def getBlockNum(self):
        t = requests.post(url = self.url, headers = {"content-type":"application/json"},  
                            data='{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}')
        return t.text[:1000000000]
#o = bitcoinRPC().bitcoinrpc("getblockhash","[1]")
#print(o)
#io = bitcoinRPC().blocknumber()
#print(ethRPC().getBlockbyNum(10000))
#print(ethRPC().getTransactionRe("0xe1afb70dc68dd9c7c4346bfa542329b7b875b83dbd69561b9784df06810bf0d8"))
url = "https://mainnet.infura.io/"
import time
t = time.time()
print(ethbybRPC("https://mainnet.infura.io/").getBlockbyNum(1000000))
print(time.time()-t)