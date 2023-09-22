from typing import Any
import pandas as pd
import random
from binance import Client
from database.files_db import HistoricalDataFile, OrderFile, UserFile


class Strategy:
    """
    Base class for strategies.
    """

    def __init__(self, api_key, order_id):
        self.api_key = api_key
        self.order_id = order_id

    def buy_order(self, curr_date: str, qnt: float) -> str:
        """
        Simulates order buyng and saves to DB.

        Args:
            curr_date: current date; when you buy an order

        Returns:
            order_id(float): an ID of order
        """
        market = pd.DataFrame(HistoricalDataFile().get_data())
        curr_price = market[market.time == curr_date].iloc[0]["close"]
        ammount = curr_price*qnt

        UserFile().post_data({
            "api_key": self.api_key,
            "order_id": self.order_id,
            })
        OrderFile().post_data({
            "order_id": self.order_id,
            "date": curr_date,
            "bought": str(curr_price),
            "quantity": str(qnt),
            "ammount": str(ammount),
            "sold": "",
            "pnl": "",
            "pnl_ammount": ""
        })


    def sell_order(self, curr_date: str) -> str:
        """
        Simulates order selling and saves to DB.

        Args:
            curr_date: current date; when you sell an order
            order_id (str): id of order that was generated in buy_order

        Returns:
            dict:
                pnl: profit and loss
        """
        market = pd.DataFrame(HistoricalDataFile().get_data())
        orders = pd.DataFrame(OrderFile().get_data())
        curr_price = float(market[market.time == curr_date].iloc[0]["close"])
        order = orders[orders.order_id == self.order_id]
        prev_price = float(order.iloc[0]["bought"])
        ammount = float(order.iloc[0]["ammount"])
        qnt = float(order.iloc[0]["quantity"])
        pnl = ((curr_price-prev_price)/(prev_price))*100
        pnl_ammount = ammount*pnl+ammount

        full_order = {
            "order_id": self.order_id,
            "date": curr_date,
            "bought": str(prev_price),
            "quantity": str(qnt),
            "ammount": str(ammount),
            "sold": str(curr_price),
            "pnl": str(pnl),
            "pnl_ammount": str(pnl_ammount)
        }
        OrderFile().post_data(full_order)

        return full_order
