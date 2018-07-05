import sys

#sys.path.append("../crypto")
from crypto.basic import *#Hash_c


class Code:
    def transactionEncode(transaction):
        coins = ['cic', 'now']
        trans = transaction
        re = ""
        reToken= ""
        for coin in coins:
            if coin in trans['out']:
                v = trans['out'][coin]
                for h in range(0,30-len(trans['out'][coin])):
                    v="0"+v
            reToken = reToken + coin + v
        """
        for i,v in trans["out"].items():
            #print(v)
            for h in range(0,30-len(v)):
                v="0"+v
            print(v)
            reToken = reToken+i+v
            print(reToken)
        """
        for x in range(0,30-len(trans["nonce"])):
            trans["nonce"]="0"+trans["nonce"]
        re = re+trans["nonce"]
        re = re+trans["to"]
        #re = re+transaction["nonce"]
        for z in range(0,30-len(trans["fee"])):
            trans["fee"]="0"+trans["fee"]
        re = re+trans["fee"]
        re = re+reToken
        #print(re)
        return re
    #newTransaction
    def txid(transaction):
        trans = transaction
        re = ""
        reToken= ""
        for i,v in trans["out"].items():
            for h in range(0,30-len(v)):
                v="0"+v
            reToken = reToken+i+v
        for x in range(0,30-len(trans["nonce"])):
            trans["nonce"]="0"+trans["nonce"]
        re = re+trans["nonce"]
        re = re+trans["to"]
        #re = re+transaction["nonce"]
        for z in range(0,30-len(trans["fee"])):
            trans["fee"]="0"+trans["fee"]
        re = re+trans["fee"]
        #re = re+trans["sign"].decode("utf-8")
        re = re+trans["sign"]
        #print("top:",trans["sign"].decode("utf-8"))
        re = re+reToken
        re = Hash_c.sha256_string(re)
        #trans["txid"]=re
        return re
    def transactionDecode(transaction):
        re = {}
        re["nonce"] = str(int(transaction[0:30]))
        re["to"] = transaction[30:72]

        re["fee"] = str(int(transaction[72:102]))
        re["out"]=[]
        outjson = {}
        for t in range(0,int(len(transaction[102:])/33)):
            p = t*33
            #re["out"].append({transaction[102+p:105+p]:str(int(transaction[105+p:135+p]))})
            outjson[transaction[102+p:105+p]] = str(int(transaction[105+p:135+p]))
        re["out"] = outjson
        #print("ch",re)
        #print("ch",transaction)
        return re

class Transaction:
    def newTransaction(transactionData,key):
        en = Code.transactionEncode(transactionData)
        sign = signature_c.sign(en,key)
        transactionData["sign"] = sign.decode()
        transactionData["publicKey"] = Key_c.publicKey(key)
        #print('txid:',Code.txid(transactionData))
        transactionData["txid"] = Code.txid(transactionData)
        #print("top2",Code.txid(transactionData))

        return transactionData
    def verifyTransaction(transaction):
        #print(transaction)
        en = Code.transactionEncode(transaction)
        
        signature_c.verify(transaction["sign"].encode(),b(en),transaction["publicKey"])
        #except:
        #    print("sign error")
        #    return False
        

        return True
"""
transaction = {
    "to":"cxfcb42deca97e4e8339e0b950ba5efa368fe71a55",
    "out":{"cic":"10","now":"100"},
    "nonce":"1",
    "fee":"1"
}
x = Transaction.newTransaction(Transaction.newTransaction(transaction,"24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53"),"24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53")

print(x)


print(Code.transactionDecode("000000000000000000000000000001cxfcb42deca97e4e8339e0b950ba5efa368fe71a55000000000000000000000000000001now000000000000000000000000000100cic000000000000000000000000000010"))


=======
#print(x)
#y = Code.txid(x)
#print(y)
#print(Code.transactionDecode("000000000000000000000000000001cxfcb42deca97e4e8339e0b950ba5efa368fe71a55000000000000000000000000000001now000000000000000000000000000100cic000000000000000000000000000010"))
"""

