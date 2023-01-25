import json
import time
import base64
from algosdk.v2client import algod
from algosdk import mnemonic, account
from algosdk import transaction
import requests
import os
from dotenv import load_dotenv

load_dotenv()
mnemonic_phrase = os.getenv('MNEMONIC_PHRASE')

# Function from Algorand Inc.


def wait_for_confirmation(client, txid):
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print('Waiting for confirmation')
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print('Transaction confirmed in round', txinfo.get('confirmed-round'))
    return txinfo


# Setup HTTP client w/guest key provided by PureStake
algod_token = 'VGA0ZbwToZ6IHKcrZlZmx5zTzyo2xups8ARsoIMA'
algod_address = 'https://mainnet-algorand.api.purestake.io/ps2'
purestake_token = {'X-Api-key': algod_token}

# Initalize throw-away account for this example - check that is has funds before running script
account_private_key = mnemonic.to_private_key(mnemonic_phrase)
account_public_key = account.address_from_private_key(account_private_key)

algodclient = algod.AlgodClient(
    algod_token, algod_address, headers=purestake_token)

# get suggested parameters from Algod


def send_transaction(net, appId, giturl, buildarg, neededcommHash):
    dict1 = {
        "Net": net,
        "AppId": appId,
        "BuildFileGitUrl": giturl,
        "BuildArgument": buildarg,
        "CommitHash": neededcommHash,
        "Status": "verified"
    }
    # trnote=("App Id:" + appId + "=" + giturl + " with commit:" + neededcommHash)
    trnote = json.dumps(dict1)

    params = algodclient.suggested_params()

    gh = params.gh
    first_valid_round = params.first
    last_valid_round = params.last
    fee = params.min_fee
    note = trnote.encode()
    send_amount = 1

    existing_account = account_public_key
    send_to_address = account_public_key

    # Create and sign transaction
    tx = transaction.PaymentTxn(
        existing_account, params, send_to_address, 0, note=note)
    signed_tx = tx.sign(account_private_key)

    try:
        tx_confirm = algodclient.send_transaction(signed_tx)
        tx_id = signed_tx.transaction.get_txid()
        print('Transaction sent with ID', tx_id)
        wait_for_confirmation(
            algodclient, txid=tx_id)
        return "https://algoexplorer.io/tx/" + signed_tx.transaction.get_txid()
    except Exception as e:
        print(e)

# limit 50 for test
# later do proper pagination or use purestake


def checker(appId):
    data = requests.get(
        "https://indexer.algoexplorerapi.io/v2/accounts/{}/transactions?limit=50".format(account_public_key)).json()

    for transaction in data['transactions']:
        if transaction['sender'] == "{}".format(account_public_key):
            try:
                if appId == json.loads(base64.b64decode(transaction['note']).decode())["AppId"]:
                    return True, "https://algoexplorer.io/tx/" + transaction["id"]
            except:
                pass
    return False, ""
