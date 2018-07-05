
import hashlib
import binascii
'''
class:
    def txdecode(data):
'''        
string = 'txA665A45920422F9D417E4867EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3yx213ix1A665A45920422F9D417E4867EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3kx2a82953d14e4495935fa884ea295b26c3ef877dfb9f8c366943cb1873711dfa42db6fbf1f3c4421c9c6dd95ad1dfafb6vx1pxixA665A45920422F9D417E4867EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3kx2a82953d14e4495935fa884ea295b26c3ef877dfb9f8c366943cb1873711dfa42db6fbf1f3c4421c9c6dd95ad1dfafb6vx1pxox1cx67EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3vx1pxox1cx67EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3vx1pxsx111lx222'


class transaction_decode:
    def ix_decode(data):
        ix_array=[]
        ix = data
        times = data.count("ix")
        for i in range(times):
            ixt = ix.find("ix")
            #print(ix)
            ix2 = ix[(ixt+2):].find("ix")
            ox = ix[(ixt+2):].find("ox")
            #print(ix)
            if(ix2!=-1):
                #
                ix1 = ix[(ixt+2):(ixt+2+ix2)]
                ix_array.append(ix1)
                ix = ix[(ixt+2):]
            elif(ox!=-1):
                ix1 = ix[(ixt+2):(ixt+2+ox)]
                ix_array.append(ix1)
                ix = ix[(ixt+2):]
            else:
                ix1 = ix1 = ix[(ixt+2):]
                ix_array.append(ix1)
        return ix_array
    def yx_decode(data):
        yx = data.find("yx")
        remain = data[yx+2:]
        next_x = remain.find("x")
        return data[yx+2:yx+2+next_x-1]
    def tx_decode(data):
        return data[(data.find("tx")+2):(data.find("tx")+66)]
    #def bx_decode(data):
        
    def ox_decode(data):
        ix_array=[]
        ix = data
        times = data.count("ox")
        for i in range(times):
            ixt = ix.find("ox")
            ix2 = ix[(ixt+2):].find("ox")
            ox = ix[(ixt+2):].find("ox")
            if(ix2!=-1):
                ix1 = ix[(ixt+2):(ixt+ix2+2)]
                ix_array.append(ix1)
                ix = ix[(ixt+2):]
            else:
                sx = ix.find("sx")
                ix1 = ix[(ixt+2):sx]
                ix_array.append(ix1)
        return ix_array
    def ixin_decode(data):
        ix = data
        tx_result = ix[0:63]
        kx = ix.find("kx")
        #px = ix[px+2:]
        vx = ix.find("vx")
        px = ix.find("px")
        #print(kx,vx,px)
        kx_result = ix[kx+2:vx]
        vx_result = ix[vx+2:px]
        px_result = ix[px+2:]
        return {"tx":tx_result,"kx":kx_result,"vx":vx_result,"px":px_result}
    def oxout_decode(data):
        ix = data
        #tx_result = ix[0:63]
        ox = ix.find("ox")
        #px = ix[px+2:]
        vx = ix.find("vx")
        px = ix.find("px")
        #print(kx,vx,px)
        ox_result = ix[ox+2:vx]
        vx_result = ix[vx+2:px]
        px_result = ix[px+2:]
        #print( "go",{"ox":ox_result,"vx":vx_result,"px":px_result})
        return {"ox":ox_result,"vx":vx_result,"px":px_result}
    def result_decode(data):
        ix=transaction_decode.ix_decode(data)
        tx=transaction_decode.tx_decode(data)
        ox=transaction_decode.ox_decode(data)
        yx=transaction_decode.yx_decode(data)
        ix_array = []
        ox_array = []        
        #print("xx",ix,ox)
        for ix_ar in ix:
            ix_content = transaction_decode.ixin_decode(ix_ar)
            ix_array.append(ix_content)
        for or_ar in ox:
            #print("in",transaction_decode.oxout_decode(or_ar))
            ox_content = transaction_decode.oxout_decode(or_ar)
            ox_array.append(ox_content)
            print("out",ox_array)
        return {"tx":tx,"yx":yx,"ix":ix_array,"ox":ox_array}
        #ixin_decode(data)
        #oxout_decode(data)
print(transaction_decode.result_decode(string))
#strings = "1A665A45920422F9D417E4867EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3kx2a82953d14e4495935fa884ea295b26c3ef877dfb9f8c366943cb1873711dfa42db6fbf1f3c4421c9c6dd95ad1dfafb6vx1px"
#strings = "1cx67EFDC4FB8A04A1F3FFF1FA07E998E86F7F7A27AE3vx1px"
#print(transaction_decode.ixin_decode(strings))

