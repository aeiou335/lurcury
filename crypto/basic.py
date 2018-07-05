from __future__ import with_statement, division

import hashlib
import binascii
from six import b, print_, binary_type
#from .keys import SigningKey, VerifyingKey

import sys
#sys.path.append("ecdsa/")
from ecdsa import SigningKey, VerifyingKey
class Hash_c:
    def sha256_string(data):
        data = bytes(data,"utf8")
        m = hashlib.sha256()
        m.update(data)
        r = m.hexdigest()
        return r
    def sha256_bytes(data):
        m = hashlib.sha256()
        m.update(data)
        r = m.hexdigest()
        return r
    '''
    def blake2b_string(data):
        data = bytes(data,"utf8")
        m = hashlib.blake2b()
        m.update(data)
        r = m.hexdigest()
        return r
    '''

class Key_c:
    def privateKey():
        priv = SigningKey.generate()
        priv_hex=(priv.to_string()).hex()
        return priv_hex
    def publicKey(priv):
        priv = SigningKey.from_string(bytes().fromhex(priv))
        pub = priv.get_verifying_key()
        pub_hex=(pub.to_string()).hex()
        return pub_hex
    def address(pub):
        r = "cx"+Hash_c.sha256_string(pub)[24:64]
        return r
    def exp():
        f = Key_c.privateKey()
        f2 = Key_c.publicKey(f)
        f3 = Key_c.address(f2)
        #print("key",f,"pub",f2,"addr",f3)
        return (f,f2,f3)

class signature_c:
    def sign(data,priv):
        priv = SigningKey.from_string(bytes().fromhex(priv))
        data = b(str(data))
        sig = priv.sign(data)
        return binascii.hexlify(sig)
    def verify(signData,rawData,pub):
        signData = binascii.unhexlify(signData)
        pub = VerifyingKey.from_string(bytes().fromhex(pub))
        return pub.verify(signData, rawData)
    def exp():
        x = signature.sign("blahblah","24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53")
        h = signature.verify(x,b("blahblah"),key.publicKey("24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53"))
        return h
'''
r = signature.sign("cxA665A45920422F9D417E4867EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3bx213ixA665A45920422F9D417E4867EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3nx02a82953d14e4495935fa884ea295b26c3ef877dfb9f8c366943cb1873711dfa42db6fbf1f3c4421c9c6dd95ad1dfafb6vx1pxixA665A45920422F9D417E4867EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3nx12a82953d14e4495935fa884ea295b26c3ef877dfb9f8c366943cb1873711dfa42db6fbf1f3c4421c9c6dd95ad1dfafb6vx1pxoxnx0cx67EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3vx1pxoxnx1cx67EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3vx1px","24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53")
print(r)
x = signature.sign("blahblah","24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53")
print(x)
'''
