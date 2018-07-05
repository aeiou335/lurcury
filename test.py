import sys
sys.path.append("./")
from key import hash_c
from account import *
from core import *
print(hash_c.sha256_string("123"))
#assert hash_c.sha256_string("123") == "ab665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
print(Account.generator_v1())
print(Genesis.genesis())
