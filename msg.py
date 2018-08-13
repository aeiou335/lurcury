"""
status
newBlockHashes
transactions
getBlockHashes
blockHashes
getBlocks
blocks
newBlock
signBlock
newSignBlock
"""

import trie.MerklePatriciaTrie as MPT
from core.database import Database
from core.block import Block
from p2p.udpPeerManager import PeerManager 

class msgProtocol:

    def __init__(self, db, key):
        self.pm = PeerManager()
        self.db = db
        self.key = key
        self.run()
    
    def getBlocks(blockHash):
        result = {}; res = []
        for _hash in blockHash:
            res.append(Database.getBlock(_hash))
        result = {"method": "blocks", "blocks": res}
        return result

    def getTrans(tranHash):
        result = {}; res = []
        for _hash in tranHash:
            res.append(Database.getTransaction(_hash))
        result = {"method": "transactions", "transactions": res}
        return result
    
    def getBlockHashes(maxBlocks):
        blockNum = Database.getBlockNumber(self.db)
        for num in range(maxBlocks, blockNum):
            block = Database.getBlockByID(num)
            blocks.append(block["hash"])
        result = {"method": "blockHashes", "hash": blocks}
        return result

    def parseMsg(message):
        nodeID = message["nodeID"]
        data = message["data"]
        method = data["method"]

        if method == "status":
                
            #elif method == "newBlockHashes":
        elif method == "transactions":
            Database().createTransaction(data["transactions"])

        elif method == "getBlockHashes":
            result = self.getBlockHashes(int(data["maxBlocks"]))
            self.pm.send(result, nodeID)

        elif method == "blockHashes":
            result = {"method": "getBlocks", "hash": data["hash"]}
            self.pm.send(result, nodeID)

        elif method == "getBlocks":
            result = self.getBlocks(data["hash"])
            self.pm.send(result, nodeID)
            for block in result["blocks"]:
                result = self.getTrans(block["transactions"])
                self.pm.send(result, nodeID)

        elif method == "blocks":
            Database().createBlock(data["blocks"])

        elif method == "newBlock":
            self.pm.broadcast(data["block"])

        elif method == "signBlock":
            for block in data["blocks"]:
                Block.newBlock_POA()

        elif method == "newSignBlock":
            

    def run(self):
        while True:
            for key, value in self.pm.recv_queue():
                if not value.empty():
                    msg = value.get()
                    self.parseMsg(msg["data"])
                time.sleep(1)


