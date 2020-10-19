# Link:  https://www.investopedia.com/terms/m/mfi.asp
import numpy as np


# MFI - Money Flow Index
def MFI(data, lookback_period):

    col = np.zeros(len(data))

    for i in range(lookback_period, len(data)):

        raw_money_flow = np.array(lookback_period)
        for j in range(lookback_period):
            raw_money_flow[j] = ((data['high'][i-lookback_period+j] + data['low'][i-lookback_period+j] + data['low'][i-lookback_period+j]) / 3) * data['volume'][i-lookback_period+j]

        money_flow_ratio = np.sum(raw_money_flow > 0) / np.sum(raw_money_flow < 0)

        col[i] = 100 - (100 / (1 + money_flow_ratio))

# Additional Resources
# https://school.stockcharts.com/doku.php?id=technical_indicators:money_flow_index_mfi
