from brownie import FundMe, network, config, MockV3Aggregator, chain
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # passiamo il price feed dal config/.env    e controlliamo se siamo su un network fisso, altrimenti creiamo un mock
    # usiamo questa variabile LOCAL.. per capire se stiamo usando ganache-cli, ganache-cli collegata a gui, se non è cosi allora deploy per rinkeby altrimenti deploy locale
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed_address"
        ]
    else:
        # spostiamo il deploy del mock negli helpfull scritps
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        # andiamo a cambiare il publish source con la roba dentro al nostro brownie-config.yaml,posso usare un alternativa a questo-> ["verify"]
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Smart contract deployed to {fund_me.address}")
    # questo serve se vogliamo che un altro file usi il deploy del contratto per il testing
    return fund_me


def main():
    deploy_fund_me()
