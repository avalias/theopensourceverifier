from vote import approval_program
from algosdk.v2client import algod
from pyteal import compileTeal, Mode
import os
from dotenv import load_dotenv

algod_token = ""
algod_address = "http://node.testnet.algoexplorerapi.io"

load_dotenv()
MY_MNEMONIC = os.getenv('MY_MNEMONIC')
private_key = mnemonic.to_private_key(MY_MNEMONIC)
sender = account.address_from_private_key(private_key)


def main():
    # Connect to an algod client
    algod_client = algod.AlgodClient(
        algod_token=algod_token, algod_address=algod_address)

    # Convert the PyTEAL approval program into a TEAL script
    teal_script = compileTeal(
        approval_program(), mode=Mode.Application, version=5)
    print(teal_script)


if __name__ == "__main__":
    main()

