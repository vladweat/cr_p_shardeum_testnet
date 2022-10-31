import config

from time import sleep
from shardeum_core import ShardeumClient


def main():
    client = ShardeumClient(address=config.ADDRESS, run=config.RUN_SCRIPT, private_key=config.PRIVATE_KEY)
    
    if client.check_connection() == True:
        client.create_accounts(10)
        # sleep необходим для паузы скритпа
        sleep(10)
        # функция рассылки токенов с основного аккаунта, 
        # в которую передается список адресов из файла wallet.txt
        client.disperse_smh_to_wallets(client.get_adresses()) 
        sleep(10)
        # функция вывода баланса, 
        # в которую передается список адресов из файла wallet.txt
        client.get_wallets_balance(client.get_adresses())

if __name__ == "__main__":
    main()