#Link:  https://www.investopedia.com/terms/s/sma.asp

# Simple Moving Average


def sma(data, column_name, windows):
    """
    this function is used to calculate simple moving averages

    :param data: entire df
    :param column_name: string name of column to calculate
    :param windows: window size
    :return: new column data
    """
    new_column = data[column_name].rolling(windows).mean()

    return new_column
