import sys

#sys.path.append("../crypto")
from crypto.basic import *#Hash_c
#sys.path.append('core')
from config import config

class Code:
    def transactionEncode(transaction):
        coins = ['cic', 'now']
        trans = transaction
        re = ""
        reToken= ""
        for coin in trans['out']:
            v = trans['out'][coin]
            for h in range(0,30-len(trans['out'][coin])):
                #v = trans['out'][coin]
                v="0"+v
            reToken = reToken + coin + v
        '''
        for coin in coins:
            if coin in trans['out']:
                v = trans['out'][coin]
                for h in range(0,30-len(trans['out'][coin])):
                    v="0"+v
            reToken = reToken + coin + v
        '''
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
        #lenth = len(trans["to"])
        #re = re+str(len(trans["to"]))+trans["to"]
        #re = re+transaction["nonce"]
        for z in range(0,30-len(trans["fee"])):
            trans["fee"]="0"+trans["fee"]
        re = re+trans["fee"]
        re = re+reToken
        re = re+str(len(trans["to"]))+trans["to"]
        re = re+trans["type"]
        try:
            re = re+trans["input"]
        except:
            re = re
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
        #re["to"] = transaction[30:72]

        re["fee"] = str(int(transaction[30:60]))
        re["out"]=[]
        outjson = {}
        '''
        for t in range(0,int(len(transaction[60:])/33)):
            p = t*33
            #re["out"].append({transaction[102+p:105+p]:str(int(transaction[105+p:135+p]))})
            outjson[transaction[102+p:105+p]] = str(int(transaction[105+p:135+p]))
        '''
        #print("test",transaction[60:63])
        #re["out"].append({"test":"123"})
        re["out"].append({transaction[60:63]:str(int(transaction[63:93]))})
        toint = int(transaction[93:95])
        print(toint)
        re["to"] = transaction[95:95+toint]
        #print(transaction[95+toint:])
        re["type"] = transaction[95+toint:95+toint+3]
        re["input"] = transaction[95+toint+3:95+toint+3+33]
        #re["out"] = outjson
        #print("ch",re)
        #print("ch",transaction)
        return re

class Transaction:
    def newTransaction(transactionData,key):
        en = Code.transactionEncode(transactionData)
        sign = signature_c.sign(en,key)
        transactionData["sign"] = sign
        transactionData["publicKey"] = Key_c.publicKey(key)
        #print('txid:',Code.txid(transactionData))
        transactionData["txid"] = Code.txid(transactionData)
        #print("top2",Code.txid(transactionData))
        
        return transactionData
    def verifyTransaction(transaction):
        #print(transaction)
        en = Code.transactionEncode(transaction)
        try:
            signature_c.verify(transaction["sign"],en.encode(),transaction["publicKey"])
        except:
            print("sign error")
            return False
        return True

class Input:
    def tokenPublish(transactionData):
        if len(transaction['input']) > 7:
            msg = transaction['input']
            #print('msg:', msg)
            if msg[:4] == '90f4':
                name = msg[4:7]
                amount = int(msg[7:])
                requiredFee = int(config.config()["fee"])
                if int(transaction['out'][config.config()["feeToken"]]) < int(config.config()["tokenPublishfee"]):
                    return False
                if transaction['to'] != config.config()["receiveAddress"]:
                    return False
                return True

transaction = {
    #"to":"cxfcb42deca97e4e8339e0b950ba5efa368fe71a55",
    "to":"16yvczqzg526o7q52r9td4sryggmjtpud7",
    "out":{"cic":"10000"},
    "nonce":"1",
    "fee":"10",
    "type":"btc",
    "input":"90f4ccd100000000000000000000000000000"
}
print(Input.tokenPublish(transaction))

#x = Transaction.newTransaction(Transaction.newTransaction(transaction,"97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a"),"97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a")
#print(x)
#print(x)

#print(Code.transactionEncode(x))
#b = Code.transactionEncode(x)
#print(Code.transactionDecode(b))
#pub = '7b83ad6afb1209f3c82ebeb08c0c5fa9bf6724548506f2fb4f991e2287a77090177316ca82b0bdf70cd9dee145c3002c0da1d92626449875972a27807b73b42e'
#en = '000000000000000000000000000001000000000000000000000000000010cic00000000000000000000000000001040cxnIQqsD2gBHcch94c7pQaVLXvHg7USoQmPywn27cic'
#sign = 'ef24fcfd466eb8aeaebc9843f1cbd81cd305047306ce71eb1d7062d28565b43266f6286f6789e1c27670cbe2fd0ece3106ff94bc051a03b2f57aa503e08dcab2'
#signature_c.verify(sign,en.encode(),pub)
'''
=======
#print(x)
#y = Code.txid(x)
#print(y)
#print(Code.transactionDecode("000000000000000000000000000001cxfcb42deca97e4e8339e0b950ba5efa368fe71a55000000000000000000000000000001now000000000000000000000000000100cic000000000000000000000000000010"))
'''
