import os
from dotenv import load_dotenv
from binance import Client
from trade_platforms.base import TradePlatform


load_dotenv()
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET = os.getenv("BINANCE_SECRET")


class BinanceTradePlatform(TradePlatform):
    """
    Binance interactions.
    """

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_connection(self) -> Client:
        """
        Create a client connection to Binance.

        Return:
        client(Client): Client object;
        """
        client = Client(api_key=self.api_key, api_secret=self.api_secret)

        return client

    def ping(self) -> bool:
        """
        Ping a connection.

        Return:
        (bool);
        """
        client = self.get_connection()
        if client.get_account():
            return True

        return False

    def get_account(self) -> dict:
        """
        Get account data.

        Return:
        acc(dict): account data;
        """
        acc = self.get_connection().get_account()

        return acc
