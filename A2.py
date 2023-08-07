import json, os
import pandas as pd
from pathlib import Path

path = str(Path(__file__).parent).split('Blockchain_System')[0]

def getGenesisBlock(chain):
    all_txn = []
    if len(chain) < 1:
        print("Blockchain is Empty\n")
    else:
        print(f"Genesis Block hash : {chain[0]['block_hash']}")

def showAllTxns(chain):
    all_txn = []
    if len(chain) < 1:
        print("Blockchain is empty\n")
    else:
        for block in chain:
            txn_list = block['transactions']
            for txn in txn_list:
                all_txn.append(pd.Series({'Sender' : txn['sender'], 'Receiver' : txn['receiver'], 'Amount' : txn['amount'], 'Block Id' : txn['block_id']}))
        print(f"{pd.DataFrame(all_txn)}\n")

def getBlockInfo(chain, hashval):
    if len(chain) < 1:
        print("Blockchain is empty\n")
    else:
        for block in chain:
            flag=0
            for i in range(len(hashval)):
                if block['block_hash'][i] == hashval[i]:
                    continue
                else:
                    flag=1
            if flag==0:
                print(f"Required Block : \n{block}\n")
                break

def getLastBlockHeight(chain):
    if len(chain) < 1:
        print("Blockchain is empty\n")
    else:
        last_block = chain[-1]
        print(f"Height of last stored block : {last_block['height']}\n")

def getLastBlock(chain):
    if len(chain) < 1:
        print("Blockchain is empty\n")
    else:
        print(f"Most Recent stored block : {chain[-1]}\n")

def getAvgTxn(chain):
    if len(chain) < 1:
        print("Blockchain is empty\n")
    else:
        total_txn = 0
        for block in chain:
            total_txn += len(block['transactions'])
        print(f"Average number of Transactions : {total_txn/len(chain)}\n")

def getSummary(chain):
    if len(chain) < 6:
        print("There is no block with Height=6\n")
    else:
        block = chain[6]
        total_btc = 0
        for txn in block['transactions']:
            total_btc += txn['amount']
        info = pd.Series({'Block Id' : block['id'], 'No. of Txns' : len(block['transactions']), 'Total BTC' : total_btc})
    print(f"{pd.DataFrame(info)}\n")

if __name__=="__main__":
    with open(os.path.join(path, 'Blockchain_System', 'Miner_0', 'blockchain.json'), 'r') as f:
        chain = json.load(f)

    all_miners = [i for i in os.listdir(os.path.join(path, 'Blockchain_System')) if i.startswith('Miner')]
    all_txn = []
    for miner in all_miners:
        with open(os.path.join(path, 'Blockchain_System', miner, 'transactions.json'), 'r') as f:
            all_txn += json.load(f)
    
    getGenesisBlock(chain)
    
    showAllTxns(chain)
    
    hashval = input("Enter a valid hash value : ")
    getBlockInfo(chain, hashval)

    getLastBlockHeight(chain)

    getLastBlock(chain)

    getAvgTxn(chain)

    getSummary(chain)