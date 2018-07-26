import threading
from run import *
from server import *

def lurcurymain():
    lurcury.main()    

def servermain():
    Server_run.run()

t1 = threading.Thread(target=lurcurymain)
t1.start()

t2 = threading.Thread(target=servermain)
t2.start()

