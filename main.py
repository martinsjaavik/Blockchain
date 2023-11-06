import hashlib
import time


class Block:
    # Represents a block in the blockchain.

    # Attributes:
    # previous_hash (str): The hash of the previous block in the chain.
    # block_hash (str): The hash of the current block..
    # transactions (list): List of transactions included in the block.
    # nonce (int): A value used in the proof-of-work algorithm.
    # timestamp (str): The timestamp when the block was created.
    # height (int): The distance from the genesis block.
    
    def __init__(self):

        self.previous_hash = ""
        self.block_hash = None
        self.transactions = []
        self.nonce = ""
        self.timestamp = None
        self.height = None
        

class Blockchain:
    # Represents a blockchain consisting of blocks.

    # Attributes:
    # chain (list): List of blocks in the blockchain.

    def __init__(self):
    # Initialize an empty blockchain and generate the genesis block
        self.chain = []
        self.generate_genesis_block()

    
    def get_last_block(self): 
        # Returns the last block in the blockchain.
        return self.chain[-1]
    
    def get_2nd_last_block(self): 
        # Returns the second last block in the blockchain.
        return self.chain[-2]
    
    def update_list(self, new_list):
        # Updates the list of transactions in the last block.
        self.get_last_block().transactions.append(new_list)

    def get_prev_hash(self):
        # Returns the hash of the previous block.
        return self.get_last_block().block_hash
    
    def get_2nd_prev_hash(self):
        # Returns the hash of the second previous block.
        return self.get_2nd_last_block().block_hash
    
    def add_genesis_hash(self, block):
        # Computes the hash of teh genesis block and performs proof-of-work.

        # Returns:
        # str: The computed hash of the genesis block.
        hashed_data = ""
        prev_hash = self.get_prev_hash()
        nonce = 0

        while hashed_data[:4] != "0000":
            data = block.timestamp + str(prev_hash) + "".join(
                self.get_last_block().transactions) + str(nonce) 
            hashed_data = hashlib.sha256(data.encode()).hexdigest()
            #print(data)
            #print(nonce, hashed_data[:4])
            nonce+=1

        block.nonce = nonce
        return hashed_data
    
    def add_hash(self, block):
        # Computes the hash of a block and performs proof-of-work.

        # Returns:
        # str: The computed hash of the block.
        hashed_data = ""
        prev_hash = self.get_2nd_prev_hash()
        nonce = 0

        while hashed_data[:4] != "0000":
            data = block.timestamp + str(prev_hash) + "".join(
                self.get_last_block().transactions) + str(nonce) 
            hashed_data = hashlib.sha256(data.encode()).hexdigest()
            #print(data)
            #print(nonce, hashed_data[:4])
            nonce+=1

        block.nonce = nonce
        return hashed_data
    
    def add_transaction(self):
        #Adds a new transaction to the current block.
        start_input = input("Do you want to add a transaction? Y/N ")
        if start_input == "y" or start_input == "Y":
            newline()
            sender = input("Input the senders name: \n")
            reciever = input("Input the recievers name: \n")
            amount = input("Input the amount in Bitcoin: \n")
            my_str = " " + sender + " sent " + reciever + " " + amount + " BTC "
            self.update_list(my_str)
            self.add_transaction()
        elif start_input == "n" or start_input == "N":
            newline()
            print("Block created")
            newline()
        else:
            print("Invalid command. Try again")
            self.add_transaction()

    def generate_genesis_block(self):
        # Generates the initial (genesis) block of the blockchain.
        genesis_block = Block()
        self.chain.append(genesis_block)
        genesis_block.previous_hash = "0" * 64
        genesis_block.height = 0
        t = time.gmtime()
        genesis_block.timestamp = time.asctime(t)
        self.add_transaction()
        genesis_block.block_hash = self.add_genesis_hash(genesis_block)
        

    def generate_block(self):
        # Generates a new block in the blockchain.
        block = Block()
        self.chain.append(block)
        block.previous_hash = self.get_2nd_prev_hash()
        block.height = self.get_2nd_last_block().height + 1
        t = time.gmtime()
        block.timestamp = time.asctime(t)
        self.add_transaction()
        block.block_hash = self.add_hash(block)
        

    def display_last_block(self):
        # Displays information about the last block.
        print(f"----- Block {len(self.chain) - 1} -----\n")
        print(f"Timestamp: {self.chain[-1].timestamp}")
        print(f"Previous Hash: {self.chain[-1].previous_hash}")
        print(f"Nonce: {self.chain[-1].nonce}")
        print(f"Hash: {self.chain[-1].block_hash}")
        print(f"Height: {self.chain[-1].height}")
        print(
        f"Transactions: {self.chain[-1].transactions}\n")


    def display_chain(self):
        # Displays information about all blocks in the blockchain.
        for i in range(len(self.chain)):
            print(f"----- Block {i} -----\n")
            print(f"Timestamp {i}: {self.chain[i].timestamp}")
            print(f"Previous Hash {i}: {self.chain[i].previous_hash}")
            print(f"Nonce {i}: {self.chain[i].nonce}")
            print(f"Hash {i}: {self.chain[i].block_hash}")
            print(f"Height {i}: {self.chain[i].height}")
            print(f"Transactions {i}: {self.chain[i].transactions}\n")


def newline():
    print("\n")


def main():
    # Start function to create and interact with the blockchain.
    start_input = input("Do you want to create a Blockchain? Y/N ")
    if start_input == "y" or start_input == "Y":
        my_blockchain = Blockchain()
        meny(my_blockchain)
    elif start_input == "n" or start_input == "N":
        print("See you later!")
        quit()
    else:
        print("Invalid command. Try again")
        main()


def meny(blockchain):
    # Interactive menu to perform actions on the blockchain.

    # Args:
    # blockchain (Blockchain): The blockchain to perform actions on.
    choice = input("""
------------ Blockchain menu ------------
                   
Press 1 for generating a new block
Press 2 for displaying the last block
press 3 for displaying the whole blockchain
Press q to quit
          
""")
    
    if choice == "1":
        newline()
        blockchain.generate_block()
        blockchain.display_chain()
        meny(blockchain)

    elif choice == "2":
        newline()
        print("Last Block")
        blockchain.display_last_block()
        meny(blockchain)

    elif choice == "3":
        newline()
        blockchain.display_chain()
        meny(blockchain)

    elif choice.lower() == "q":
        quit()

    else:
        print("Invalid command. Try again")
        meny(blockchain)

if __name__ == "__main__":
    main()
else:
    print("two.py is being imported into another module")
