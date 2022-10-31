from web3 import Web3, HTTPProvider
from eth_account import Account
from loguru import logger
from decimal import Decimal
import config
import random
from time import sleep
import json


class ShardeumClient:
    def __init__(self, address: str, run: str, private_key: str) -> None:
        self._web3 = Web3(HTTPProvider(config.LIBERTY15_RPC_URL))
        self._address = self._web3.toChecksumAddress(address)
        self._private_key = private_key
        if config.LIBERTY15_RPC_URL == "https://liberty10.shardeum.org/":
            self._chain_id = 8080
        else:
            self._chain_id = 8081
        if run == 'Special for https://t.me/importweb3, creator - https://t.me/vladweat':
            logger.info(f"{run}")
        else:
            raise SystemExit(1)

    def check_connection(self) -> None:
        """Check connection to RPC URL"""
        return self._web3.isConnected()

    def create_accounts(self, num_of_wallets: int = None) -> None:
        """Create wallets and write in wallet.txt

        Args:
            num_of_walelts (str, optional): number of wallets to create. Defaults to None.
        """
        try:
            for _ in range(num_of_wallets):
                account = Account.create("KEYSMASH FJAFJKLDSKF7JKFDJ 1530")
                with open("wallets.txt", "a+") as file:
                    file.write(f"{account.key.hex()} {account.address}\n")
            logger.info(f"Create and save {num_of_wallets} wallets!")
        except Exception as e:
            logger.error(e)

    def convert_from_ether_format(self, num: int = None) -> int:
        """Convert Wei to Ether format
        100000000000000000000 -> 100

        Args:
            num (integer): wei format integer

        Returns:
            int: _description_
        """
        try:
            ether_format = self._web3.fromWei(num, "ether")
            return ether_format
        except Exception as e:
            logger.error(e)

    def convert_to_ether_format(self, num: int = None) -> int:
        """Convert Ether to Wei format
        100 -> 100000000000000000000
        Args:
            num (integer): ether format integer

        Returns:
            int: _description_
        """
        try:
            wei_format = self._web3.toWei(Decimal(num), "ether")
            return wei_format
        except Exception as e:
            logger.error(e)

    def get_main_balance(self) -> str:
        """Get and return balance of _address

        Returns:
            int: balance of main wallet
        """
        balance = self._web3.eth.get_balance(self._address)
        return self.convert_from_ether_format(balance)

    def get_wallets_balance(self, wallets: list[Account]) -> None:
        """Log balance of addresses in wallets

        Args:
            wallets (list[Account]): target_wallets
        """
        for wallet in wallets:
            balance = self._web3.eth.get_balance(wallet)
            logger.info(
                f"Wallet {wallet} balance: {self.convert_from_ether_format(balance)}"
            )

    def get_wallets(self) -> dict:
        """Return dict of wallets from wallets.txt

        Returns:
            dict: wallets_dict
        """
        wallets_dict = {}
        with open("wallets.txt", "r") as file:
            wallets = file.readlines()

        for wallet in wallets:
            private_key = wallet.split(" ")[0].strip()
            address = wallet.split(" ")[1].strip()
            wallets_dict[address] = private_key
        return wallets_dict

    def get_adresses(self) -> list:
        """Return address from wallets dict

        Returns:
            list: all addresses from wallets dict
        """
        wallets_dict = self.get_wallets()
        addresses = wallets_dict.keys()
        return addresses

    def get_private_key(self, address: str) -> str:
        """Return private key of wallet address

        Args:
            address (str): string of wallet address

        Returns:
            str: private key
        """
        wallets_dict = self.get_wallets()
        private_key = wallets_dict.get(address)
        return private_key

    def disperse_smh_to_wallets(self, target_wallets: list[Account]) -> None:
        """Disperce SMH token from [self._address] wallet to wallets in list

        Args:
            target_wallets (list[Account]): target_wallets
        """
        for wallet in target_wallets:
            amount = random.uniform(0.25, 0.97)
            amount_decimal = self.convert_to_ether_format(amount)

            nonce = self._web3.eth.get_transaction_count(self._address)
            gas_price = self._web3.eth.gas_price
            to_address = Web3.toChecksumAddress(wallet)

            try:
                transaction = {
                    "chainId": self._chain_id,
                    "nonce": nonce,
                    "gas": 1000000,
                    "gasPrice": gas_price,
                    "to": to_address,
                    "from": self._address,
                    "value": amount_decimal,
                }

                signed_txn = self._web3.eth.account.sign_transaction(
                    transaction, private_key=self._private_key
                )

                raw_tx_hash = self._web3.eth.send_raw_transaction(
                    signed_txn.rawTransaction
                )
                tx_hash = self._web3.toHex(raw_tx_hash)

                logger.info(
                    f"Send {amount} from {self._address[:7]} to {wallet} TXHash: {tx_hash}"
                )

                # nonce += 1 # !!!!!!!!!!!!!!!!!!!!!!

                sleep(random.randint(7, 10))

            except Exception as e:
                logger.error(e)
        logger.success(f"Disperse SMH to {len(target_wallets)} wallets")

    def send_smh_to_main(self, wallets: list[Account]) -> None:
        """Send all SMH token from wallets list

        Args:
            wallets (list[Account]): all wallets from wallets.txt
        """
        for wallet in wallets:
            try:
                amount = self._web3.eth.get_balance(wallet)

                if amount > 0:
                    nonce = self._web3.eth.get_transaction_count(wallet)
                    private_key = self.get_private_key(wallet)
                    gas_price = self._web3.eth.gas_price
                    fee = self.convert_to_ether_format(0.0021)

                    if (amount - fee) > 0:

                        transaction = {
                            "chainId": self._chain_id,
                            "nonce": nonce,
                            "gas": 250000,
                            "gasPrice": gas_price,
                            "to": self._address,
                            "from": wallet,
                            "value": amount - fee,
                        }

                        signed_txn = self._web3.eth.account.sign_transaction(
                            transaction, private_key=private_key
                        )

                        raw_tx_hash = self._web3.eth.send_raw_transaction(
                            signed_txn.rawTransaction
                        )
                        tx_hash = self._web3.toHex(raw_tx_hash)

                        logger.info(
                            f"Send {self.convert_from_ether_format(amount)} from {wallet} to {self._address[:7]}. TXHash: {tx_hash}"
                        )

                        sleep(random.randint(5, 10))
                    else:
                        logger.error(
                            f"Wallet {wallet} does not have enough SMH to cover transaction fee! [balance: {self.convert_from_ether_format(amount)}]"
                        )
                else:
                    logger.error(f"Wallet {wallet} has zero balance!")
            except Exception as e:
                logger.error(e)
        logger.success(f"Unite SMH to {self._address} from {len(wallets)} wallets")

    def get_abi_bytecode(self) -> list | list:
        """Return abi and bytecode from contract json file

        Returns:
            list|list: abi|bytecode
        """
        with open("Attendence.json") as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()

        abi = jsonObject["abi"]
        bytecode = jsonObject["bytecode"]
        return abi, bytecode

    def deploy_contract_on_main(self) -> None:
        """Deploying Attendence.sol contract from [self._address] wallet"""
        abi, bytecode = self.get_abi_bytecode()
        Attendence = self._web3.eth.contract(abi=abi, bytecode=bytecode)
        nonce = self._web3.eth.get_transaction_count(self._address)
        try:
            transaction = Attendence.constructor().buildTransaction(
                {
                    "chainId": self._chain_id,
                    "gasPrice": self._web3.eth.gas_price,
                    "from": self._address,
                    "nonce": nonce,
                }
            )
            signed_txn = self._web3.eth.account.sign_transaction(
                transaction, self._private_key
            )
            raw_tx_hash = self._web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_hash = self._web3.toHex(raw_tx_hash)
            # tx_receipt = self._web3.eth.wait_for_transaction_receipt(tx_hash)
            logger.info(
                # f"{self._address[:7]} created contract {tx_receipt}. TXHash: {tx_hash}"
                f"{self._address[:7]} created contract. TXHash: {tx_hash}"
            )
        except Exception as e:
            logger.error(e)

    def deploy_contract_on_wallets(self, wallets: list[Account]) -> None:
        """Deploying Attendence.sol contract from wallets list

        Args:
            wallets (list[Account]): all wallets from wallets.txt
        """
        abi, bytecode = self.get_abi_bytecode()
        Attendence = self._web3.eth.contract(abi=abi, bytecode=bytecode)

        for wallet in wallets:
            try:
                nonce = self._web3.eth.get_transaction_count(wallet)
                private_key = self.get_private_key(wallet)
                transaction = Attendence.constructor().buildTransaction(
                    {
                        "chainId": self._chain_id,
                        "gasPrice": self._web3.eth.gas_price,
                        "from": wallet,
                        "nonce": nonce,
                    }
                )
                signed_txn = self._web3.eth.account.sign_transaction(
                    transaction, private_key=private_key
                )

                raw_tx_hash = self._web3.eth.send_raw_transaction(
                    signed_txn.rawTransaction
                )
                tx_hash = self._web3.toHex(raw_tx_hash)
                logger.info(f"{wallet[:7]} created contract. TXHash: {tx_hash}")

            except Exception as e:
                logger.error(e)
