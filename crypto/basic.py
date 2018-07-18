<<<<<<< HEAD
from __future__ import with_statement, division
import eth_keys, eth_utils, binascii, os

import hashlib
import binascii
from six import b, print_, binary_type
#from .keys import SigningKey, VerifyingKey
import base58
import sys
sys.path.append("../")
from ecdsa import SigningKey, VerifyingKey, NIST256p, SECP256k1
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
        priv = SigningKey.generate(curve=SECP256k1)
        priv_hex=(priv.to_string()).hex()
        return priv_hex
    def publicKey(priv):
        '''
        priv = SigningKey.from_string(bytes().fromhex(priv))
        pub = priv.get_verifying_key()
        pub_hex=(pub.to_string()).hex()
        return pub_hex
        '''
        privKey = eth_keys.keys.PrivateKey(binascii.unhexlify(priv))
        pubKey = privKey.public_key
        return pubKey
    def address(pub):
        r = "cx"+Hash_c.sha256_string(pub)[24:64]
        #r = pub.to_checksum_address()
        return r
    def bitcoinpub2addr(key): #input string, output string 
        pubkey = b"04" + b(key) 
        ripemd = hashlib.new('ripemd160') 
        ripemd.update(hashlib.sha256(binascii.unhexlify(pubkey)).digest()) 
        key = ripemd.digest() 
        key = b"00" + binascii.hexlify(key) 
        hash_key = binascii.unhexlify(key) 
        checksum = hashlib.sha256(hashlib.sha256(hash_key).digest()).digest()[:4] 
        key = key + binascii.hexlify(checksum) 
        return str(base58.b58encode(binascii.unhexlify(key)),'ascii')

    def exp():
        f = Key_c.privateKey()
        f2 = Key_c.publicKey(f)
        f3 = Key_c.address(f2)
        #print("key",f,"pub",f2,"addr",f3)
        return (f,f2,f3)

class signature_c:
    def sign(data,priv):
        priv = SigningKey.from_string(bytes().fromhex(priv),curve=SECP256k1)
        data = b(str(data))
        sig = priv.sign(data)
        return binascii.hexlify(sig).decode()
    def verify(signData,rawData,pub):
        signData = binascii.unhexlify(signData)
        pub = VerifyingKey.from_string(bytes().fromhex(pub),curve=SECP256k1)
        return pub.verify(signData, rawData)
    def exp():
        x = signature.sign("blahblah","24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53")
        h = signature.verify(x,b("blahblah"),key.publicKey("24ac4b12bbb37e5b1e59830c7e376f1963b9cacb4233fa53"))
        return h
h = Key_c.privateKey()
print(h)
t = Key_c.bitcoinpub2addr(Key_c.publicKey(h))
print(t)
#print(Key_c.publicKey("97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a"))
#print(Key_c.address("7b83ad6afb1209f3c82ebeb08c0c5fa9bf6724548506f2fb4f991e2287a77090177316ca82b0bdf70cd9dee145c3002c0da1d92626449875972a27807b73b42e"))

#r = signature_c.sign("123","97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a")
#b = signature_c.verify(r,b"123",Key_c.publicKey("97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a"))
#print(r)
#print(b)

#x = signature_c.sign("blahblah","f8b9fc996979291ac2968faeaedd88cd4c2fbc5611fda0605415e05eafc6658a")
#print(x)


