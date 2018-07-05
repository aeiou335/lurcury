import sys
sys.path.append("../crypto")
from basic import *#Hash_c


class Account:
    def generator_v1():
        priv,pub,addr = Key_c.exp()
        re = {"privateKey":priv,"publicKey":pub,"address":addr,"version":"1","type":"cic"}
        return re


print(Account.generator_v1())

