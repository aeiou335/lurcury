## Conversion from key to address ##
'''
    Functions:
        - priv2addr (cls, priv=None, wif=None, main=True)
        - priv2addr_compress (cls, priv=None, wif=None, main=True)
        - priv2pub (cls, priv=None, wif=None)
        - priv2pub_compress (cls, priv=None, wif=None)
        - pub2addr (cls, key, main=True)
        - pub2addr_compress (cls, key, main=True)
        - priv2signkey (cls, priv=None, wif=None)
        - priv2verkey (cls, priv=None, wif=None)
        - compress_pub (cls, key)
        - priv2wif (cls, key)
        - priv2wif_compressed (cls, key)
        - wif2priv (cls, wif)
        - signdata (cls, priv=None, wif=None, signkey=None, data=None)
        - verifydata (cls, priv=None, wif=None, verkey=None, sigdata=None, origdata=None)

    Usage notes:
        1. For signdata(), the input can be privkey/wif/signkey, 
        where privkey and wif are strings and signkey is ecdsa.SigningKey(which 
        can be obtained by calling identity.priv2signkey()).
        
        2. Similarly, for verifydata(), the input verkey must be of type
        ecdsa.VerifyingKey (which can be obtained by identity.priv2verkey()). Privkey
        and wif input types are for testing, don't send your privkey to someone else!
        The signed data created by signdata() should be directly fed into verifydata()
        without any conversions.
        
        3. All other functions accept input as strings and output strings
        
        4. The pubkey inputs to pub2addr() and pub2addr_compress() should be uncompressed
        with b"04" in front of it.
        
        5. There is a parameter main in pub2addr() and pub2addr_compress()
        which indicates where the address corresponds to the mainnet. It defaults to true.
'''
import os
import time
import hashlib
import base58
import ecdsa
import binascii
from six import b

class identity():
    """ 
    Class with keys and encoded address. 
    """
    
    @classmethod
    def priv2addr(cls, priv=None, wif=None, main=True):
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = cls._wif2priv(wiff)
        else:
            privkey = binascii.unhexlify(pk)
        verkey = cls._priv2verkey(privkey)
        pubkey = b"04" + binascii.hexlify(verkey.to_string())
        addr = cls._pub2addr(pubkey,main)
        return str(addr, 'ascii')

    @classmethod
    def priv2addr_compress(cls, priv=None, wif=None, main=True):
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = cls._wif2priv(wiff)
        else:
            privkey = binascii.unhexlify(pk)
        verkey = cls._priv2verkey(privkey)
        pubkey = binascii.hexlify(verkey.to_string())
        pbc = cls._compress_pub(pubkey)
        addr = cls._pub2addr(pbc,main)
        return str(addr, 'ascii')

    @classmethod
    def priv2pub(cls, priv=None, wif=None):
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = cls._wif2priv(wiff)
            #privkey = binascii.hexlify(privkey)
        else:
            privkey = binascii.unhexlify(pk)
        verkey = cls._priv2verkey(privkey)
        pubkey = b"04" + binascii.hexlify(verkey.to_string())
        return str(pubkey, 'ascii')

    @classmethod
    def priv2pub_compress(cls, priv=None, wif=None):
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = cls._wif2priv(wiff)
        else:
            privkey = binascii.unhexlify(pk)
        verkey = cls._priv2verkey(privkey)
        pubkey = binascii.hexlify(verkey.to_string())
        pbc = cls._compress_pub(pubkey)
        return str(pbc, 'ascii')

    @classmethod
    def pub2addr(cls, key, main=True):   #input not compressed
        pubkey = b(key) if isinstance(key,str) else key
        if len(pubkey) == 128:
            pubkey = b"04" + pubkey
        addr = cls._pub2addr(pubkey,main=main)      
        return str(addr, 'ascii')

    @classmethod
    def pub2addr_compress(cls, key, main=True):    #input not compressed
        pubkey = b(key) if isinstance(key,str) else key
        if len(pubkey) == 130:
            pb_comp = cls._compress_pub(pubkey[2:])
        elif len(pubkey) == 128:
            pb_comp = cls._compress_pub(pubkey)
        else:
            print("error!! key length neither 130 nor 128")
        addr = cls._pub2addr(pb_comp,main=main)      
        return str(addr, 'ascii')
    
    @classmethod
    def priv2signkey(cls, priv=None, wif=None):
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = cls._wif2priv(wiff)
        else:
            privkey = binascii.unhexlify(pk)
        p = cls._priv2signkey(privkey)
        #return str(binascii.hexlify(p.to_string()), 'ascii')
        return p.to_string()

    @classmethod
    def priv2verkey(cls, priv=None, wif=None):
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = cls._wif2priv(wiff)
        else:
            privkey = binascii.unhexlify(pk)
        v = cls._priv2verkey(privkey)
        #return str(binascii.hexlify(v.to_string()), 'ascii')
        return v.to_string()

    @classmethod
    def compress_pub(cls, key):
        pubkey = b(key) if isinstance(key,str) else key
        if len(pubkey) == 130:
            pb_comp = cls._compress_pub(pubkey[2:])
        elif len(pubkey) == 128:
            pb_comp = cls._compress_pub(pubkey)
        return pb_comp

    @classmethod
    def priv2wif(cls, key):
        privkey = b(key) if isinstance(key,str) else key
        wif = cls._priv2wif(privkey)
        return str(wif, 'ascii')
        #return str(binascii.hexlify(wif), 'ascii')

    @classmethod
    def priv2wif_compressed(cls, key):
        privkey = b(key) if isinstance(key,str) else key
        wif = cls._priv2wif(privkey,True)
        return str(wif, 'ascii')

    @classmethod
    def wif2priv(cls, wif):
        wiff = b(wif) if isinstance(wif,str) else wif
        p = cls._wif2priv(wiff)
        return str(binascii.hexlify(p), 'ascii')
    
    @classmethod
    def signdata(cls, priv=None, wif=None, signkey=None, data=None):
        assert data is not None, "no data given!"
        data = b(data) if isinstance(data, str) else data
        
        if signkey is not None:
            #signkey = binascii.unhexlify(signkey)
            skey = ecdsa.SigningKey.from_string(signkey,curve=ecdsa.SECP256k1) #if isinstance(signkey,str) else signkey
        else:
        
            pk = b(priv) if isinstance(priv,str) else priv
            wiff = b(wif) if isinstance(wif,str) else wif
            if pk == None:
                assert wiff is not None, "no keys given!"
                privkey = cls._wif2priv(wiff)
            else:
                privkey = binascii.unhexlify(pk)
            skey = cls._priv2signkey(privkey)
        
        #return binascii.hexlify(skey.sign(data))
        return skey.sign(data)
            
    @classmethod
    def verifydata(cls, priv=None, wif=None, verkey=None, sigdata=None, origdata=None):
        '''
        assert sigdata is not None, "no signed data given!"
        assert origdata is not None, "no original data given!"      
        if verkey is not None:
            #verkey = binascii.hexlify(b(verkey))
            vkey = ecdsa.VerifyingKey.from_string(verkey,curve=ecdsa.SECP256k1) #if isinstance(verkey,str) else verkey
            assert isinstance(vkey, ecdsa.VerifyingKey)
        else:
            
            if pubkey is not None:
                verkey = binascii.unhexlify(pubkey[2:])
                vkey = ecdsa.VerifyingKey.from_string(verkey,curve=ecdsa.SECP256k1) if isinstance(verkey,str) else verkey
                assert isinstance(verkey,ecdsa.VerifyingKey)
            else:
            
            pk = b(priv) if isinstance(priv,str) else priv
            wiff = b(wif) if isinstance(wif,str) else wif
            if pk == None:
                assert wiff is not None, "no keys given!"
                privkey = cls._wif2priv(wiff)
            else:
                privkey = binascii.unhexlify(pk)
            vkey = cls._priv2verkey(privkey)
        '''
        vkey = ecdsa.VerifyingKey.from_string(verkey,curve=ecdsa.SECP256k1)
        #sigdata = binascii.unhexlify(sigdata)
        origdata = b(origdata)
        return vkey.verify(sigdata, origdata)


################## PRIVATE FUNCTIONS ###########################
    
    @staticmethod
    def _pub2addr(key, main=True):
        def enc(key, ad):
            key = ad + binascii.hexlify(key)
            hash_key = binascii.unhexlify(key)
            checksum = hashlib.sha256(hashlib.sha256(hash_key).digest()).digest()[:4]
            key = key + binascii.hexlify(checksum)
            return base58.b58encode(binascii.unhexlify(key))
        ripemd = hashlib.new('ripemd160')
        ripemd.update(hashlib.sha256(binascii.unhexlify(key)).digest())
        key = ripemd.digest()
        ad = b"00" if main else b"6F"
        addr = enc(key,ad)
        return addr

    @staticmethod
    def _priv2signkey(priv):
        signkey = ecdsa.SigningKey.from_string(priv, curve=ecdsa.SECP256k1)
        return signkey
    
    @staticmethod
    def _priv2verkey(priv):
        s = ecdsa.SigningKey.from_string(priv, curve=ecdsa.SECP256k1)
        k = s.get_verifying_key()
        return k

    @staticmethod
    def _compress_pub(key):
        l = len(key)
        assert l==128, "key length wrong: %i" % l
        x = key[:int(l/2)]
        y = key[int(l/2):]
        assert len(x)==int(l/2) and len(y)==int(l/2), "x and y wrong length!"
        if int(binascii.hexlify(y))%2:
            return b"03" + x
        else:
            return b"02" + x

    @staticmethod
    def _encrypt(key, ad):
        key = ad + binascii.hexlify(key)
        hash_key = binascii.unhexlify(key)
        checksum = hashlib.sha256(hashlib.sha256(hash_key).digest()).digest()[:4]
        key = key + binascii.hexlify(checksum)
        return base58.b58encode(binascii.unhexlify(key))

    @staticmethod
    def _priv2wif(key, main=True, compress=False):
        def enc(key, ad, c):
            key = ad + key + c #binascii.hexlify(key) + c
            hash_key = binascii.unhexlify(key)
            checksum = hashlib.sha256(hashlib.sha256(hash_key).digest()).digest()[:4]
            key = key + binascii.hexlify(checksum)
            return base58.b58encode(binascii.unhexlify(key))
        c = b"01" if compress else b""
        if main:
            return enc(key, b"80", c)
        else:
            return enc(key, b"EF", c)

    @staticmethod
    def _wif2priv(wif):
        #print(str(wif, 'ascii')[0])
        ad = base58.b58decode_check(wif)
        #print(str(binascii.hexlify(ad), 'ascii'))
        if str(wif,'ascii')[0]=='K' or str(wif,'ascii')[0]=='L':
            #print('Compressed wif!')
            #return binascii.hexlify(ad[1:-1])
            return ad[1:-1]
        else:
            #print('Not Compressed wif!')
            #return binascii.hexlify(ad[1:])
            return ad[1:]



## TESTS ##
priv = '164C0EA5314F63D2BF5FD7DCD387E66ABD0B0DB360032A9E2232E71E51F8565A'
wif1 = '5JdFN2jJvC9bCuN4F9i93RkDqBDBqcyinpzBRmnW8xXiXsnGmHT'
wif2 = 'L1uyy5qTuGrVXrmrsvHWHgVzW9kKdrp27wBC7Vs6nZDTF2BRUVwy'
pub = identity.priv2pub(priv=priv)
'''
# test priv2wif
w = identity.priv2wif(priv)
print("testing priv2wif:", w)
# test priv2pub
print("testing priv2pub with priv:", identity.priv2pub(priv=priv))
print("testing priv2pub with wif:", identity.priv2pub(wif=w))
# test priv2pub_compressed
print("testing priv2pub_compress with priv:", identity.priv2pub_compress(priv=priv))
print("testing priv2pub_compress with wif:", identity.priv2pub_compress(wif=w))
# test priv2addr
print("testing priv2addr with priv:", identity.priv2addr(priv=priv))
print("testing priv2addr with wif:", identity.priv2addr(wif=w))
# test priv2addr_compressed
print("testing priv2addr_compress with priv:", identity.priv2addr_compress(priv=priv))
print("testing priv2addr_compress with w:", identity.priv2addr_compress(wif=w))
# test pub2addr
print("testing pub2addr with 0x04:", identity.pub2addr(pub))
print("testing pub2addr without 0x04:", identity.pub2addr(pub[2:]))
# test pub2addr_compressed
print("testing pub2addr_compress with 0x04:", identity.pub2addr_compress(pub))
print("testing pub2addr_compress without 0x04:", identity.pub2addr_compress(pub[2:]))

# test priv2wif
p = identity.wif2priv(wif2)
print("testing wif2priv compress:", p)
w = '5JsyQainyFU5CXJsGcdpRArcggbHTUbfmcqXcTUfU62v56VK5La'
p2 = identity.wif2priv(w)
print("testing wif2priv not-comp:", p2)
pub = identity.priv2pub(wif=w)
# test priv2pub
print("testing priv2pub with priv:", identity.priv2pub(priv=p2))
print("testing priv2pub with wif:", identity.priv2pub(wif=w))
# test priv2pub_compressed
print("testing priv2pub_compress with priv:", identity.priv2pub_compress(priv=p2))
print("testing priv2pub_compress with wif:", identity.priv2pub_compress(wif=w))
# test priv2addr
print("testing priv2addr with priv:", identity.priv2addr(priv=p2))
print("testing priv2addr with wif:", identity.priv2addr(wif=w))
# test priv2addr_compressed
print("testing priv2addr_compress with priv:", identity.priv2addr_compress(priv=p2))
print("testing priv2addr_compress with w:", identity.priv2addr_compress(wif=w))
# test pub2addr
print("testing pub2addr with 0x04:", identity.pub2addr(pub))
print("testing pub2addr without 0x04:", identity.pub2addr(pub[2:]))
# test pub2addr_compressed
print("testing pub2addr_compress with 0x04:", identity.pub2addr_compress(pub))
print("testing pub2addr_compress without 0x04:", identity.pub2addr_compress(pub[2:]))


p = identity.wif2priv(wif2)
# test priv2signkey
print("testing priv2signkey with priv:", identity.priv2signkey(priv=p))
print("testing priv2signkey with wif:", identity.priv2signkey(wif=wif2))
# test priv2verkey
print("testing priv2verkey with priv:", identity.priv2verkey(priv=p))
print("testing priv2verkey with wif:", identity.priv2verkey(wif=wif2))

'''
data = "This is a bunch of test data."
w = identity.priv2wif(priv)
p = identity.wif2priv(w)
print("original priv:",priv)
print("priv2wif :",w)
print("back to priv:",p)

s = identity.priv2signkey(priv=priv)
v = identity.priv2verkey(priv=priv)
# test signdata() and verifydata()
signed = identity.signdata(data=data, signkey=s)
start_time = time.time()
result = identity.verifydata(sigdata=signed, origdata=data, verkey=v)
end_time = time.time()
print("Result: %s, time elapsed: %f" %(result, end_time-start_time))
'''
signed = identity.signdata(data=data, priv=priv)
print("testing signdata with priv:", identity.signdata(data=data, priv=priv))
print("testing verifydata with priv:", identity.verifydata(sigdata=signed, origdata=data, priv=priv))
print("testing verifydata with priv:", identity.verifydata(sigdata=signed, origdata=data, verkey=v))
signed = identity.signdata(data=data, wif=w)
print("testing signdata with w:", identity.signdata(data=data, wif=w))
print("testing verifydata with w:", identity.verifydata(sigdata=signed, origdata=data, wif=w))
print("testing verifydata with priv:", identity.verifydata(sigdata=signed, origdata=data, verkey=v))
signed = identity.signdata(data=data, signkey=s)
print("testing verifydata with verkey:", identity.verifydata(sigdata=signed, origdata=data, verkey=v))
'''