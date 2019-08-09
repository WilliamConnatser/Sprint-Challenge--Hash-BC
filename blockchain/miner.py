import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

cache = {}


def proof_of_work(last_proof, starting_nonce):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...999123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    """

    last_proof_hash = f'{last_proof}'.encode()
    last_proof_hash = hashlib.sha256(last_proof_hash).hexdigest()
    last_proof_hash = str(last_proof_hash)[-6:]

    start = timer()

    print("Searching for next proof")
    proof = starting_nonce
    while not cache.get(last_proof_hash, None):

        if not cache.get(last_proof_hash, None):
            valid_proof(last_proof_hash,proof)
        
        proof += 1

        if proof % 9999999 == 0:
            print(f"Mining on {last_proof} Checking for new block... \U0001F50D\U0001F50D")
            r = requests.get(url=node + "/last_proof")
            data = r.json()
            if data.get("proof") != last_proof:
                print(f"New Block Received.. Restarting Work! \U0001F612\U0001F612 {last_proof} {data.get('proof')}") 
                last_proof = data.get("proof")
                proof = len(cache.keys())
            else:
                print(f"Mining on {last_proof}.... \U0001F477\U0001F477")

    print(f"Proof found: {str(proof)} Proof From Cache: {cache.get(last_proof_hash)} Time: {str(timer() - start)} \U0001F4B0\U0001F4B0\U0001F4B0\U0001F4B0\U0001F4B0\U0001F4B0")
    return cache.get(last_proof_hash)


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the last hash match the first six characters of the proof?

    IE:  last_hash: ...999123456, new hash 123456888...
    """
            
    hashed_proof = f'{proof}'.encode()
    hashed_proof = hashlib.sha256(hashed_proof).hexdigest()    
    hashed_proof = str(hashed_proof)[:6]
    cache[hashed_proof] = proof

    return last_proof == hashed_proof

if __name__ == '__main__':
    # What node are we interacting with?
    # if len(sys.argv) > 1:
    #     node = sys.argv[1]
    # else:
    #     node = "https://lambda-coin.herokuapp.com"
    node = "https://lambda-coin.herokuapp.com"
    
    if len(sys.argv) > 1:
        starting_nonce = int(sys.argv[1])
    else:
        starting_nonce = 0

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    if len(id) == 0:
        f = open("my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'), starting_nonce)

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
