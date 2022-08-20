import json
import time
import base64
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
import requests

trnote = "privet"

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
algod_address = 'https://testnet-algorand.api.purestake.io/ps2'
purestake_token = {'X-Api-key': algod_token}

# Initalize throw-away account for this example - check that is has funds before running script
mnemonic_phrase = 'they quote toss buffalo expand win pill episode solar tide figure run knee keep push patch stand click riot elephant coil include zone absorb spice';
account_private_key = mnemonic.to_private_key(mnemonic_phrase)
account_public_key = mnemonic.to_public_key(mnemonic_phrase)

algodclient = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)

# get suggested parameters from Algod
def send_transaction(appId, giturl, neededcommHash):
    dict1 = {
        "AppId":appId,
        "GitUrl":giturl,
        "CommitHash":neededcommHash,
        "Status":"verified"
        }
    #trnote=("App Id:" + appId + "=" + giturl + " with commit:" + neededcommHash)
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
    tx = transaction.PaymentTxn(existing_account, fee, first_valid_round, last_valid_round, gh, send_to_address, send_amount, note=note, flat_fee=True)
    signed_tx = tx.sign(account_private_key)

    try:
        tx_confirm = algodclient.send_transaction(signed_tx)
        print('Transaction sent with ID', signed_tx.transaction.get_txid())
        wait_for_confirmation(algodclient, txid=signed_tx.transaction.get_txid())
    except Exception as e:
        print(e)

def checker(appId):
    data = requests.get("https://algoindexer.testnet.algoexplorerapi.io/v2/accounts/{}/transactions?limit=999".format(account_public_key)).json()

    for transaction in data['transactions']:
        if transaction['sender'] == "{}".format(account_public_key):
            try:
                if appId == json.loads(base64.b64decode(transaction['note']).decode())["AppId"]:
                    return True
            except: pass
    return False

