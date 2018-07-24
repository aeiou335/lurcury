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
        print(self.url)
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
    def __init__(self):
        self.url = "http://192.168.51.33:28332"
        self.user = "bitcoinrpc" 
        self.password = "bitcoinrpctest"
o = bitcoinRPC().bitcoinrpc("getblockhash","[1]")
print(o)
o = bitcoinRPC().bitcoinrpc("generate","[1]")
print(o)
