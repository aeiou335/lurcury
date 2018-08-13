import tornado.web
from testmodel import *
def make_app():
    return tornado.web.Application([
        (r"/getAccount/", getAccountHandler),
        #(r"/dog", DogHandler),
        #(r"/transactioninfo", HashHandler),
        #(r"/addressinfo",AddressHandler)
    ])

