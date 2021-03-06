## Conversion from key to address ##
'''
    Functions:
        - priv2addr (cls, priv=None, wif=None, main=True)
        - priv2addr_compress (cls, priv=None, wif=None, main=True)
        - priv2pub (cls, priv=None, wif=None)
        - priv2pub_compress (cls, priv=None, wif=None)
        - pub2addr (cls, key, main=True)
        - pub2addr_compress (cls, key, main=True)
        - compress_pub (cls, key)
        - priv2wif (cls, key)
        - priv2wif_compressed (cls, key)
        - wif2priv (cls, wif)
        - signdata (cls, priv=None, wif=None, data=None)
        - verifydata (cls, pub=None, verkey=None, sigdata=None, origdata=None)

    Usage notes:
        1. For signdata(), input can be private key in hex or wif format. It will be converted
        with library fastecdsa to generate a priv key in long format compatible to the 
        signing function. The output is a concatenated string "int(r)"+"int(s)"
        
        2. Similarly, for verifydata(), the input pubkey(uncompressed format 0x40....) will be converted 
        to a fastecdsa.VerifyingKey for the verify function. The original data(origdata) is a string(message) and the 
        signature (sigdata) is the output of signdata(), which is a string "r,s"
        
        3. All other functions accept input as strings and output strings
        
        4. The pubkey inputs to pub2addr() and pub2addr_compress() should be uncompressed
        with b"04" in front of it.
        
        5. There is a parameter main in pub2addr() and pub2addr_compress()
        which indicates where the address corresponds to the mainnet. It defaults to true.

        ** Signing & Verifying **

        pub = identity.priv2pub(priv=priv)                                      # create public key from private key
        signed = identity.signdata(data=data, priv=priv)                        # sign data with privkey, returns signature string
        result = identity.verifydata(sigdata=signed, origdata=data, verkey=v)   # verify data with pubkey, signature, and original data
        print("Result: %s" %(result))

'''
import os
import hashlib
import base58
import ecdsa
import binascii
from six import b
from fastecdsa import asn1 as fasn1
from fastecdsa import point as fpoint
from fastecdsa import ecdsa as fecdsa
from fastecdsa import curve as fcurve


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
    def signdata(cls, priv=None, wif=None, data=None):
        assert data is not None, "no data given!"
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = cls._wif2priv(wiff)
        else:
            privkey = binascii.unhexlify(pk)
        s = cls.priv2pemlong(privkey)
        
        order = 'FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141'
        (r, s) = fecdsa.sign(data, s, fcurve.secp256k1)
        signed = ecdsa.util.sigencode_der(r,s,order)
        return str(binascii.hexlify(signed), 'ascii')

            
    @classmethod
    def verifydata(cls, pub=None, verkey=None, sigdata=None, origdata=None):
        assert sigdata is not None, "no signed data given!"
        assert origdata is not None, "no original data given!"
        if pub is not None:
            verkey = cls.pub2vkey(pub)
        
        sigdata = binascii.unhexlify(sigdata)
        order = 'FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141'
        r,s = ecdsa.util.sigdecode_der(sigdata, order)
        return fecdsa.verify((r,s), origdata, verkey, fcurve.secp256k1) 


################## PRIVATE FUNCTIONS ###########################
    @staticmethod
    def priv2pemlong(priv):
        skey = ecdsa.SigningKey.from_string(priv,curve=ecdsa.SECP256k1)
        skey = skey.to_pem()
        d = b("").join([l.strip() for l in skey.split(b("\n")) if l and not l.startswith(b("-----"))])
        raw_data = binascii.a2b_base64(d)
        p, Q = fasn1.decode_key(raw_data)
        return p

    @staticmethod
    def pub2vkey(pub):
        key = pub[2:]
        l = len(key)
        assert l==128, "key length wrong: %i" % l
        x = int(key[:int(l/2)],16)
        y = int(key[int(l/2):],16)
        return fpoint.Point(x,y,curve=fcurve.secp256k1)

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
            key = ad + key + c
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
        ad = base58.b58decode_check(wif)
        if str(wif,'ascii')[0]=='K' or str(wif,'ascii')[0]=='L':
            return ad[1:-1]
        else:
            return ad[1:]
