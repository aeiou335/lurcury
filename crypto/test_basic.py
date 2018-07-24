from basic import *

import unittest

class CryptoMethods(unittest.TestCase):

    def test_key(self):
        assertEqual(Key_c.bitcoinkey("5KUEwxHXTyWPoE6SLeomvqUQmN6o63Hzu7YFC9K6A4NKXh75QCr"),"d9e06c9441f891458bfe279a444fb93a9d8f961a96be5c561da6ab4a71fcb56e")
        assertEqual(Key_c.publicKey("97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a"),"2b5660eea7f9176cf921de540e8302b8c4981ef620ba5526ece49149c7c0f3e5fb4ea925dd443ec0b354ac7f3b07bf70122ed12c8c228752ca6c1be9a5060173")
        print(Key_c.address("7b83ad6afb1209f3c82ebeb08c0c5fa9bf6724548506f2fb4f991e2287a77090177316ca82b0bdf70cd9dee145c3002c0da1d92626449875972a27807b73b42e"))
        print("ethadd:",Key_c.ethereumaddress(Key_c.publicKey(h)))
    def test_hash():
        print("hash")
    def test_signature():
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()

print(Key_c.bitcoinkey("5KUEwxHXTyWPoE6SLeomvqUQmN6o63Hzu7YFC9K6A4NKXh75QCr"))
h = Key_c.privateKey()
print(h)
print(Key_c.publicKey(h))
t = Key_c.bitcoinaddress(Key_c.publicKey(h))
print(t)
print(Key_c.publicKey("97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a"))
print(Key_c.address("7b83ad6afb1209f3c82ebeb08c0c5fa9bf6724548506f2fb4f991e2287a77090177316ca82b0bdf70cd9dee145c3002c0da1d92626449875972a27807b73b42e"))
print("ethadd:",Key_c.ethereumaddress(Key_c.publicKey(h)))
r = signature_c.sign("123",Key_c.bitcoinkey("5KUEwxHXTyWPoE6SLeomvqUQmN6o63Hzu7YFC9K6A4NKXh75QCr"))

print("r",r)
b = signature_c.verify(str(r),b"123",str(Key_c.publicKey(Key_c.bitcoinkey("5KUEwxHXTyWPoE6SLeomvqUQmN6o63Hzu7YFC9K6A4NKXh75QCr"))))
b = signature_c.verify(str("ef24fcfd466eb8aeaebc9843f1cbd81cd305047306ce71eb1d7062d28565b43266f6286f6789e1c27670cbe2fd0ece3106ff94bc051a03b2f57aa503e08dcab2"),b"000000000000000000000000000001000000000000000000000000000010cic00000000000000000000000000001040cxnIQqsD2gBHcch94c7pQaVLXvHg7USoQmPywn27cic","7b83ad6afb1209f3c82ebeb08c0c5fa9bf6724548506f2fb4f991e2287a77090177316ca82b0bdf70cd9dee145c3002c0da1d92626449875972a27807b73b42e")
print(r)
print(b)

'''
#x = signature_c.sign("blahblah","f8b9fc996979291ac2968faeaedd88cd4c2fbc5611fda0605415e05eafc6658a")
#print(x)
'''
