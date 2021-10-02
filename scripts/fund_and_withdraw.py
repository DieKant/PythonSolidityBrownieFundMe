from brownie import FundMe
from scripts.helpful_scripts import get_account


def fund():
    # prendo il contratto fund me più recente
    fund_me = FundMe[-1]
    # prendo un account
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    # eseguo la transazione sulla blockchain locale
    print(f"il minimo richiesto per le transazioni è di {entrance_fee}")
    print("deposito in corso...")
    fund_me.fund({"from": account, "value": entrance_fee})
    print("deposito effettuato con successo!")


def withdraw():
    # prendo il contratto fund me più recente
    fund_me = FundMe[-1]
    # prendo un account
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
