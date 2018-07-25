## Conversion from key to address ##
import os
import hashlib
import base58
import ecdsa
import binascii
from six import b

class identity:
    """ 
    Class with keys and encoded address. 
    Must be initialized with private_key(hex or wif format).
    """
    def __init__(self, priv=None, pub=None, wif=None, addr=None, addr_c=None):
        self.privkey = b(priv) if isinstance(priv,str) else priv
        self.privkey_wif = b(wif) if isinstance(wif,str) else wif
        self.pubkey = b(pub) if isinstance(pub,str) else pub
        self.pub_compressed = None
        self.addr = b(addr) if isinstance(addr,str) else addr
        self.addr_compressed = b(addr_c) if isinstance(addr_c,str) else addr_c
        self.signkey = None
        self.verkey = None

    def init_priv(self, private_key=None, wif=None):
        if private_key is None:
            assert(wif is not None),"Missing argument: key!"
            self.privkey_wif = b(wif) if isinstance(wif,str) else wif
            self.privkey = self.wif2privkey()
            self.get_privkey()
        else:
            self.privkey = b(private_key) if isinstance(private_key,str) else private_key
            if wif is None: 
                self.privkey_wif = self.privkey2wif() 
            else:
                self.privkey_wif = b(wif) if isinstance(wif,str) else wif

        #key = str(self.privkey)
        self.signkey = ecdsa.SigningKey.from_string(self.privkey, curve=ecdsa.SECP256k1)
        self.verkey = self.signkey.get_verifying_key()
        self.pubkey = b"04" + binascii.hexlify(self.verkey.to_string())
        self.pub_compressed = self.compress_pub()
        #self.pubkey = binascii.hexlify(self.verkey.to_string()) #pubkey ==
        #self.pubkey = b"04" + self.verkey #binascii.hexlify(self.verkey.to_string())
        #self.addr = self.pubkey2addr(self.pubkey.to_string())
        self.pub2addr(self.pubkey)
        self.pub2addr(self.pub_compressed)

    def pub2addr(self, key): 
        #input string/bytes, output string
        pubkey = b(key) if isinstance(key,str) else key
        #pubkey = b"04" + key
        ripemd = hashlib.new('ripemd160')
        ripemd.update(hashlib.sha256(binascii.unhexlify(pubkey)).digest())
        key = ripemd.digest()
        if len(pubkey) == 130:
            print("not compressed!")
            self.addr = self.encrypt(key, b"00")
            return self.get_addr(compressed=False)
        elif len(pubkey) == 66:
            print("is compressed!")
            self.addr_compressed = self.encrypt(key, b"00")
            return self.get_addr(compressed=True)
        else:
            print("Length of key incorrect, must be 130 or 66. Length: %i" % len(pubkey))

    def sign_data(self, data):
        assert (self.signkey is not None), "No private key provided! Init with private key first."
        data = b(data) if isinstance(data, str) else data
        return binascii.hexlify(self.signkey.sign(data))

    def verify_data(self, sig_data, orig_data):
        assert (self.verkey is not None), "No private key provided! Init with private key first."
        sig_data = binascii.unhexlify(sig_data)
        orig_data = b(orig_data)
        return self.verkey.verify(sig_data, orig_data)
    
    def compress_pub(self):
        portion = self.pubkey[2:]
        l = len(portion)
        assert l==128, "portion length wrong: %i" % l
        x = portion[:int(l/2)]
        y = portion[int(l/2):]
        assert len(x)==int(l/2) and len(y)==int(l/2), "x and y wrong length!"
        if int(binascii.hexlify(y))//2:
            return b"02" + x
        else:
            return b"03" + x
    
    '''def pubkey2addr(self):
        pubkey = b"04" + self.pubkey
        ripemd = hashlib.new('ripemd160')
        ripemd.update(hashlib.sha256(binascii.unhexlify(pubkey)).digest())
        key = ripemd.digest()
        return self.encrypt(key, b"00")'''

    def privkey2wif(self):
        return self.encrypt(self.privkey, b"80")

    def wif2privkey(self):
        print(str(self.privkey_wif)[0])
        ad = base58.b58decode_check(self.privkey_wif)
        print(str(binascii.hexlify(ad), 'ascii'))

        if str(self.privkey_wif,'ascii')[0]=='K' or str(self.privkey_wif,'ascii')[0]=='L':
            print('Compressed wif!')
            return ad[1:-1]
        else:
            print('Non-compressed wif!')
            return ad[1:]


    def encrypt(self, key, ad):
        key = ad + binascii.hexlify(key)
        hash_key = binascii.unhexlify(key)
        checksum = hashlib.sha256(hashlib.sha256(hash_key).digest()).digest()[:4]
        key = key + binascii.hexlify(checksum)
        return base58.b58encode(binascii.unhexlify(key))

    def get_keys(self):
        '''Returns key pair and address as tuple'''
        return (binascii.hexlify(self.privkey), self.pubkey, self.addr)  

    def get_privkey(self):
        return str(binascii.hexlify(self.privkey), 'ascii')

    def get_wifkey(self):
        return str(self.privkey_wif, 'ascii')

    def get_pubkey(self,compressed):
        if not compressed:
            return str(self.pubkey, 'ascii')#
        else:
            return str(self.pub_compressed, 'ascii')
        #return str(binascii.hexlify(self.pubkey), 'ascii')

    def get_addr(self,compressed):
        if not compressed:
            return str(self.addr, 'ascii')
        else:
            return str(self.addr_compressed, 'ascii')


# unit tests
if __name__ == "__main__":
    # test1: random generate 32 bytes
    '''pk = os.urandom(32)
    unit = identity(private_key=pk)
    print("private key: ", unit.get_privkey())
    print("private wif: ", unit.get_wifkey())
    print("public key: ", unit.get_pubkey())
    print("address:", unit.get_addr())
    '''
    '''
    pk = '5JdFN2jJvC9bCuN4F9i93RkDqBDBqcyinpzBRmnW8xXiXsnGmHT'
    data = "this is a bunch of test messages"
    unit = identity()
    unit.init_priv(wif=pk)
    print("private key: ", unit.get_privkey())
    print("private wif: ", unit.get_wifkey())
    pb = unit.get_pubkey()
    print("public key: ", pb)#unit.get_pubkey())
    print("address:", unit.get_addr())
    sig = unit.sign_data(data)
    print("signed data: ", str(sig, 'ascii'))
    print("verifying: ", unit.verify_data(sig, data))
    '''
    #wif = 'L1uyy5qTuGrVXrmrsvHWHgVzW9kKdrp27wBC7Vs6nZDTF2BRUVwy'
    #wif = '5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ'
    '''
    unit2 = identity()
    unit2.init_priv(wif=wif)
    addr = unit2.get_addr()
    print("testing new function: ", addr)'''
    # test2: input 32 bytes string
    '''
    pk = 'this is my key!!'
    unit = identity(pk, bin=False)
    print("private key: ", unit.get_privkey())
    print("public key: ", unit.get_pubkey())
    print("address:", unit.get_addr())'''
    unit3 = identity()
    wif = 'L3ChN4SuZpRD4oXgMyDxoVkGzxtroas5D67hdA5EmjZ82Vi9kCas'
    unit3.init_priv(wif=wif)
    print("privkey: %s" %(unit3.get_privkey()))
    pb1 = unit3.get_pubkey(False)
    pb2 = unit3.get_pubkey(True)
    print("not compressed pubkey: %s " %(pb1))
    print("compressed pubkey: %s " %(pb2))
    addr = unit3.get_addr(False)
    print("not compressed address: %s" % addr)
    addr_c = unit3.get_addr(True)
    print("compressed address: %s" % addr_c)
    #unit4 = identity()
    #print(unit4.pub2addr('024C2AA8DAFB4111CC87868E6E34BCBC07D58DD7E704CECB85182385A8E70FC9EB'))