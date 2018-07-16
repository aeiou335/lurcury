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
    def __init__(self, private_key=None, wif=None):      #bin=False
        if private_key is None:
            assert(wif is not None),"Missing argument: key!"
            self.privkey_wif = wif
            self.privkey = self.wif2privkey()
        else:
            self.privkey = private_key
            if wif is None: 
                self.privkey_wif = self.privkey2wif() 
            else:
                self.privkey_wif = wif
        '''if bin:
            self.privkey = private_key
        else:
            self.privkey = binascii.hexlify(private_key.encode('ascii'))'''

        self.signkey = ecdsa.SigningKey.from_string(self.privkey, curve=ecdsa.SECP256k1)
        self.verkey = self.signkey.get_verifying_key()
        self.pubkey = binascii.hexlify(self.verkey.to_string()) #pubkey
        #self.pubkey = b"04" + self.verkey #binascii.hexlify(self.verkey.to_string())
        self.addr = self.pubkey2addr()

    def sign_data(self, data):
        data = b(data)
        return binascii.hexlify(self.signkey.sign(data))

    def verify_data(self, sig_data, orig_data):
        sig_data = binascii.unhexlify(sig_data)
        orig_data = b(orig_data)
        return self.verkey.verify(sig_data, orig_data)
    
    def pubkey2addr(self):
        pubkey = b"04" + self.pubkey
        ripemd = hashlib.new('ripemd160')
        ripemd.update(hashlib.sha256(binascii.unhexlify(pubkey)).digest())
        key = ripemd.digest()
        return self.encrypt(key, b"00")

    def privkey2wif(self):
        return self.encrypt(self.privkey, b"80")

    def wif2privkey(self):
        return base58.b58decode_check(self.privkey_wif)[1:]

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

    def get_pubkey(self):
        return str(self.pubkey, 'ascii')#str(binascii.hexlify(self.verkey.to_string()), 'ascii')

    def get_addr(self):
        return str(self.addr, 'ascii')


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
    pk = b'5JdFN2jJvC9bCuN4F9i93RkDqBDBqcyinpzBRmnW8xXiXsnGmHT'
    data = "this is a bunch of test messages"
    unit = identity(wif=pk)
    print("private key: ", unit.get_privkey())
    print("private wif: ", unit.get_wifkey())
    print("public key: ", unit.get_pubkey())
    print("address:", unit.get_addr())
    sig = unit.sign_data(data)
    print("signed data: ", str(sig, 'ascii'))
    print("verifying: ", unit.verify_data(sig, data))

    # test2: input 32 bytes string
    '''
    pk = 'this is my key!!'
    unit = identity(pk, bin=False)
    print("private key: ", unit.get_privkey())
    print("public key: ", unit.get_pubkey())
    print("address:", unit.get_addr())'''
