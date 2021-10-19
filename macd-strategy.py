import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web

plt.style.use("dark_background")

macd1 = 30
macd2 = 100

start = dt.datetime.now() - dt.timedelta(days = 365*3)
end = dt.datetime.now()

data = web.DataReader('AAPL', 'yahoo', start, end);
#print(data)
data[f'SMA_{macd1}'] = data['Adj Close'].rolling(window=macd1).mean()
data[f'SMA_{macd2}'] = data['Adj Close'].rolling(window=macd2).mean()

data = data.iloc[macd2:]

buy_signals = []
sell_signals = []
state = 0

for x in range(len(data)):
    if data[f'SMA_{macd1}'].iloc[x] > data[f'SMA_{macd2}'].iloc[x] and state != 1:
        #buy signal state
        buy_signals.append(data['Adj Close'].iloc[x])
        sell_signals.append(float('nan'))
        state = 1
    elif data[f'SMA_{macd1}'].iloc[x] < data[f'SMA_{macd2}'].iloc[x] and state != -1:
        #sell signal state
        sell_signals.append(data['Adj Close'].iloc[x])
        buy_signals.append(float('nan'))
        state = -1
    else:
        buy_signals.append(float('nan'))
        sell_signals.append(float('nan'))

data['Buy Signals'] = buy_signals
data['Sell Signals'] = sell_signals

print(data)
plt.plot(data['Adj Close'], label="Price", alpha=0.4)
plt.plot(data[f'SMA_{macd1}'], label=f"MACD1={macd1}", color="orange", linestyle="--")
plt.plot(data[f'SMA_{macd2}'], label=f"MACD2={macd2}", color="purple", linestyle="--")
plt.scatter(data.index, data['Buy Signals'], label="Buy", marker="^", color="#00ff00", lw=3)
plt.scatter(data.index, data['Sell Signals'], label="Sell", marker="v", color="#ff0000", lw=3)
plt.legend(loc="upper left")
plt.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/