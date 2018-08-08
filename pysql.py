import pymssql 
import pickle
import time 
import datetime 
import json 
def updateBlockStatus(conn, _hash, blockNum, parentHash, tx, _type): 
    u0SQL = "INSERT [dbo].[{}_block] ( [hash], [blocknumber], [parenthash], [transactions]) VALUES (%s, %d, %s, %s)".format(_type)
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
    u0SQL = "INSERT [dbo].[btc_transaction_vout] ( [txid], [value], [n]) VALUES (%s, %d, %d)"
    cur = conn.cursor()
    cur.execute(u0SQL, (txid, value, n))
    conn.commit()

def updateEthTxStatus(conn, blockHash, blockNumber, _from, gas, gasPrice, _hash, _input, nonce, to, value, _type):
    u0SQL = "INSERT [dbo].[{}_transaction] ( [blockhash], [blocknumber], [from], [gas], [gasprice], [hash], \
            [input], [nonce], [to], [value]) VALUES (%s, %d, %s, %d, %d, %s, %s, %d, %s, %s)".format(_type)
    cur = conn.cursor()
    cur.execute(u0SQL, (blockHash, blockNumber, _from, gas, gasPrice, _hash, _input, nonce, to, value))
    conn.commit()

def updateEthTxReStatus(conn, blockHash, blockNumber, contractAddress, cumulativeGasUsed, _from, gasUsed, logs, logsBloom, to, transactionHash, transactionIndex, _type):
    u0SQL = "INSERT [dbo].[{}_transactionReceipt] ( [blockhash], [blocknumber], [contractaddress], [cumulativegasused], [from], [gasused], [logs], [logsbloom], [to],\
             [transactionhash], [transactionindex]) VALUES (%s, %d, %s, %d, %s, %d, %s, %s, %s, %s, %d)".format(_type)
    cur = conn.cursor()
    cur.execute(u0SQL, (blockHash, blockNumber, contractAddress, cumulativeGasUsed, _from, gasUsed, logs, logsBloom, to, transactionHash, transactionIndex))
    conn.commit()

def sqlcon(sqlhost,sqluser,sqlpassword,sqldatabase): 
    conn=pymssql.connect(host=sqlhost,user=sqluser,password=sqlpassword,database=sqldatabase) 
    cur=conn.cursor(); 
    if not cur: 
        raise Exception('f') 
    return (cur,conn) 

def selectBlockStatus(conn):
    cur = conn.cursor() 
    sSQL = "SELECT transactions FROM [dbo].[eth_block]" 
    cur.execute(sSQL) 
    result=cur.fetchall() 
    return result

