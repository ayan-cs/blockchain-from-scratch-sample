import json, time, os, pathlib, importlib
from Miner_4 import Miner # Change here for other Miners

while True:
    time.sleep(5)
    if Miner().verifyBlockchain() != 1:
        print("BLOCKCHAIN VERIFICATION FAILED")
    else:
        print(f"Verification Successful at {time.ctime()}")