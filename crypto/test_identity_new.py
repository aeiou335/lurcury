from identity_new import identity
import time

## TESTS ##
priv = '164C0EA5314F63D2BF5FD7DCD387E66ABD0B0DB360032A9E2232E71E51F8565A'
wif1 = '5JdFN2jJvC9bCuN4F9i93RkDqBDBqcyinpzBRmnW8xXiXsnGmHT'
wif2 = 'L1uyy5qTuGrVXrmrsvHWHgVzW9kKdrp27wBC7Vs6nZDTF2BRUVwy'
pub = identity.priv2pub(priv=priv)

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


data = "I want to go to disneyland. Does it matter what I put into this string? Hmm apparently not. But verification time getslonger and longer and longer and longer."
w = identity.priv2wif(priv)
p = identity.wif2priv(w)
print("original priv:",priv)
print("priv2wif :",w)
print("back to priv:",p)

start_time = time.time()
vk = identity.priv2pub(priv=priv)
vk = identity.priv2pub(wif=w)
end_time = time.time()
print("priv2pub, time elapsed: %f" %(end_time-start_time))

start_time = time.time()
signed1 = identity.signdata(data=data, wif=w)
end_time = time.time()
print("signed data: %s" %signed1)
print("Sign, time elapsed: %f" %(end_time-start_time))

start_time = time.time()
signed2 = identity.signdata(data=data, priv=priv)
end_time = time.time()
print("Sign, time elapsed: %f" %(end_time-start_time))

start_time = time.time()
result = identity.verifydata(sigdata=signed1, origdata=data, pub=vk)
end_time = time.time()
print("Result: %s, time elapsed: %f" %(result, end_time-start_time))

start_time = time.time()
result = identity.verifydata(sigdata=signed2, origdata=data, pub=vk)
end_time = time.time()
print("Result: %s, time elapsed: %f" %(result, end_time-start_time))
