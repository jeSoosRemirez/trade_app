import random
from datetime import date, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from database.files_db import HistoricalDataFile, OrderFile
from strategies.strategy import Strategy


def generate_dates(start_dt: date, end_dt: date) -> list:
    """
    Generate list of dates in some range.

    Args:
        start_dt (date): start date
        end_dt (date): end date

    Returns:
        list: list of dates
    """
    delta = timedelta(days=1)
    dates = []

    while start_dt <= end_dt:
        dates.append(start_dt.isoformat())
        start_dt += delta

    return dates


def emulate_grid_strategy(
    profit_percent: float,
    start_dt: date,
    end_dt: date,
    api_key: str,
    qnt: float,
    entries: int) -> dict:
    """
    Emulates work of strategy on market.

    Args:
        profit_percent (float): desirable profit
        start_dt (date): start date
        end_dt (date): end date
        api_key (str): api key of user(random here)
        qnt (float): how many you wanna buy coin
        entries (int): count of spots

    Returns:
        stats (dict): closed_orders, pnl, pnl_ammount
    """
    stats = {"closed_orders": [], "pnl": [], "pnl_ammount": []}
    order_ids = []
    key_dates = []
    dates = generate_dates(start_dt = start_dt, end_dt=end_dt)
    key_dates.append(dates[0])
    order_id = str(random.random())
    strategy = Strategy(api_key="test_api_key", order_id=order_id)
    strategy.buy_order(curr_date=dates[0], qnt=qnt)
    order_ids.append(order_id)
    entries_done = 1

    # Here should be data from real-time market
    # so the itteration gonna be adapted
    for dt in dates:
        # If all entries accomplished or the market gone higher
        if entries == entries_done and len(order_ids) == 0:
            break
        elif len(order_ids) == 0:
            break

        market = pd.DataFrame(HistoricalDataFile().get_data())
        orders = pd.DataFrame(OrderFile().get_data())
        curr_price = float(market[market.time == dt].iloc[0]["close"])
        prev_price = float(orders[orders.order_id == order_ids[-1]].iloc[0]["bought"])
        price_diff = ((curr_price-prev_price)/prev_price)*100

        # If low -> buy
        if prev_price and price_diff <= -1*(profit_percent) and entries_done != entries:
            order_id = str(random.random())
            order_ids.append(order_id)
            strategy = Strategy(api_key=api_key, order_id=order_ids[-1])
            strategy.buy_order(curr_date=dt, qnt=qnt)
            entries_done += 1
            key_dates.append(dt)

        # If high -> sell
        elif prev_price and price_diff >= profit_percent:
            strategy = Strategy(api_key="test_api_key", order_id=order_ids[-1])
            sold = strategy.sell_order(curr_date=dt)
            stats["closed_orders"].append(order_ids[-1])
            stats["pnl"].append(sold["pnl"])
            stats["pnl_ammount"].append(sold["pnl_ammount"])
            order_ids.pop()
            key_dates.append(dt)

    # Visualizing the spots on graph
    df = pd.DataFrame(HistoricalDataFile().get_data())
    df["time"] = pd.to_datetime(df["time"])
    start_dt = pd.to_datetime(start_dt)
    end_dt = pd.to_datetime(key_dates[-1])
    df = df[(df['time'] >= start_dt) & (df['time'] <= end_dt)]
    marked_dates = pd.to_datetime(key_dates)

    plt.figure(figsize=(12, 6))
    plt.plot(df['time'], df['close'], label='Your Data', linewidth=2)

    marked_dates_within_range = [date for date in marked_dates if start_dt <= date <= end_dt]
    plt.scatter(marked_dates_within_range,
                df.loc[df['time'].isin(marked_dates_within_range), 'close'],
                color='red',
                marker='o',
                label='Marked Date'
                )

    plt.xlabel('Time')
    plt.ylabel('Close price')
    plt.legend()
    plt.show()


    return stats


# Better to provide wide range
emulate_grid_strategy(
    profit_percent=0.2,
    start_dt = date(2023, 3, 21),
    end_dt = date(2023, 9, 21),
    api_key="testtesttest",
    qnt=0.5,
    entries=5
    )
