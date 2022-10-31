# from compile import abi, bytecode
from web3 import Web3, HTTPProvider
import json
import os
from dotenv import load_dotenv

load_dotenv()

web3 = Web3(HTTPProvider("https://liberty10.shardeum.org/"))

account_from = {
    "private_key": os.getenv('PRIVATE_KEY'),
    "address": os.getenv('ADDRESS'),
}


with open("Attendence.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()
    
abi = jsonObject["abi"]
bytecode = jsonObject["bytecode"]

Attendence = web3.eth.contract(abi=abi, bytecode=bytecode)
nonce = web3.eth.getTransactionCount(account_from["address"])
transaction = Attendence.constructor().buildTransaction(
    {
        "chainId": 8080,
        "gasPrice": web3.eth.gas_price,
        "from": account_from["address"],
        "nonce": nonce,
    }
)

tx_create = web3.eth.account.sign_transaction(
    transaction, account_from["private_key"]
)
tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Contract deployed at address: { tx_receipt.contractAddress }")
