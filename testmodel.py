import tornado.web
#cur, t = sql.sqlcon("192.168.51.11","bc_developer","d!tRv36B","BlockChain")
#cur.execute("SELECT * FROM eth_block")
#result=cur.fetchall()
#print(result)
import time
from top import * 

class getAccountHandler(tornado.web.RequestHandler):
    def get(self):
        num = self.get_argument("blocknumber")
        print(num)

        self.write(topdb["testdb"].get(b'cat'))

        #topdb["testdb"].close()
'''
        re = {"version":"1.0","status":"2","message":"blocknumber_search","result":[]}
        try:
            num = self.get_argument("blocknumber")
            cur, t = sql.sqlcon("192.168.51.11","bc_developer","d!tRv36B","BlockChain")
            #print("go:","SELECT * FROM eth_block"+" WHERE 'blocknumber'="+str(num))
            cur.execute("SELECT [hash],[blocknumber],[parenthash],[transactions] FROM byb_block"+" WHERE [blocknumber]="+str(num))
            result=cur.fetchall()
            #print(result)
            for (what) in enumerate(result):
                c1,c2 = what
                Hash,Blocknumber,Parenthash,Transactions = c2
                re["result"].append({"hash":Hash,"blocknumber":Blocknumber,"parenthash":Parenthash,"transactions":Transactions})
            #c1 = result
            #self.write(str(re))
        except:
            re = {"version":"1.0","status":"5","message":"blocknumber_search_error","result":[]}
        self.write(str(re))
'''


