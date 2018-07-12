import sys
sys.path.append("./crypto")
from account import Hash_c
print(Hash_c.sha256_string("123"))
#assert hash_c.sha256_string("123") == "ab665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
