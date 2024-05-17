from typing import Union
 
from fastapi import FastAPI
from blockchain import Block, Blockchain
import time
import json
import requests

app = FastAPI()
genesis = Block([b"tx1", b"tx2"], time.time(), 0, bytes(32), 0)
genesis.get_head(0)
genesis.get_hash()
blockchain = Blockchain([genesis], 250)

 
@app.get("/")
def read_root():
    return {"Hello": "blockchain"}
 
@app.post("/addtx/")
def addtx(tx):

    return {"status":200, "msg":"added"}
 
 
@app.post("/mine/")
def mine(tx):
    blockchain = Blockchain.from_json("blockchain.json")
    block = Block([tx.encode(), tx.encode()])
    blockchain.mine(block)
    blockchain.save_json("blockchain.json")
    return {"status":200, "msg":"minado"}
 
@app.get("/blockchain/")
def get_blockchain():
    blockchain = Blockchain.from_json("blockchain.json")
    return blockchain.to_json()

@app.get("/fetch/")
def fetch_blockchain():
    with open("hosts.json", "r") as f:
        hosts = json.load(f)
    url = hosts.get("hosts")[0].get("ip")
    print(url)
    x = requests.get(url)
    print(x)
    blockchain_json = x.text
    blockchain = Blockchain.load_from_json(blockchain_json)
    return {"blockckain":blockchain.to_json()}

 