import hashlib, json, os, codecs, pickle, sys, time, rsa
from pathlib import Path
import importlib

class User :
    def __init__(self, miner):
        self.miner = miner
        self.wallet = {'publicKey' : None, 'privateKey' : None, 'address' : None, 'wallet' : 0}
        self.wallet['publicKey'], self.wallet['privateKey'] = rsa.newkeys(1024)
        self.wallet['address'] = hashlib.sha256(str(self.wallet['publicKey']).encode()).hexdigest()

def addUser(username):
    path = str(Path(__file__).parent).split('Blockchain_System')[0]
    MINERS = [i for i in os.listdir(os.path.join(path, 'Blockchain_System')) if i.startswith('Miner')]
    for m in MINERS:
        sys.path.insert(0, os.path.join(path, 'Blockchain_System', m))

    min_user = 999999
    min_miner = None
    for miner in MINERS:
        with open(os.path.join(path, 'Blockchain_System', miner, 'users.json'), 'r') as f:
            users = json.load(f)
        if len(users) > 0:
            #print(miner, users[0].items(), len(users[0].items()), '\n')
            if len(users[0].items()) < min_user:
                min_user = len(users[0].items())
                min_miner = miner
        else:
            min_user = 0
            min_miner = miner
            break
    print(min_user, min_miner)

    new_user = User(min_miner)
    with open(os.path.join(path, 'Blockchain_System', min_miner, 'users.json'), 'r') as f_u:
        users = json.load(f_u)
    
    with open(os.path.join(path, 'Blockchain_System', min_miner, 'all_users.json'), 'r') as f_au:
        all_users = json.load(f_au)
    
    userobj = codecs.encode(pickle.dumps(new_user), 'base64').decode()

    if len(all_users) > 0:
        if len(users) > 0:
            users[0][f'{username}'] = {'miner' : new_user.miner, 'user_object' : userobj, 'balance' : 100, 'active' : True}
        else:
            users.append({f'{username}' : {'miner' : new_user.miner, 'user_object' : userobj, 'balance' : 100, 'active' : True}})
        
        all_users[0][f'{username}'] = {'miner' : new_user.miner, 'user_object' : userobj, 'balance' : 100, 'active' : True}
    else:
        users.append({f'{username}' : {'miner' : new_user.miner, 'user_object' : userobj, 'balance' : 100, 'active' : True}})
        all_users.append({f'{username}' : {'miner' : new_user.miner, 'user_object' : userobj, 'balance' : 100, 'active' : True}})

    with open(os.path.join(path, 'Blockchain_System', min_miner, 'users.json'), 'w') as f_u:
        json.dump(users, f_u, indent=4, separators=(',', ':'))
    
    with open(os.path.join(path, 'Blockchain_System', min_miner, 'all_users.json'), 'w') as f_au:
        json.dump(all_users, f_au, indent=4, separators=(',', ':'))

    # other miner's user updation thread will automatically update the all_user.json
    for miner in MINERS:
        if miner == min_miner:
            continue
        m_obj = importlib.import_module(miner)
        m_obj.Miner().updateUserlist('all_users', all_users)

    print(f"User added successfully! Connected to Miner : {new_user.miner}\n")
    new_user = None

def main():
    path = str(Path(__file__).parent).split('Blockchain_System')[0]
    MINERS = [i for i in os.listdir(os.path.join(path, 'Blockchain_System')) if i.startswith('Miner')]
    for m in MINERS:
        sys.path.insert(0, os.path.join(path, 'Blockchain_System', m))

    all_users = json.load(open(os.path.join(path, 'Blockchain_System', 'Miner_0', 'all_users.json')))

    uname = input("Enter your username : ")
    if len(all_users) > 0 :
        while uname not in all_users[0].keys():
            ch = input("Username does not exist\nPress 1 for Adding User\nPress 2 to Retry\nEnter your choice : ")
            if ch == '1':
                addUser(uname)
                all_users = json.load(open(os.path.join(path, 'Blockchain_System', 'Miner_0', 'all_users.json')))
                break
            elif ch == '2':
                uname = input("Enter your username : ")
            else:
                print("Wrong choice! Aborted!")
                return
        user = all_users[0][uname]
        print(f"Welcome! : Your Miner : {user['miner']}\tAvailable balance : {user['balance']}")
    
    else:
        while True :
            ch = input("Username does not exist. Press 1 for Adding User : ")
            if ch == '1':
                addUser(uname)
                all_users = json.load(open(os.path.join(path, 'Blockchain_System', 'Miner_0', 'all_users.json')))
                break
            else:
                print("Wrong choice! Please try again!")
    
    while True:

        all_users = json.load(open(os.path.join(path, 'Blockchain_System', 'Miner_0', 'all_users.json')))
        user = all_users[0][uname]

        print("\nAvailable User Operations :\n1. Transaction\n2. Check balance\n3. Check Miner\n4. Logout")
        ch = input("Enter your choice : ")
        if ch == '1':
            recv = input("\nTRANSACTION\nEnter receiver's username : ")
            if recv not in all_users[0].keys():
                print(f"Receiver {recv} does not exist. Please try again!")
            else:
                user_miner = user['miner']
                amount = int(input("Enter amount : "))
                m_obj = importlib.import_module(user_miner)
                status = m_obj.Miner().makeTransacton(uname, recv, amount)
                if status == 1:
                    print("Transaction Successful")
        
        elif ch == '2':
            print(f"Available balance : {user['balance']}")
            pass

        elif ch == '3':
            print(f"You are connected with {user['miner']}")
            pass
        
        elif ch == '4':
            print("Thank you")
            break

        else:
            print("Invalid choice! Please try again!")

main()