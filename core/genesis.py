import time
import sys
#sys.path.append("../crypto")
#from basic import *#Hash_c
#sys.path.append("./crypto")
#from basic import *

class Genesis:
    def genesis():
        genesis = {
            "version":"sue",
            "config":
                {
                    "version":"init"
                },
            "blockNumber" : "0",
            "timestamp":time.time(),
            "hash":"AC66D1839E1B79F1FB22181B70237F1E45E3D95A512A0790C216328CA2631674",
            "extraData":"",
            "ParentHash":"",
            "transaction":[{"to":"cxa65cfc9af6b7daae5811836e1b49c8d2570c9387",
                            "out":{"cic":"5000000000000000000000000000","now":"100000000"},
                            "nonce":"1",
                            "fee":"1"}]
        }
        return genesis

