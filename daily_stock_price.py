from datetime import date


class PriceHistory:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.open_price: list[float] = []
        self.close_price: list[float] = []
        self.volume: list[int] = []
        self.price_date: list[date] = []
        self.cumulative_vwap = None
        self.cumulative_volume = None

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
    print(stock.ticker, stock.cumulative_vwap, stock.cumulative_volume)


with open("price_data.txt") as file:
    for line in file:
        handle_line(line.strip())
