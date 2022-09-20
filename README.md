# Blockchain Implementation (Sample Demo)

This is my solution of Blockchain implementation for the fulfillment of Assignment-1 of the course **Introduction to Blockchain** *(Instructor : Dr. Debashis Das; Run : Fall 2022).*

### Miner(s)

For adding Miner(s), follow these steps :
- Copy and paste any of the Miners' folder and edit the `Miner_x.py` file in the appropriate places. Replace `x` with suitable number.
- Remove all Users and Transactions from `users.json` and `transactions.json` files respectively. Keep the `all_users.json` and `blockchain.json` unchanged.
- Make necessary changes in Miner's number in `verify_chain_thread.py` file.

### Leader Selection

For leader selection, a separate `leader_selection_thread.py` has been written. Run this program in a separate Terminal/CMD and leave it running infinitely. The main functionalities of this code are -
- Initialize Leader Miner
- Collect all unrecorded transactions in the whole network
- Mine block by following all protocols (e.g. proper PoW, timestamp etc.)
- Get the block verified from other Miners
- If the acceptance is more than 75%, add the block in the blockchain

### User Operations

This is a Menu Driven code from the perspective of an End User. The user has to register using a unique username and use that to perform various operations (mainly, transactions with other users in the network) through this.

## Instructions for Execution

- Open one terminal/CMD for each of the Miners and start executing `verify_chain_thread.py`. This will keep on verifying the existing blockchain for malicious/altered blocks at a certain interval.
- Open one terminal/CMD and start executing `leader_selection_thread.py`. This will keep on assigning Mining workload on each of the miners in a sequential manner.
- Open a Terminal/CMD and start executing `UserOperations.py`. From here, you can register yourself as a user. Add multiple users in the network and perform some transactions. You can see the changes to be reflected on the corresponding files inside Miners' folders.
