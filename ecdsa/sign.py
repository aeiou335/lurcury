


class sign:
    def signTx(data):
        atom = {'txhash':'tx','block':'yx','in':"ix","out":"ox"}
        result = ""
        print(data.items())
        for key, value in data.items():
            if key=='in' or key=='out' :
                for con in value:
                    result = result+con
            else:
                result = result+value
            #print(key,value)
            #result = result+value
            print(result)
    def signTx_o(data):
        atom = {'txhash':'tx','block':'yx','in':"ix","out":"ox"}
        order = ['txhash','block','in','out']
        result = ""
        re = []
        for key in order: 
            #result = result + str(data[key])
            if key == "in" or key == "out":
                for v in data[key]:
                    result = result + str(v)
            else:
                result = result + str(data[key])
        return result
print(sign.signTx_o({'txhash':'ttt','block':'bbb','in':['iii','ppp'],'out':['ooo','yyy']}))

