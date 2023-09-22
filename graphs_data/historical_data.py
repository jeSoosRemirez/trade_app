import pandas as pd
from binance import Client


class HistoricalData:
    """
    Args:
        client (Client): client from Binance class
        symbol (str): "BTCUSDT"
        interval (str): "1 d"
        lookback (str): "300 d ago"
    """

    def __init__(self, client: Client, symbol, interval, lookback):
        self.client = client
        self.symbol = symbol
        self.interval = interval
        self.lookback= lookback

    def get_interval_data(self) -> pd.DataFrame:
        """
        Get data from Binance and form it.

        Returns:
            frame(pd.DataFrame): structured data
        """
        client = self.client.get_connection()
        frame = pd.DataFrame(client.get_historical_klines(
            self.symbol,
            self.interval,
            self.lookback
            ))
        frame = frame.iloc[:, :6]
        frame.columns = ["time", "open", "high", "low", "close", "volume"]
        frame = frame.set_index("time")
        frame.index = pd.to_datetime(frame.index, unit="ms")
        frame = frame.astype(float)

        return frame
