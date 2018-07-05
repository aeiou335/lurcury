import sys
sys.path.append("../crypto")
from basic import *#Hash_c
from genesis import *#Hash_c
#print(Hash_c.sha256_string(""))
#print(Genesis.genesis())
from transactionCode import Code

class Block:
    #parentHash
    def newBlock_POA(parentblock,key):
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
        blockData["ParentHash"]= parentblock["hash"]
        blockData["hash"]= Hash_c.sha256_string(str(blockData))
        blockData["blockNumber"]= str(int(parentblock["blockNumber"])+1)
        pub = Key_c.publicKey(key)
        sign = signature_c.sign(Hash_c.sha256_string(str(blockData)),key)
        blockData["verify"].append({pub:signature_c.sign(Hash_c.sha256_string(str(blockData)),key)})
        #print(Key_c.publicKey(key))
        #print(blockData["verify"])
        return blockData
    def newTransaction(transactionData,key):
        en = Code.transactionEncode(transactionData)
        sign = signature_c.sign(en,key)
        transactionData["sign"] = sign
        transactionData["publicKey"] = Key_c.publicKey(key)
        return transactionData

    def expTransaction():
        transaction = {
             "to":"cxfcb42deca97e4e8339e0b950ba5efa368fe71a55",
             "out":{"cic":"10","now":"100"},
             "nonce":"1",
             "fee":"1"
        }
        #sign = signature_c.sign(transaction,"108b4975233c55efc957843265be4aafccdfb4c02b23ed88")
        en = Code.transactionEncode(transaction)
        de = Code.transactionDecode(en)
        #print("de",de)
        sign = signature_c.sign(en,"24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53")
        #print(sign)
        transaction["sign"] = sign
        publickey = Key_c.publicKey("24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53")
        en2 = Code.transactionEncode(de)
        #de = Code.transactionDecode(en)
        #print(signature_c.verify(sign,b(en2),Key_c.publicKey("24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53")))
        transaction["sign"] = sign
        transaction["publicKey"] = Key_c.publicKey("24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53")
        return transaction
    def verifyBlock(transaction):
        #consensus
        return 0
    def verifyTransaction(transaction):
        print(transaction)
        en = Code.transactionEncode(transaction)
        try:
            signature_c.verify(transaction["sign"],b(en),transaction["publicKey"])
            #balance verify and nonce
            try:
                #
                return 0
            except:
                #
                print("not enough balance")
        except:
            print("sign error")

transaction = {
    "to":"cxfcb42deca97e4e8339e0b950ba5efa368fe71a55",
    "out":{"cic":"10","now":"100"},
    "nonce":"1",
    "fee":"1"
}
Block.newTransaction(Block.newTransaction(transaction,"24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53"),"24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53")




#print(Block.newBlock_POA(Genesis.genesis(),"24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53"))
#Block.transactionDecode("000000000000000000000000000001cxfcb42deca97e4e8339e0b950ba5efa368fe71a55000000000000000000000000000001now000000000000000000000000000100cic000000000000000000000000000010")
#print(Block.transactionEncode(Block.expTransaction()))

#print(Block.verifyTransaction(Block.expTransaction()))
#print(Block.expTransaction())
