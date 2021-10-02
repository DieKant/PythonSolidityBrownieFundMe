from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me

# importa da brownie le exceprions per controllare gli errori
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    # mettici +100 per imprevisiti e spread di prezzo
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    # controllo se ho fundato il contratto col minimo indispensabile
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    # controllo se ho ritirato i fondi dal contratto
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    # testiamo se un utente non owner può prelevare i fondi
    # salto il test se sono su rinkeby
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local env, skipping...")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # diciamo quale exception ci aspettiamo, e di fare l'azione correttiva senza far crashare tutto quanto
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
