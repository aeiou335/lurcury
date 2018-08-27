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
    
    def priv2addr(priv=None, wif=None, main=True):
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = identity._wif2priv(wiff)
        else:
            privkey = binascii.unhexlify(pk)
        verkey = identity._priv2verkey(privkey)
        pubkey = b"04" + binascii.hexlify(verkey.to_string())
        addr = identity._pub2addr(pubkey,main)
        return str(addr, 'ascii')


    def priv2addr_compress(priv=None, wif=None, main=True):
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = identity._wif2priv(wiff)
        else:
            privkey = binascii.unhexlify(pk)
        verkey = identity._priv2verkey(privkey)
        pubkey = binascii.hexlify(verkey.to_string())
        pbc = identity._compress_pub(pubkey)
        addr = identity._pub2addr(pbc,main)
        return str(addr, 'ascii')


    def priv2pub(priv=None, wif=None):
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = identity._wif2priv(wiff)
        else:
            privkey = binascii.unhexlify(pk)
        verkey = identity._priv2verkey(privkey)
        pubkey = b"04" + binascii.hexlify(verkey.to_string())
        return str(pubkey, 'ascii')


    def priv2pub_compress(priv=None, wif=None):
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = identity._wif2priv(wiff)
        else:
            privkey = binascii.unhexlify(pk)
        verkey = identity._priv2verkey(privkey)
        pubkey = binascii.hexlify(verkey.to_string())
        pbc = identity._compress_pub(pubkey)
        return str(pbc, 'ascii')


    def pub2addr(key, main=True):   #input not compressed
        pubkey = b(key) if isinstance(key,str) else key
        if len(pubkey) == 128:
            pubkey = b"04" + pubkey
        addr = identity._pub2addr(pubkey,main=main)      
        return str(addr, 'ascii')


    def pub2addr_compress(key, main=True):    #input not compressed
        pubkey = b(key) if isinstance(key,str) else key
        if len(pubkey) == 130:
            pb_comp = identity._compress_pub(pubkey[2:])
        elif len(pubkey) == 128:
            pb_comp = identity._compress_pub(pubkey)
        else:
            print("error!! key length neither 130 nor 128")
        addr = identity._pub2addr(pb_comp,main=main)      
        return str(addr, 'ascii')


    def compress_pub(key):
        pubkey = b(key) if isinstance(key,str) else key
        if len(pubkey) == 130:
            pb_comp = identity._compress_pub(pubkey[2:])
        elif len(pubkey) == 128:
            pb_comp = identity._compress_pub(pubkey)
        return pb_comp


    def priv2wif(key):
        privkey = b(key) if isinstance(key,str) else key
        wif = identity._priv2wif(privkey)
        return str(wif, 'ascii')


    def priv2wif_compressed(key):
        privkey = b(key) if isinstance(key,str) else key
        wif = identity._priv2wif(privkey,True)
        return str(wif, 'ascii')


    def wif2priv(wif):
        wiff = b(wif) if isinstance(wif,str) else wif
        p = identity._wif2priv(wiff)
        return str(binascii.hexlify(p), 'ascii')
    

    def signdata(priv=None, wif=None, data=None):
        assert data is not None, "no data given!"
        pk = b(priv) if isinstance(priv,str) else priv
        wiff = b(wif) if isinstance(wif,str) else wif
        if pk == None:
            assert wiff is not None, "no keys given!"
            privkey = identity._wif2priv(wiff)
        else:
            privkey = binascii.unhexlify(pk)
        s = identity.priv2pemlong(privkey)
        
        order = 'FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141'
        (r, s) = fecdsa.sign(data, s, fcurve.secp256k1)
        signed = ecdsa.util.sigencode_der(r,s,order)
        return str(binascii.hexlify(signed), 'ascii')

            
    def verifydata(pub=None, verkey=None, sigdata=None, origdata=None):
        assert sigdata is not None, "no signed data given!"
        assert origdata is not None, "no original data given!"
        if pub is not None:
            verkey = identity.pub2vkey(pub)
        
        sigdata = binascii.unhexlify(sigdata)
        order = 'FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141'
        r,s = ecdsa.util.sigdecode_der(sigdata, order)
        return fecdsa.verify((r,s), origdata, verkey, fcurve.secp256k1) 


################## PRIVATE FUNCTIONS ###########################

    def priv2pemlong(priv):
        skey = ecdsa.SigningKey.from_string(priv,curve=ecdsa.SECP256k1)
        skey = skey.to_pem()
        d = b("").join([l.strip() for l in skey.split(b("\n")) if l and not l.startswith(b("-----"))])
        raw_data = binascii.a2b_base64(d)
        p, Q = fasn1.decode_key(raw_data)
        return p

    def pub2vkey(pub):
        key = pub[2:]
        l = len(key)
        assert l==128, "key length wrong: %i" % l
        x = int(key[:int(l/2)],16)
        y = int(key[int(l/2):],16)
        return fpoint.Point(x,y,curve=fcurve.secp256k1)

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

    def _priv2signkey(priv):
        signkey = ecdsa.SigningKey.from_string(priv, curve=ecdsa.SECP256k1)
        return signkey
    
    def _priv2verkey(priv):
        s = ecdsa.SigningKey.from_string(priv, curve=ecdsa.SECP256k1)
        k = s.get_verifying_key()
        return k

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

    def _encrypt(key, ad):
        key = ad + binascii.hexlify(key)
        hash_key = binascii.unhexlify(key)
        checksum = hashlib.sha256(hashlib.sha256(hash_key).digest()).digest()[:4]
        key = key + binascii.hexlify(checksum)
        return base58.b58encode(binascii.unhexlify(key))

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

    def _wif2priv(wif):
        ad = base58.b58decode_check(wif)
        if str(wif,'ascii')[0]=='K' or str(wif,'ascii')[0]=='L':
            return ad[1:-1]
        else:
            return ad[1:]

