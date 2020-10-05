#Link:  https://www.investopedia.com/terms/r/rsi.asp

# Relative Strength Index
def RSI():
    net = (data['close'][0] - data['open'][0]) / float(data['open'][0])

    ave_gain = [net if net > 0 else 0.0]
    ave_loss = [abs(net) if net < 0 else 0]
    for i in range(1, len(data.index)):  #enumerate(data['open'][1:], start=1):
        net = (data['close'][i] - data['open'][i]) / float(data['open'][i]) # percentage of this days gain or loss
        #day_ave_gain = ((net if net > 0 else 0.0) + ave_gain[i-1]) / float(i+1)
        #day_ave_loss = ((abs(net) if net < 0 else 0) + ave_loss[i-1]) / float(i+1) #float('-inf')
        ave_gain.append(((net if net > 0 else 0.0) + ave_gain[i-1]) / float(i+1))
        ave_loss.append(((abs(net) if net < 0 else 0) + ave_loss[i-1]) / float(i+1))
