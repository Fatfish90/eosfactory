# python3 ./tests/test1.py

import setup
import cleos
import teos
import eosf
import unittest
from termcolor import colored, cprint
import time

setup.set_json(False)        
setup.set_verbose(True)
cleos.dont_keosd()

cprint("""
Testing `eosf.account()`.

`eosf.account()` is a factory: depending on parameters, it returns the same 
object, representing an EOSIO account functionality, yet build in many ways:

    -- with the `cleos create account` command;
    -- with the `cleos system newaccount` command;
    -- it can be one restored from the blockchain.
""", 'magenta')

def test():
    global account_alice
    global account_carol
    global account_eosio
    global account_bill
    global account_et

    cprint("""
Start session: reset the local EOSIO node, create a wallet object, put the
master account into it.
    """, 'magenta')

    account_eosio = cleos.AccountEosio()
    node_reset = teos.node_reset()
    wallet = eosf.Wallet()
    wallet.import_key(account_eosio)

    cprint("""
Create an account object, named `account_alice`, with the `eosf.account()`, 
with default parameters: 

    -- using the `account_eosio` as the creator;
    -- using a random 12 character long name;
    -- using internally created `owner` and `active` keys.
    """, 'magenta')

    account_alice = eosf.account()
    wallet.import_key(account_alice)


    account_carol = eosf.account()
    wallet.import_key(account_carol)

    cprint("""
The following `account_bill` object represents the account of the name `bill`
    """, 'magenta')

    account_bill = eosf.account(name="bill")
    wallet.import_key(account_bill)

    account_et = eosf.account()
    wallet.import_key(account_et)

    cprint("""
The last account `account_et` is going to take a contract. Now, it does not have
any:
    """, 'magenta')

    account_et.code()

    cprint("""
Define a contract, with its code specified in the EOS repository 
(build/contracts/eosio.token), and deploy it:
    """, 'magenta')

    contract_et = eosf.Contract(account_et, "eosio.token")
    ok = contract_et.deploy()
    account_et.code()

    action = account_et.push_action(
        "create", 
        '{"issuer":"' 
            + str(account_eosio) 
            + '", "maximum_supply":"1000000000.0000 EOS", \
            "can_freeze":0, "can_recall":0, "can_whitelist":0}')

    action = contract_et.push_action(
        "issue", 
        '{"to":"' + str(account_alice)
            + '", "quantity":"100.0000 EOS", "memo":"memo"}', \
            account_eosio)
    
    cprint("""
The code of the account is not null anymore. Experiments with the `eosio.token`
contract are shown elsewere. Here, we show how the session accounts recover after
a session restart.
    """, 'magenta')

    account_alice = None
    account_bill = None
    account_carol = None
    account_et = None
    contract_et = None

    wallet = eosf.Wallet()

    cprint("""
The old wallet is restored. It is possible, because there is a password map 
in the wallet directory. 

Note that this provision is available only if the `keosd` Wallet Manager is not 
used and wallets are managed by the local node - this condition is set with the
`cleos.dont_keosd()` statement above.
    """, 'magenta')

    wallet.restore_accounts(globals())
    print(account_alice.account())

    cprint("""
Continue operations on the restored account objects:
    """, 'magenta')

    action = account_et.push_action(
        "transfer", 
        '{"from":"' 
            + str(account_alice)
            + '", "to":"' + str(account_carol)
            + '", "quantity":"25.0000 EOS", "memo":"memo"}', 
        account_alice)

    cprint("""
However, note that the accounts have to be declared global, in order to be 
restorable with the current means.
    """, 'magenta')

#     cprint("""
# Restoration of the accounts is important when working with remote EOSIO nodes.
# Switch a remote node `54.38.137.99:8888`:
#     """, 'magenta')

#     cleos.dont_keosd(False)
#     setup.set_nodeos_URL("54.38.137.99:8888")
#     cleos.WalletStop()
#     setup.set_debug_mode()

#     wallet_name = "tokenika"
#     wallet = eosf.Wallet(wallet_name)

#     cprint("""
# Restoration of the accounts is important when working with remote EOSIO nodes.
# Switch a remote node `54.38.137.99:8888`:
#     """, 'magenta')
    # tokenika_pass = "PW5KRg1DeMrafTRbrYH44xNz9utzAX9JPC8ugYqH6PspVqPVUQBwQ"
    # return
    # account_master = cleos.AccountMaster()
#     cprint("""
# We have got the following message:

# SAVE THE FOLLOWING DATA to use in the future to restore thisaccount object.
# Accout Name: upe1ahhgb3xq
# Owner Public Key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP
# Active Public Key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP

# >>> print(account_master.owner_key)
# Private key: 5HrA3vzVpavzgbRpiYD5T8jG4eVaeygGCi1spydZQSFBgVCpzQp
# Public key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP

# >>> print(account_master.active_key)
# Private key: 5HrA3vzVpavzgbRpiYD5T8jG4eVaeygGCi1spydZQSFBgVCpzQp
# Public key: EOS6GCDeWSDgEwJaqcWpZTJ2PRnYeWuGjTMHstNbHy2cJto9WgvnP
#     """, 'magenta')



#     wallet = eosf.Wallet("tokenika", tokenika_pass)
#     # wallet.list()
#     # wallet.keys()
#     # wallet.open()
#     # wallet.unlock()
#     # wallet.import_key("5HrA3vzVpavzgbRpiYD5T8jG4eVaeygGCi1spydZQSFBgVCpzQp")
#     # 
#     return    
#     cleos.GetAccount("upe1ahhgb3xq")


#     wallet.restore_accounts(globals())

#     cprint("""
# Chose one item from the list of restored account objects. 
# If it is `play11111111`, then:
#     """, 'magenta')

#     print(play11111111.account())


if __name__ == "__main__":
    test()