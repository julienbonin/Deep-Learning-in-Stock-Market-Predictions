# Link:  https://www.investopedia.com/terms/m/mfi.asp
import numpy as np


# MFI - Money Flow Index
def MFI(data, lookback_period):
    money_flow_ratio = np.zeros(len(data))
    typical_price = (data['2. high'] + data['3. low'] + data['4. close']) / 3.0
    raw_money_flow = typical_price * data['5. volume']
    for j in range(lookback_period, len(raw_money_flow)):
        pos = 1
        neg = 1
        for i in range(j-lookback_period, j):
            if raw_money_flow[i+1] > raw_money_flow[i]:
                pos += raw_money_flow[i+1]
            elif raw_money_flow[i+1] < raw_money_flow[i]:
                neg += raw_money_flow[i+1]

        money_flow_ratio[j] = pos / neg

    # the three lines below are for if we want to just add the column to the dataframe here
    #col_name = lookback_period, ' day MFI'
    #data[col_name] = 100 - (100 / (1 + money_flow_ratio))
    #retur data

    return 100 - (100 / (1 + money_flow_ratio))

# Additional Resources
# https://school.stockcharts.com/doku.php?id=technical_indicators:money_flow_index_mfi
