import sys
#sys.path.append("../crypto")
from crypto.basic import *#Hash_c
from core.genesis import *#Hash_c
#print(Hash_c.sha256_string(""))
#print(Genesis.genesis())
from core.transactionCode import Code as tranCode
 
class Code:
    def blockEncodeForSign(blockData):
        re = ""
        #print ("w",blockData["version"])
        re = re + blockData["version"]
        re = re + blockData["blockNumber"]
        re = re + str(blockData["timestamp"])
        re = re + blockData["hash"]
        re = re + blockData["extraData"]
        re = re + blockData["ParentHash"]
        for v in blockData["transaction"]:
            re += tranCode.transactionEncode(v)
        #print(re)
        return re
'''
blockData = {
            "version":"sue",
            "config":
                {
                    "version":"init"
                },
            "blockNumber" : "1",
            "timestamp":time.time(),
            "hash":"qwe",
            "extraData":"g",
            "ParentHash":"ddd",
            "verify":["a"],
            "transaction":["a","b"]
}

Code.blockEncodeForSign(blockData)
'''
class Block:
    def block():
        blockData = {
            "version":"sue",
            "config":
                {
                    "version":"init"
                },
            "blockNumber" : "",
            "timestamp":time.time(),
            "hash":"",
            "extraData":"",
            "ParentHash":"",
            "verify":[],
            "transaction":[]
        }
        return blockData
    def pushTransactionToArray(blockData, transaction):
        blockData['transaction'].append(transaction)
        return blockData
        
    def newBlock_POA(blockData,parentblock,key):
        #print (blockData["version"])
        blockData["ParentHash"]= parentblock["hash"]
        blockData["hash"]= Hash_c.sha256_string(str(blockData))
        blockData["blockNumber"]= str(int(parentblock["blockNumber"])+1)
        pub = Key_c.publicKey(key)
        #print(blockData)
        blockJ = Code.blockEncodeForSign(blockData)
        #print(blockJ)
        sign = signature_c.sign(blockJ,key)
        #sign = signature_c.sign("123",key)
        blockData["verify"].append({pub:sign})
        #signature_c.verify(sign,b("123"),pub)
        #print(Key_c.publicKey(key))
        #print(blockData["verify"])
        return blockData
    def verifyBlock(transaction):
        #pub= transaction["verify"][0].items()
        #print(pub)
        en = Code.blockEncodeForSign(transaction)
        try:
            for p,s in transaction["verify"][0].items():
                signature_c.verify(s,b(en),p)
            #balance verify and nonce
            try:
                #check authority or pbft
                return 0
            except:
                #
                print("not enough balance")
        except:
            print("sign error")

'''
class POA:
    def verifyBlock(block):
        if block["verify"]
'''

blockData = {
            "version":"sue",
            "config":
                {
                    "version":"init"
                },
            "blockNumber" : "",
            "timestamp":time.time(),
            "hash":"",
            "extraData":"",
            "ParentHash":"",
            "verify":[],
            "transaction":[]
}
#print(Block.newBlock_POA(blockData,Genesis.genesis(),"24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53"))
#print(Block.verifyBlock(Block.newBlock_POA(blockData,Genesis.genesis(),"24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53")))

#Block.transactionDecode("000000000000000000000000000001cxfcb42deca97e4e8339e0b950ba5efa368fe71a55000000000000000000000000000001now000000000000000000000000000100cic000000000000000000000000000010")
