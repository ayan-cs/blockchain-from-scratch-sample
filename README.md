# Blockchain implementation (Sample Demo)

This is my solution of Blockchain implementation for the fulfillment of Assignment-1 of the course **Introduction to Blockchain** *(Instructor : Dr. Debashis Das; Run : Fall 2022).*

### Miner(s)

For adding Miner(s), follow these steps :
- Copy and paste any of the Miners' folder and edit the `Miner_x.py` file in the appropriate places. Replace `x` with suitable number.
- Remove all Users and Transactions from `users.json` and `transactions.json` files respectively. Keep the `all_users.json` and `blockchain.json` unchanged.
- Make necessary changes in Miner's number in `verify_selection_thread.py` file.

### Leader Selection

For leader selection, a separate `leader_selection_thread.py` has been written. Run this program in a separate Terminal/CMD and leave it running infinitely. The main functionalities of this code are -
- Initialize Leader Miner
- Collect all unrecorded transactions in the whole network
- Mine block by following all protocols (e.g. proper PoW, timestamp etc.)
- Get the block verified from other Miners
- If the acceptance is more than 75%, add the block in the blockchain