import hashlib as hs
import time
import json
import base64 
 
class ByteEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, bytes):
      return base64.b64encode(o).decode("ascii")
    else:
      return super().default(o)
 
class Block:
  def __init__(self, tx, timestamp=None, height=None,  prev_hash=None,  target=250, ver=1, head=None, hash=None):
    self.ver = ver
    self.tx = tx
    self.prev_hash = prev_hash
    self.target = target
    self.timestamp = timestamp
    self.height = height
    self.head = head
    self.hash = hash
 
  def get_head(self, nonce):
    ver = int.to_bytes(self.ver, 4, "little")
    prev_hash = self.prev_hash
    merkle_root = self.merkle_root(self.tx)
    timestamp = int.to_bytes(int(self.timestamp), 4, "little")
    target = int.to_bytes(self.target, 4, "little") #toca cambiarlo
    nonce = int.to_bytes(nonce,4,"little")
    self.head = ver + prev_hash + merkle_root + timestamp + target + nonce
 
    return self.head
 
  def get_hash(self):
    self.hash = hs.sha256(self.head).digest()
    return self.hash
 
  def SHA256(self, data):
    return hs.sha256(hs.sha256(data).digest())
 
  def merkle_root(self, tx):
    if len(tx) == 2:
        return self.SHA256(tx[0][::-1] + tx[1][::-1]).digest()
    if len(tx) % 2 != 0 :
        tx = tx[::-1] + [tx[-1]]
    pairs = [(tx[i], tx[i+1]) for i in range(0, len(tx), 2)]
    
    hashes = [self.SHA256(pair[0][::-1] + pair[1][::-1]).digest() for pair in pairs]
    return self.merkle_root(hashes)
 
  def __repr__(self):
    return str(self.__dict__)
 
class Blockchain:
  def __init__(self, blocks, target):
    self.blocks = blocks
    self.target = target
 
  def append(self, block):
 
    if ((int(block.prev_hash.hex(), 16) == 0) or (self.blocks[-1].hash == block.prev_hash)) and (int(block.hash.hex(), 16) < 2**block.target ):
      self.blocks.append(block)
    else:
      print(self.blocks[-1])
      print( block)
      print(self.blocks[-1].hash == block.prev_hash, block.hash.hex(),self.blocks[-1].hash.hex()   )
      print(int(block.hash.hex(), 16) < 2**block.target, block.target)
 
  def mine(self, block):
    block.prev_hash = self.blocks[-1].get_hash()
    block.target = self.target
    block.timestamp = time.time()
    block.height = len(self.blocks)
    for nonce in range(2**24):
      head = block.get_head(nonce)
      h = block.get_hash()
      if int(h.hex(), 16) < 2**self.target:
        self.append(block)
        break
 
 
  def to_json(self):
    d = {k:v for k,v in self.__dict__.items()}
    d["blocks"] = [b.__dict__ for b in self.blocks]

    
    return json.dumps(d, cls = ByteEncoder)

  def save_json(self, path):
    with open(path, "w") as f:
      json.dump(str(self.to_json()), f)
    
  @staticmethod
  def load_from_json(data):
    blockchain = Blockchain([], 250)
    data = json.loads(data)
    print(data)
    for block in data["blocks"]:
      b = Block(
          ver = block.get("ver"),
          tx = [base64.b64decode(x) for x in block.get("tx")],
          prev_hash = base64.b64decode(block.get("prev_hash")),
          target = block.get("target"),
          timestamp = block.get("timestamp"),
          height = block.get("height"),
          head = base64.b64decode(block.get('head')),
          hash = base64.b64decode(block.get("hash")),
      )
      blockchain.append(b)
    return blockchain


  @staticmethod
  def from_json(path):
    with open(path, "r") as f:
      data = json.load(f)
      data = json.loads(data)
    blockchain = Blockchain([], 250)

    for block in data["blocks"]:
      b = Block(
          ver = block.get("ver"),
          tx = [base64.b64decode(x) for x in block.get("tx")],
          prev_hash = base64.b64decode(block.get("prev_hash")),
          target = block.get("target"),
          timestamp = block.get("timestamp"),
          height = block.get("height"),
          head = base64.b64decode(block.get('head')),
          hash = base64.b64decode(block.get("hash")),
      )
      blockchain.append(b)
    return blockchain

