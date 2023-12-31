import hashlib
import time
import json
import tkinter as tk
from tkinter import messagebox

class Block:
    def _init_(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def create_genesis_block():
    return Block(0, "0", time.time(), "BLOCKCHAIN IS CREATED", calculate_hash(0, "0", time.time(), "BLOCKCHAIN IS CREATED"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + previous_hash + str(timestamp) + data
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def save_blockchain(blockchain):
    with open('blockchain.json', 'w') as file:
        json.dump([vars(block) for block in blockchain], file)

def load_blockchain():
    try:
        with open('blockchain.json', 'r') as file:
            data = json.load(file)
            return [Block(block['index'], block['previous_hash'], block['timestamp'], block['data'], block['hash']) for block in data]
    except FileNotFoundError:
        return []

def validate_blockchain(blockchain):
    for i in range(1, len(blockchain)):
        if blockchain[i].previous_hash != blockchain[i-1].hash:
            return False
    return True

def add_block(entry, label, blockchain):
    new_block_data = entry.get()
    if not new_block_data:
        messagebox.showerror("Error", "Please enter block data")
        return

    if not blockchain:
        previous_block = create_genesis_block()
    else:
        previous_block = blockchain[-1]

    new_block = create_new_block(previous_block, new_block_data)
    blockchain.append(new_block)
    save_blockchain(blockchain)

    entry.delete(0, tk.END)
    label.config(text="Block #{} added to the blockchain".format(new_block.index))

def show_blockchain(blockchain):
        if not blockchain:
            messagebox.showinfo("Blockchain", "Blockchain is empty")
            return

        # Create a new window
        show_window = tk.Toplevel()
        show_window.title("Blockchain View")

        # Create a scrollable text area
        text_area = tk.Text(show_window, wrap="word", width=50, height=20)
        text_area.pack(expand=True, fill="both")

        # Populate the text area with blockchain information
        for block in blockchain:
            block_info = "Block #{}:\nData: {}\nHash: {}\nPrevious Hash: {}\nTimestamp: {}\n\n".format(
                block.index, block.data, block.hash, block.previous_hash, block.timestamp)
            text_area.insert("end", block_info)

        text_area.configure(state="disabled")  # Make the text area read-only


def main():
    blockchain = load_blockchain()

    root = tk.Tk()
    root.title("Blockchain GUI")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    title_label = tk.Label(root, text="Blockchain Application", font=("Helvetica", 20), bg="#f0f0f0")
    title_label.pack(pady=(10, 20))

    label = tk.Label(root, text="Enter block data:", font=("Helvetica", 12), bg="#f0f0f0")
    label.pack()

    entry = tk.Entry(root, width=30, font=("Helvetica", 12))
    entry.pack(pady=(0, 10))

    add_button = tk.Button(root, text="Add Block", command=lambda: add_block(entry, label, blockchain),
                           font=("Helvetica", 12), bg="#4caf50", fg="white")
    add_button.pack()

    show_button = tk.Button(root, text="Show Blockchain", command=lambda: show_blockchain(blockchain),
                            font=("Helvetica", 12), bg="#2196f3", fg="white")
    show_button.pack()

    root.mainloop()

if _name_ == '_main_':
    main()
