#Link:  https://www.investopedia.com/terms/s/sma.asp
import pandas as pd


# Simple Moving Average
def SMA(data):

    # Calculate SMA_Open
    SMA_Open = [data['open'][0]]
    for i, row in enumerate(data['open'][1:], start=1):
        SMA_Open.append((row + (SMA_Open[i-1]*i)) / float(i+1))

    # Calculate SMA_High
    SMA_High = [data['high'][0]]
    for i, row in enumerate(data['high'][1:], start=1):
        SMA_High.append((row + (SMA_High[i-1]*i)) / float(i+1))

    # Calculate SMA_Low
    SMA_Low = [data['low'][0]]
    for i, row in enumerate(data['low'][1:], start=1):
        SMA_Low.append((row + (SMA_Low[i-1]*i)) / float(i+1))

    # Calculate SMA_Close
    SMA_Close = [data['close'][0]]
    for i, row in enumerate(data['close'][1:], start=1):
        SMA_Close.append((row + (SMA_Close[i-1]*i)) / float(i+1))

    data['SMA_Open'] = SMA_Open
    data['SMA_High'] = SMA_High
    data['SMA_Low'] = SMA_Low
    data['SMA_Close'] = SMA_Close

    return data
