import time, random, importlib, json, sys, os
from pathlib import Path
path = str(Path(__file__).parent).split('Blockchain_System')[0]

MINERS = [i for i in os.listdir(os.path.join(path, 'Blockchain_System')) if i.startswith('Miner')]
for m in MINERS:
    sys.path.insert(0, os.path.join(path, 'Blockchain_System', m))

current_miner = random.randint(0, len(MINERS)-1)
while True:

    print(f"\nCurrent Miner : {current_miner}")
    time.sleep(10)

    # Call the current_miner's MINE method : Take unrecorded transactions from all Miners and write into block
    miner = importlib.import_module(MINERS[current_miner])
    unrecorded_transactions = []
    for m in MINERS:
        txn_list = json.load(open(os.path.join(path, 'Blockchain_System', m, 'transactions.json')))
        if len(txn_list) > 0:
            for txn in txn_list:
                if txn['recorded'] == False:
                    unrecorded_transactions.append(txn)
                    txn['recorded'] = True
            with open(os.path.join(path, 'Blockchain_System', m, 'transactions.json'), 'w') as f:
                json.dump(txn_list, f, indent=4, separators=(',', ':'))

    if len(unrecorded_transactions) > 0:
        new_block = miner.Miner().mine_block(unrecorded_transactions)
        print("Block mined")

        # Call every other miner's update_blockchain method : Read the current_miner folder's blockchain.json and write the last block
        checklist = [0 for _ in range(len(MINERS))]
        for m in range(len(MINERS)):
            if MINERS[m] == current_miner:
                checklist[m] = 1
                continue
            miner = importlib.import_module(MINERS[m])
            checklist[m] = miner.Miner().verifyBlock(new_block)

        if sum(checklist) > int(len(MINERS) * 0.75):
            for m in MINERS:
                miner = importlib.import_module(m)
                miner.Miner().updateBlockchain(new_block)
            print("Block accepted")

        current_miner = (current_miner + 1) % len(MINERS)
    else:
        print("No new Transactions in last 10 seconds. Retaining Miner.")