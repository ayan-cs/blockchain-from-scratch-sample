import os, shutil, pickle, codecs, json, sys, importlib, time, hashlib, rsa
from pathlib import Path

class User :
    def __init__(self, miner):
        self.miner = miner
        self.wallet = {'publicKey' : None, 'privateKey' : None, 'address' : None, 'wallet' : 0}
        self.wallet['publicKey'], self.wallet['privateKey'] = rsa.newkeys(1024)
        self.wallet['address'] = hashlib.sha256(str(self.wallet['publicKey']).encode()).hexdigest()

class Miner:
    def __init__(self):

        path = str(Path(__file__).parent).split('Blockchain_System')[0]
        self.miners = [i for i in os.listdir(os.path.join(path, 'Blockchain_System')) if i.startswith('Miner')]
        for m in self.miners:
            sys.path.insert(0, os.path.join(path, 'Blockchain_System', m))

        if os.path.exists(os.path.join(path, 'Blockchain_System', 'Miner_1', 'blockchain.json')) == False:
            path = str(Path(__file__).parent).split('Blockchain')[0]
            
            f_prev = os.path.join(path, self.miners[-1], 'blockchain.json')
            f_curr = os.path.join(path, f"Miner_{int(self.miners[-1].split('_')[1])+1}", 'blockchain.json')

            shutil.copy(f_prev, f_curr)
        
        self.path = os.path.join(str(Path(__file__).parent).split('Miner_1')[0], 'Miner_1') # Change here for other Miners
        self.all_users = 'all_users.json'
        self.users = 'users.json'
        self.txn_path = 'transactions.json'
        self.blockchain = 'blockchain.json'
    
    def makeTransacton(self, sender, receiver, amount):
        with open(os.path.join(self.path, self.all_users), 'r') as f:
            all_users = json.load(f)
        with open(os.path.join(self.path, self.users), 'r') as f:
            users = json.load(f)

        sender_uname = sender
        receiver_uname = receiver

        try :
            sender = pickle.loads(codecs.decode(users[0][sender_uname]['user_object'].encode(), 'base64'))
        except KeyError:
            print("User not registered with this Miner! Transaction aborted!")
            return 0
        
        try:
            receiver = pickle.loads(codecs.decode(all_users[0][receiver_uname]['user_object'].encode(), 'base64'))
        except KeyError:
            print(f"Receiver not found! Transaction aborted!")
            return 0

        if users[0][sender_uname]['balance'] < amount:
            print(f"Sender does not have enough balance! Transaction aborted!")
        else:
            new_txn = {'sender' : sender_uname, 'receiver' : receiver_uname, 'amount' : amount, 'timestamp' : time.ctime(), 'recorded' : False}

            # Create serialized object and sign that. Verify sign from other Miners using receiver's pubkey.
            sign = rsa.sign(pickle.dumps(new_txn), sender.wallet['privateKey'], 'SHA-1')
            message = {'new_txn' : new_txn, 'signature' : sign}

            recv_miner = all_users[0][receiver_uname]['miner']
            print(receiver_uname, recv_miner)
            recv_miner = importlib.import_module(recv_miner)
            status = recv_miner.Miner().verifyTransaction(message)

            if status == True:
            
                new_txn = {'sender' : sender.wallet['address'], 'receiver' : receiver.wallet['address'], 'amount' : amount, 'timestamp' : time.ctime(), 'recorded' : False}
                with open(os.path.join(self.path, self.txn_path), 'r') as f:
                    txn_list = json.load(f)
                txn_list.append(new_txn)
                
                with open(os.path.join(self.path, self.txn_path), 'w') as f:
                    json.dump(txn_list, f, indent=4, separators=(',', ':'))
                
                users[0][sender_uname]['balance'] -= amount
                all_users[0][sender_uname]['balance'] -= amount
                all_users[0][receiver_uname]['balance'] += amount
                
                with open(os.path.join(self.path, self.all_users), 'w') as f:
                    json.dump(all_users, f, indent=4, separators=(',', ':'))
                with open(os.path.join(self.path, self.users), 'w') as f:
                    json.dump(users, f, indent=4, separators=(',', ':'))
                
                # update all Miners
                for miner in self.miners:
                    if miner == "Miner_1":
                        continue
                    m_obj = importlib.import_module(miner)
                    m_obj.Miner().updateUserlist('all_users', all_users)
                    if miner == all_users[0][receiver_uname]['miner']:
                        m_obj = importlib.import_module(miner)
                        m_obj.Miner().updateUserlist('users')
                return 1
            
            else:
                print("Transaction could not be verified! Transaction aborted!")
                return 0    
    
    def verifyTransaction(self, message):
        sender = message['new_txn']['sender']
        signature = message['signature']
        all_users = json.load(open(os.path.join(self.path, self.all_users), 'r'))
        
        sender_object = pickle.loads(codecs.decode(all_users[0][sender]['user_object'].encode(), 'base64'))
        sender_key = sender_object.wallet['publicKey']

        try :
            return rsa.verify(pickle.dumps(message['new_txn']), signature, sender_key) == 'SHA-1'
        except :
            return False

    def mine_block(self, txn_list):

        def proof_of_work(last_nonce):
            new_nonce = 1
            valid = False
            while valid == False:
                new_hash = hashlib.sha256(str(new_nonce**2 - last_nonce**2).encode()).hexdigest()
                if str(new_hash)[:4] == '0000':
                    valid = True
                else:
                    new_nonce += 1
            return new_nonce
        
        def createMerkleRoot(txn_list):
            serialised = codecs.encode(pickle.dumps(txn_list), 'base64').decode()
            return hashlib.sha256(serialised.encode()).hexdigest()
        
        def createHash(block):
            serialised = codecs.encode(pickle.dumps(block), 'base64').decode()
            return hashlib.sha256(serialised.encode()).hexdigest()

        chain = json.load(open(os.path.join(self.path, self.blockchain), 'r'))
        if len(chain) < 1:
            new_block = {
                'timestamp' : time.ctime(),
                'data_root' : createMerkleRoot(txn_list),
                'nonce' : 1,
                'previous_hash' : '0000'
            }
        else:
            last_block = chain[-1]
            new_block = {
                'timestamp' : time.ctime(),
                'data_root' : createMerkleRoot(txn_list),
                'nonce' : proof_of_work(last_block['nonce']),
                'previous_hash' : createHash(last_block)
            }
        return new_block

    def verifyBlock(self, block):
        chain = json.load(open(os.path.join(self.path, self.blockchain), 'r'))

        if len(chain) > 0:
            prev_block = chain[-1]
            if hashlib.sha256(str(block['nonce']**2 - prev_block['nonce']**2).encode()).hexdigest()[:4] != '0000':
                print("PoW False")
                return 0
            if block['previous_hash'] != hashlib.sha256(str(codecs.encode(pickle.dumps(prev_block), 'base64').decode()).encode()).hexdigest():
                print("Prev Hash False")
                return 0
            return 1
        else:
            return 1

    def updateBlockchain(self, new_block):
        if self.verifyBlock(new_block) :
            chain = json.load(open(os.path.join(self.path, self.blockchain), 'r'))
            chain.append(new_block)
            with open(os.path.join(self.path, self.blockchain), 'w') as f:
                json.dump(chain, f, indent=4, separators=(',', ':'))

    def verifyBlockchain(self):
        chain = json.load(open(os.path.join(self.path, self.blockchain), 'r'))
        if len(chain) > 1:
            for i in range(1, len(chain)):
                prev_block = chain[i-1]
                block = chain[i]
                if hashlib.sha256(str(block['nonce']**2 - prev_block['nonce']**2).encode()).hexdigest()[:4] != '0000':
                    print("PoW False")
                    return 0
                if block['previous_hash'] != hashlib.sha256(str(codecs.encode(pickle.dumps(prev_block), 'base64').decode()).encode()).hexdigest():
                    print("Prev Hash False")
                    return 0
            return 1
        elif len(chain) > 0:
            prev_block = chain[-1]
            if hashlib.sha256(str(block['nonce']**2 - prev_block['nonce']**2).encode()).hexdigest()[:4] != '0000':
                print("PoW False")
                return 0
            if block['previous_hash'] != hashlib.sha256(str(codecs.encode(pickle.dumps(prev_block), 'base64').decode()).encode()).hexdigest():
                print("Prev Hash False")
                return 0
            return 1
        else:
            print("Blockchain empty!")
            return 1

    def updateUserlist(self, lname, new_list=None):
        if lname=='all_users':
            with open(os.path.join(self.path, self.all_users), 'w') as f:
                json.dump(new_list, f, indent=4, separators=(',', ':'))
        if lname=='users':
            all_users = json.load(open(os.path.join(self.path, self.all_users), 'r'))
            my_users = json.load(open(os.path.join(self.path, self.users), 'r'))
            
            for user in all_users[0].keys():
                if user in my_users[0].keys():
                    my_users[0][user] = all_users[0][user]
            
            with open(os.path.join(self.path, self.users), 'w') as f:
                json.dump(my_users, f, indent=4, separators=(',', ':'))