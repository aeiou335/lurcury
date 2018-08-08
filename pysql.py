import pymssql 
import pickle
import time 
import datetime 
import json 
def updateBlockStatus(conn, _hash, blockNum, parentHash, tx): 
    u0SQL = "INSERT [dbo].[btc_block] ( [hash], [blocknumber], [parenthash], [tx]) VALUES (%s, %d, %s, %s)"
    print(u0SQL)
    cur2=conn.cursor() 
    cur2.execute(u0SQL,(_hash, blockNum, parentHash, tx)) 
    conn.commit()

def updateTxStatus(conn, _hex, txid, tranhash, blockhash):
    u0SQL = "INSERT [dbo].[btc_transaction] ( [hex], [txid], [hash], [blockhash]) VALUES (%s, %s, %s, %s)"
    cur = conn.cursor()
    cur.execute(u0SQL, (_hex, txid, tranhash, blockhash))
    conn.commit()

def updateVinStatus(conn, unspendtxid, txid, vin_vout, coinbase):
    u0SQL = "INSERT [dbo].[btc_transaction_vin] ( [unspendtxid], [txid], [vout], [coinbase]) VALUES (%s, %s, %d, %s)"
    cur = conn.cursor()
    cur.execute(u0SQL, (unspendtxid, txid, vin_vout, coinbase))
    conn.commit()

def updateVoutStatus(conn, txid, value, n):
    u0SQL = "INSERT [dbo].[btc_transaction] ( [hex], [txid], [value], [n]) VALUES (%s, %d, %d)"
    cur = conn.cursor()
    cur.execute(u0SQL, (txid, value, n))
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
