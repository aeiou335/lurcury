import pymssql 
import pickle
import time 
import datetime 
import json 
def updateBlockStatus(conn, _hash, height, merkleroot, tx, _time, previousblockhash, difficulty): 
    u0SQL = "INSERT [dbo].[btc_block] ( [hash], [height], [merkleroot], [tx], [time], [previousblockhash], [difficulty]) VALUES (%s, %d, %s, %s, %d, %s, %d)"
    print(u0SQL)
    cur2=conn.cursor() 
    cur2.execute(u0SQL,(_hash, height, merkleroot, tx, _time, previousblockhash, difficulty)) 
    conn.commit()   

def sqlcon(sqlhost,sqluser,sqlpassword,sqldatabase): 
    conn=pymssql.connect(host=sqlhost,user=sqluser,password=sqlpassword,database=sqldatabase) 
    cur=conn.cursor(); 
    if not cur: 
        raise Exception('f') 
    return (cur,conn) 

def selectBlockStatus(cur): 
    sSQL = "SELECT * FROM [dbo].[btc_block]" 
    cur.execute(sSQL) 
    result=cur.fetchall() 
    return result
