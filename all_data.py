import pandas as pd
from sqlalchemy import create_engine
import numpy as np

def resample_and_fill_in_na(non_sampled_df):
    resampled_df = non_sampled_df.resample('T').mean()
    resampled_df['1. open'] = resampled_df['1. open'].fillna(1.1111111111111111111111)
    resampled_df['2. high'] = resampled_df['2. high'].fillna(1.1111111111111111111111)
    resampled_df['3. low'] = resampled_df['3. low'].fillna(1.1111111111111111111111)
    resampled_df['4. close'] = resampled_df['4. close'].fillna(1.1111111111111111111111)
    resampled_df['5. volume'] = resampled_df['5. volume'].fillna(1.1111111111111111111111)
    return resampled_df


def drop_non_business_days_and_trim_hours(un_trimmed_df):
    trimmed_df = un_trimmed_df[un_trimmed_df.index.dayofweek < 5]
    trimmed_df = trimmed_df.drop(trimmed_df.between_time("00:00", "9:30").index)
    trimmed_df = trimmed_df.drop(trimmed_df.between_time("16:00", "00:00").index)
    return trimmed_df


def drop_incomplete_days(df_incomplete):
    df_test = df_incomplete[df_incomplete['1. open'] != 1.1111111111111111111111]
    gp = df_test.groupby(df_test.index.date).aggregate(np.count_nonzero)
    tf = gp[gp['1. open'] > 300].reset_index()
    tf['date_kk'] = pd.to_datetime(tf['level_0'])
    df_incomplete['date_kk'] = pd.to_datetime(df_incomplete.index.date)
    final_df = df_incomplete.reset_index().merge(tf, how='outer', indicator=True, on=['date_kk']).set_index('date')
    final_df = final_df.loc[final_df._merge == 'both']
    final_df = final_df.drop(
        ['index_x', 'date_kk', 'level_0', 'index_y', '1. open_y', '2. high_y', '3. low_y', '4. close_y', '5. volume_y',
         '_merge'], axis=1)
    final_df = final_df.rename(
        columns={"1. open_x": '1. open', '2. high_x': '2. high', '3. low_x': '3. low', '4. close_x': '4. close',
                 '5. volume_x': '5. volume'})
    final_df = final_df.dropna()
    final_df.index = pd.DatetimeIndex(final_df.index)
    return final_df


def create_engine_for_db():
    engine = create_engine('postgresql://django@68.226.133.212:5440/inner_db')
    return engine


def get_list_of_symbols_from_db():
    symbols = pd.read_sql("stocks", create_engine_for_db())
    symbols = symbols.sort_values(by=['data_points'], ascending=True)
    print(symbols[:4])
    return symbols['stock'].values.tolist()


def get_dataframe(stock):
    data = pd.read_sql(stock, create_engine_for_db())
    return data


def set_index_for_time_series(non_time_index):
    non_time_index.set_index('date', inplace=True)
    non_time_index.index = pd.DatetimeIndex(non_time_index.index)
    return non_time_index

def clean_data_and_sort(unsorted_df):
    sorted_df = unsorted_df.drop_duplicates()
    sorted_df = sorted_df.sort_values('date')
    return sorted_df


# stock_list = get_list_of_symbols_from_db()
# for i in stock_list:
#     x = 0
#     error = 0
#     try:
#         df = get_dataframe(i)
#         df = set_index_for_time_series(df)
#         df = df.drop(columns=['index'], axis=1)
#         df_len = len(df)
#         df = resample_and_fill_in_na(df)
#         df = drop_non_business_days_and_trim_hours(df)
#         df = drop_incomplete_days(df)
#         print(x, "/", len(stock_list), "    ", i, "           ", "error: ", error)
#         if df_len > 0:
#
#
#     except Exception as ex:
#         print(ex)
#         error += 1
#     x += 1



error = 0
x = 0
stock_list = get_list_of_symbols_from_db()
for i in stock_list:
    try:
        df = get_dataframe(i)
        df_len = len(df)
        print(x, "/", len(stock_list), "    ", i, "           ", "error: ", error)
        if df_len > 0:
            df = clean_data_and_sort(df)
            df = set_index_for_time_series(df)
            df = resample_and_fill_in_na(df)
            df = drop_non_business_days_and_trim_hours(df)
            df = drop_incomplete_days(df)
            with open("Data/all_data.csv", "a") as f:
                df.to_csv(f, header=False, line_terminator="\n", sep=",")

    except Exception as ex:
        print(ex)
        error += 1
    x += 1