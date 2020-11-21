# Link:  https://www.investopedia.com/terms/r/rsi.asp
import numpy as np
import pandas as pd


# Relative Strength Index
####This takes to long...not using built in pandas functions.. has a time complexity of N(where n is >= 100,000)
# def RSI(data, lookback_period):
#     col = np.zeros(len(data))
#     for i in range(lookback_period, len(data)):
#
#         ave_gain = 0
#         ave_loss = 0
#         for j in range(lookback_period):
#             net = (data['4. close'][i - lookback_period + j] - data['1. open'][i - lookback_period + j]) / float(
#                 data['1. open'][i - lookback_period + j])  # percentage of this days gain or loss
#             ave_gain = ((net if net > 0 else 0.0) + ave_gain)  # / float(j+1)
#             ave_loss = ((abs(net) if net < 0 else 0.0) + ave_loss)  # / float(i+1) #float('-inf')
#
#         ave_gain = ave_gain / float(lookback_period)
#         ave_loss = ave_loss / float(lookback_period)
#         rs = ave_gain / (ave_loss if ave_loss != 0 else float('-inf'))
#
#         col[i] = 100 - (100 / (1 + rs))  # rsi
#
#     # data[str(lookback_period, 'day RSI')] = col
#     # return data
#
#     return col


def RSI(stock, period):

    close = stock['4. close']
    delta = close.diff()
    up, down = delta.copy(), delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    gain = up.ewm(com=period - 1, adjust=False).mean()
    loss = down.ewm(com=period - 1, adjust=False).mean()

    # Calculate RS based on exponential moving average (EWMA)
    rs = gain / loss  # relative strength =  average gain/average loss

    rsi = 100 - (100 / (1 + rs))
    return rsi
