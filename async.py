import gevent
from server import *
from run import *
def foo():
    print('Running in foo')
    gevent.sleep(0)
    print('Explicit context switch to foo again')

def bar():
    print('Explicit context to bar')
    gevent.sleep(0)
    print('Implicit context switch back to bar')
def run3():
    print(456)
    gevent.sleep(10)
    lurcury.main()
def run2():
    print("##################################################123")
    Server_run.run()

gevent.joinall([
    gevent.spawn(run2),
    gevent.spawn(run2),
    gevent.spawn(foo),
    gevent.spawn(bar),
])
