from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_VALUE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"Il network attivo è {network.show_active()}")
    print("deploying mocks...")
    # il to"ei aggiunge 18 decimali dopo il numero che gli diamo, also facciamo il deploy del mock solo una volta e prendiamo quello più recente
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_VALUE, {"from": get_account()})
    print("Mocks pronte!")
