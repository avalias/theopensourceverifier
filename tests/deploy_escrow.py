from datetime import datetime, timedelta
import base64
from algosdk.v2client import algod
from algosdk import account
from algosdk import transaction
from algosdk.encoding import decode_address
from pyteal import compileTeal, Mode
from algosdk import account, mnemonic


import config_escrow as config

local_ints = 0
local_bytes = 0
global_ints = 15
global_bytes = 3


def get_current_timestamp():
    # This function returns the cureent date time timestamp
    return datetime.timestamp(datetime.now())


def get_future_timestamp_in_days(days):
    # This function returns the future timestamp in days from current date time
    future_time = timedelta(days=days) + datetime.now()
    return datetime.timestamp(future_time)


def get_future_timestamp_in_secs(secs):
    # This function returns the future timestamp in seconds from current date time
    future_time = timedelta(seconds=secs) + datetime.now()
    return datetime.timestamp(future_time)


def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response["result"])


# helper function that converts a mnemonic passphrase into a private signing key
def get_private_key_from_mnemonic(mn):
    private_key = mnemonic.to_private_key(mn)
    return private_key


# helper function that waits for a given txid to be confirmed by the network
def wait_for_confirmation(client, txid):
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") > 0):
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print(
        "Transaction {} confirmed in round {}.".format(
            txid, txinfo.get("confirmed-round")
        )
    )
    return txinfo


def wait_for_round(client, round):
    last_round = client.status().get("last-round")
    print(f"Waiting for round {round}")
    while last_round < round:
        last_round += 1
        client.status_after_block(last_round)
        print(f"Round {last_round}")


def main(
    deployer_address: str = config.account_a_address,
    deployer_mnemonic: str = config.account_a_mnemonic,
    buyer_address: str = config.account_b_address,
    seller_address: str = config.account_c_address,
    escrow_payment_1: int = config.escrow_payment_1,
    escrow_payment_2: int = config.escrow_payment_2,
    total_price: int = config.total_price,
    inspection_start: int = int(get_current_timestamp()),
    inspection_end: int = int(get_future_timestamp_in_secs(60)),
    closing_date=int(get_future_timestamp_in_secs(240)),
    free_funds_date=int(get_future_timestamp_in_secs(360)),
    enable_time_checks=False,
    foreign_apps=[],
    foreign_assets=[],
):
    deployer_private_key = get_private_key_from_mnemonic(deployer_mnemonic)

    # declare application state storage (immutable)
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    # approval_program_ast = approval()
    # approval_program_teal = compileTeal(
    #     approval_program_ast, mode=Mode.Application, version=6
    # )

    # with open("./build/approval.teal", "w") as h:
    #     h.write(approval_program_teal)

    approval_program_compiled = base64.b64decode("""
    CCAEAQAEoI0GJgsMZ2xvYmFsX2J1eWVyDWdsb2JhbF9hc2FfaWQZZ2xvYmFsX2VuYWJsZV90aW1lX2NoZWNrcw5nbG9iYWxfY3JlYXRvchB3aXRoZHJhd19iYWxhbmNlDWdsb2JhbF9zZWxsZXITZ2xvYmFsX2Nsb3NpbmdfZGF0ZR1nbG9iYWxfYnV5ZXJfYXJiaXRyYXRpb25fZmxhZx5nbG9iYWxfc2VsbGVyX2FyYml0cmF0aW9uX2ZsYWcaZ2xvYmFsX2luc3BlY3Rpb25fZW5kX2RhdGUZZ2xvYmFsX2J1eWVyX3B1bGxvdXRfZmxhZzEYIxJAAK0xGYEFEkAAmTEZJBJAAIcxGSISQAB+MRmBAhJAAHQxGSMSQAABAIgAiUAAYIgAmEAAVIgAp0AASIgBiUAAPIgA2kAAMIgA8kAAJIgBDUAAGIgBOUAADIgAmUAAAQCIAywjQycHImciQ4gDgUL/8ogDVEL/7IgDMUL/5icIImciQ4gC50L/2ogC4UL/1IgC20L/ziJDI0MrZDEAEkAAAQAiQzIKYCMSQAACI0MiQ4gBTiJDigABMgQiEitkMQASEDYaACcEEhCJigABMgQiEihkMQASEDYaACcEEhCJigABMgQiEicFZDEAEhA2GgAnBBIQiYoAATIEIhIxAChkEhAxEIEGEhA2GgCADm9wdGluX2NvbnRyYWN0EhCJigABMgQiEjYaAIAPb3B0b3V0X2NvbnRyYWN0EhCJigABMgQiEihkMQASEDYaAIAMd2l0aGRyYXdfQVNBEhCJigABMgQiEihkMQASEDYaAIARYnV5ZXJfc2V0X3B1bGxvdXQSECpkIhIQMgcnCWQMEImKAAEyBCISKGQxABIQNhoAgBVidXllcl9zZXRfYXJiaXRyYXRpb24SECpkIhIQMgcnBmQMECMRiYoAATIEIhInBWQxABIQNhoAgBZzZWxsZXJfc2V0X2FyYml0cmF0aW9uEhAqZCISEDIHJwZkDBAjEYmKAAAqNhoLF2cpNhoMF2cnCiNnJwcjZycII2crMQBnKDYaAGcnBTYaAWc2GgIXJQ82GgMXJQ8QNhoCFzYaAxcINhoEFxIQQADJI0M2GgUXNhoGFw42GgYXNhoHFw4QNhoHFzYaCBcOEDYaCBc2GgkXDhA2GgkXNhoKFw4QQAACI0OAHGdsb2JhbF9pbnNwZWN0aW9uX3N0YXJ0X2RhdGU2GgUXZycJNhoGF2eAIGdsb2JhbF9pbnNwZWN0aW9uX2V4dGVuc2lvbl9kYXRlNhoHF2eAEmdsb2JhbF9tb3ZpbmdfZGF0ZTYaCBdnJwY2GgkXZ4AWZ2xvYmFsX2ZyZWVfZnVuZHNfZGF0ZTYaChdnQgBZgBdnbG9iYWxfZXNjcm93X3BheW1lbnRfMTYaAhdngBdnbG9iYWxfZXNjcm93X3BheW1lbnRfMjYaAxdngBNnbG9iYWxfZXNjcm93X3RvdGFsNhoEF2dC/uCJigAAsSKyEDIKYDIACbIIMgqyADEAsgcyALIBMQCyCbMiQ4oAALEkshApZLIRI7ISMgqyADIKshQjsgGzIkOKAACxJLIQKWSyETIKshUyCrIAMgqyFCOyAbMiQ4oAADIKKWRwADUBNQCxJLIQKWSyETQAshIyCrIAMQCyFCOyAbMiQ4oAACcKImciQw==
    """)

    # clear_state_program_ast = clear()
    # clear_state_program_teal = compileTeal(
    #     clear_state_program_ast, mode=Mode.Application, version=6
    # )

    # with open("./build/clear.teal", "w") as h:
    #     h.write(clear_state_program_teal)

    clear_state_program_compiled = base64.b64decode("""CIEBQw==""")

    app_args = [
        decode_address(buyer_address),  # 0 buyer
        decode_address(seller_address),  # 1 seller
        escrow_payment_1,  # 2 1st_escrow_payment
        escrow_payment_2,  # 3 2nd_escrow_payment
        total_price,  # 4 total escrow
        # 5 GLOBAL_INSPECTION_START_DATE, Btoi(Txn.application_args[5]) # uint64
        inspection_start,
        # 6 GLOBAL_INSPECTION_END_DATE, Btoi(Txn.application_args[6]) # uint64
        inspection_end,
        # 7 GLOBAL_CLOSING_DATE, Btoi(Txn.application_args[7]) # uint64
        closing_date,
        # 8 GLOBAL_FREE_FUNDS_DATE, Btoi(Txn.application_args[8]) # uint64,
        free_funds_date,
        free_funds_date,
        free_funds_date,
        enable_time_checks,  # 9 GLOBAL_TIME_CHECK_ENABLED
        1,
    ]
    client = algod.AlgodClient("", "http://node.testnet.algoexplorerapi.io")
    on_complete = transaction.OnComplete.NoOpOC.real
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    txn = transaction.ApplicationCreateTxn(
        deployer_address,
        params,
        on_complete,
        approval_program_compiled,
        clear_state_program_compiled,
        global_schema,
        local_schema,
        app_args,
        foreign_apps=[],
        # foreign_assets=[config.stablecoin_ASA],
        foreign_assets=foreign_assets,
    )
    print("sending ApplicationCreateTxn...")
    # sign transaction
    signed_txn = txn.sign(deployer_private_key)
    tx_id = signed_txn.transaction.get_txid()
    # send transaction
    client.send_transactions([signed_txn])
    # await confirmation
    wait_for_confirmation(client, tx_id)
    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    # print("transaction_response", transaction_response)
    app_id = transaction_response["application-index"]
    confirmed_round = transaction_response["confirmed-round"]
    print("Created new app-id:", app_id)
    # created_app_state = read_created_app_state(
    #     Algod.getClient(), deployer_address, app_id
    # )
    # print("Global state: {}".format(json.dumps(created_app_state, indent=4)))
    return {
        "app_id": app_id,
        "confirmed_round": confirmed_round,
        "inspection_start": inspection_start,
        "inspection_end": inspection_end,
    }


if __name__ == "__main__":
    main()
