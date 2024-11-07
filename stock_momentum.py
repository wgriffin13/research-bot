import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Download historical data
ticker = "AAPL"  # Example ticker
data = yf.download(ticker, start="2015-01-01", end="2023-01-01")

# Calculate moving averages
data["50_MA"] = data["Close"].rolling(window=50).mean()
data["200_MA"] = data["Close"].rolling(window=200).mean()

# Signal Generation
data["Signal"] = 0
data["Signal"][50:] = np.where(data["50_MA"][50:] > data["200_MA"][50:], 1, -1)

# Shift signal to avoid look-ahead bias
data["Position"] = data["Signal"].shift(1)
data.dropna(inplace=True)

# Calculate Returns
data["Daily_Return"] = data["Close"].pct_change()
data["Strategy_Return"] = data["Daily_Return"] * data["Position"]

# Calculate Cumulative Returns
data["Cumulative_Returns"] = (1 + data["Daily_Return"]).cumprod()
data["Cumulative_Strategy"] = (1 + data["Strategy_Return"]).cumprod()

# Plot Results
plt.figure(figsize=(14, 7))
plt.plot(data["Cumulative_Returns"], label="Buy and Hold Return", color="blue")
plt.plot(data["Cumulative_Strategy"], label="Momentum Strategy Return", color="red")
plt.title("Momentum Trading Strategy vs. Buy and Hold")
plt.xlabel("Date")
plt.ylabel("Cumulative Returns")
plt.legend()
plt.show()
