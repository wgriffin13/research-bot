from datetime import date
from math import inf


class PriceHistory:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.open_price: list[float] = []
        self.close_price: list[float] = []
        self.volume: list[int] = []
        self.price_date: list[date] = []
        self.cumulative_vwap = None
        self.cumulative_volume = None
        self.highest_change: float = -inf
        self.highest_day_change: float = -inf

    def insert_price_record(
        self,
        price_date: date,
        open_price: float,
        close_price: float,
        volume: int,
    ):
        self.price_date.append(price_date)
        self.open_price.append(open_price)
        self.close_price.append(close_price)
        self.volume.append(volume)

        current_vwap = self.cumulative_vwap
        current_volume = self.cumulative_volume
        if current_volume is None or current_vwap is None:
            self.cumulative_volume = volume
            self.cumulative_vwap = close_price
        else:
            new_volume = current_volume + volume
            new_vwap = (
                current_vwap * current_volume / new_volume
                + close_price * volume / new_volume
            )
            self.cumulative_volume = new_volume
            self.cumulative_vwap = new_vwap

        if len(self.close_price) > 1:
            change = (self.close_price[-1] - self.close_price[-2]) / self.close_price[
                -2
            ]
            self.highest_change = max(self.highest_change, change)

        day_change = (self.close_price[-1] - self.open_price[-1]) / self.open_price[-1]
        self.highest_day_change = max(self.highest_day_change, day_change)

    def get_std_dev(self):
        n = len(self.close_price)
        mean = sum(self.close_price) / n
        sum_diff = 0
        for price in self.close_price:
            sum_diff += (price - mean) ** 2
        return (sum_diff / (n - 1)) ** 0.5

    def __repr__(self):
        return f"PriceHistory({self.ticker}) {self.price_date} {self.open_price} {self.close_price} {self.volume} {self.cumulative_vwap} {self.cumulative_volume} {self.highest_change} {self.highest_day_change}"


stock_price_history_map: dict[str, PriceHistory] = {}


def handle_line(line: str):
    line_parts = line.split(" ")
    ticker = line_parts[0]
    price_date = line_parts[1]
    open_price = line_parts[2]
    close_price = line_parts[3]
    volume = line_parts[4]
    if ticker not in stock_price_history_map:
        stock_price_history_map[ticker] = PriceHistory(ticker)
    stock = stock_price_history_map[ticker]
    stock.insert_price_record(
        price_date=date.fromisoformat(price_date),
        open_price=float(open_price),
        close_price=float(close_price),
        volume=int(volume),
    )


with open("price_data.txt") as file:
    for line in file:
        handle_line(line.strip())


for ticker in stock_price_history_map:
    ph = stock_price_history_map[ticker]
    print(ph)
    print(ph.get_std_dev())
