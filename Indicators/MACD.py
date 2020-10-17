# Link:  https://www.investopedia.com/terms/m/macd.asp

# Moving Average Convergence Divergence
def moving_average_converge_diverge(data, column_name_slow, column_name_fast):
    """
    Calcuate the Moving average converge diverge indicator on what ever column from a dataset

    :param data: the full data frame
    :param column_name_slow: the slow moving column e.g(EMA_26)
    :param column_name_fast: the fast moving column e.g.(EMA_12)
    :return: the new column of data which is slow minus the fast
    """
    new_column = data[column_name_fast] - data[column_name_slow]
    return new_column


def moving_average_converge_diverge_charting(data, column_name, window):
    """
    Use this function strictly for charting purposes

    :param data: the full data frame
    :param column_name: column name of the calculated MACD
    :param window: the number of periods to calculate the mean of
    :return: the new column of data
    """
    new_column = data[column_name].ewm(window).mean()
    return new_column
