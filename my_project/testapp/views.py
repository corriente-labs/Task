from django.shortcuts import render
from django.http import HttpResponse

from web3 import Web3
import requests

from jsonrpcserver import dispatch
from hexbytes import HexBytes

# Create your views here.


def index(request):
    url = "https://mainnet.infura.io/v3/5fb83531001742e6b127d50929d3eb73"

    # conntect to Metamask
    w3 = Web3(Web3.HTTPProvider(url))
    print("connected to infura?: ", w3.isConnected())

    # set headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # get latest block number
    data = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
    }

    response = requests.post(url, json=data, headers=headers)
    last_number = response.json()["result"]

    # TRICK METAMASK HERE
    second_last_number = hex(int(last_number, 16) - 1)
    last_block = w3.eth.get_block(last_number)
    second_last_block = w3.eth.get_block(second_last_number)

    print("\n*** last block information ***")
    print(last_block["hash"])
    print(last_block["number"])


    print("*** second last block information ***")
    print(second_last_block["hash"])
    print(second_last_block["number"])

    hash_str = second_last_block["hash"].hex()
    # print(hash_str)

    # get_blockByHash

    payload = {
        "id": 2,
        "jsonrpc": "2.0",
        "method": "eth_getBlockByHash",
        "params": [hash_str,
                   False],
    }

    response = requests.post(url, json=payload, headers=headers)

    print("\n*** eth_hash last block ***")
    print(last_block["hash"].hex())

    print("*** eth_getBlockByHash second last block ***")
    print(response.json()["result"]["hash"])

    return HttpResponse(response.json())
