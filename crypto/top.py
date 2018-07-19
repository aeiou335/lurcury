from identity import identity

unit = identity()
unit.init_priv(wif="5KUEwxHXTyWPoE6SLeomvqUQmN6o63Hzu7YFC9K6A4NKXh75QCr")
print("private key: ", unit.get_privkey())
print("private wif: ", unit.get_wifkey())
pb = unit.get_pubkey()
print("public key: ", pb)#unit.get_pubkey())
print("address:", unit.get_addr())
#sig = unit.sign_data(data)
