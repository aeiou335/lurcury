import pymssql 
import pickle
import time 
import datetime 
import json 
def updateBlockStatus(conn, _hash, height, merkleroot, tx, _time, previousblockhash, difficulty): 
    u0SQL = "INSERT [dbo].[btc_block] ( [hash], [height], [merkleroot], [tx], [time], [previousblockhash], [difficulty]) VALUES (%s, %d, %s, %s, %d, %s, %d)"
    #print(u0SQL)
    cur2=conn.cursor() 
    cur2.execute(u0SQL,(_hash, height, merkleroot, tx, _time, previousblockhash, difficulty)) 
    conn.commit()

def updateTxStatus(conn, txid, _hash, time):
    sql = "INSERT [dbo].[btc_transaction] ([txid], [hash], [time]) VALUES (%s, %s, %d)"
    cur = conn.cursor()
    cur.execute(sql, (txid, _hash, time))
    conn.commit()

def updateVinStatus(conn, unspendtxid, txid, coinbase, vout, scriptSig_asm, scriptSig_hex, sequence):
    sql = "INSERT [dbo].[btc_transaction_vin] ([unspendtxid], [txid], [coinbase], [vout], [scriptSig_asm], [scriptSig_hex], [sequence]) VALUES (%s, %s, %s, %d, %s, %s, %d)"
    cur = conn.cursor()
    cur.execute(sql, (unspendtxid, txid, coinbase, vout, scriptSig_asm, scriptSig_hex, sequence))
    conn.commit()

def updateVoutStatus(conn,txid,value,n,scriptPubKey_asm,scriptPubKey_hex,scriptPubKey_type,scriptPubKey_reqSigs,scriptPubKey_addresses):
    sql = "INSERT [dbo].[btc_transaction_vout] ([txid],[value],[n], [scriptPubKey_asm], [scriptPubKey_hex], [scriptPubKey_type], [scriptPubKey_reqSigs], [scriptPubKey_addresses]) VALUES (%s, %s, %d, %s, %s, %s, %s, %s)"
    cur = conn.cursor()
    cur.execute(sql, (txid,value,n,scriptPubKey_asm,scriptPubKey_hex,scriptPubKey_type,scriptPubKey_reqSigs,scriptPubKey_addresses))
    conn.commit()

def sqlcon(sqlhost,sqluser,sqlpassword,sqldatabase): 
    conn=pymssql.connect(host=sqlhost,user=sqluser,password=sqlpassword,database=sqldatabase) 
    cur=conn.cursor(); 
    if not cur: 
        raise Exception('f') 
    return (cur,conn) 

def selectStatus(cur, table): 
    sSQL = "SELECT * FROM [dbo].[btc_{}]".format(table)
    cur.execute(sSQL) 
    result=cur.fetchall() 
    return result