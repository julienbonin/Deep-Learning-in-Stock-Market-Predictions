# Link:  https://www.investopedia.com/terms/r/rsi.asp
import numpy as np

# Relative Strength Index
def RSI(data, lookback_period):
    col = np.zeros(len(data))
    for i in range(lookback_period, len(data)):

        ave_gain = 0
        ave_loss = 0
        for j in range(lookback_period):
            net = (data['4. close'][i - lookback_period + j] - data['1. open'][i - lookback_period + j]) / float(
                data['1. open'][i - lookback_period + j])  # percentage of this days gain or loss
            ave_gain = ((net if net > 0 else 0.0) + ave_gain)  # / float(j+1)
            ave_loss = ((abs(net) if net < 0 else 0.0) + ave_loss)  # / float(i+1) #float('-inf')

        ave_gain = ave_gain / float(lookback_period)
        ave_loss = ave_loss / float(lookback_period)
        rs = ave_gain / (ave_loss if ave_loss != 0 else float('-inf'))

        col[i] = 100 - (100 / (1 + rs))  # rsi

    # data[str(lookback_period, 'day RSI')] = col
    # return data

    return col
