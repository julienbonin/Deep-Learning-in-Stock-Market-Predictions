import datetime
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

pd.set_option('display.max_rows', None)


def create_engine_for_db():
    engine = create_engine('postgresql://django@68.226.133.212:5440/inner_db')
    return engine

def create_engine_for_final_db():
    engine = create_engine('postgresql://django@68.226.133.212:5440/final_lstm_db')
    return engine

def save_data_to_final_db(final_data,stock):
    final_data.to_sql(stock,create_engine_for_final_db())


def get_list_of_symbols_from_db():
    symbols = pd.read_sql("stocks", create_engine_for_db())
    symbols = symbols.sort_values(by=['date_updated'])
    return symbols['stock'].values.tolist()


def get_dataframe(stock):
    data = pd.read_sql(stock, create_engine_for_db())
    return data


def clean_data_and_sort(unsorted_df):
    sorted_df = unsorted_df.drop_duplicates()
    sorted_df = sorted_df.sort_values('date')
    return sorted_df


def set_index_for_time_series(non_time_index):
    non_time_index.set_index('date', inplace=True)
    non_time_index.index = pd.DatetimeIndex(non_time_index.index)
    return non_time_index


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
    final_df = final_df.drop(['index_x', 'date_kk', 'level_0', 'index_y', '1. open_y', '2. high_y', '3. low_y', '4. close_y', '5. volume_y','_merge'], axis=1)
    final_df = final_df.rename(columns={"1. open_x": '1. open', '2. high_x': '2. high', '3. low_x': '3. low', '4. close_x': '4. close','5. volume_x': '5. volume'})
    final_df = final_df.dropna()
    final_df.index = pd.DatetimeIndex(final_df.index)
    return final_df


# def fix_it(data, next, current, future, previous):
#     prev = data.loc[previous]
#     print(prev)
#     foward = data.loc[next]
#     print(foward)
#     avg_open = (prev['1. open'] + foward['1. open']) / 2
#     avg_high = (prev['2. high'] + foward['2. high']) / 2
#     avg_low = (prev['3. low'] + foward['3. low']) / 2
#     avg_close = (prev['4. close'] + foward['4. close']) / 2
#     avg_volume = (prev['5. volume'] + foward['5. volume']) / 2
#     print(avg_open, avg_high, avg_low, avg_close, avg_volume)


#
#     pass
#
#
# import datetime, time
#
# y = 0
# x = datetime.datetime.now() - datetime.timedelta(days=1500)
# dt_y = datetime.datetime.now() - datetime.timedelta(days=1500)
# for i, r in kk.iterrows():
#     dt = pd.to_datetime(r.name)
#     dt_f = dt + datetime.timedelta(minutes=1)
#
#     if y == 0:
#         x = dt
#         dt_y = dt_f
#
#     else:
#
#         if dt != dt_y:
#
#             print(dt," != ",dt_y)
#             yy = input("c or f?")
#             if yy == "c":
#                 dt_y = dt_f
#
#                 continue
#             if yy == "f":
#                 fix_it(kk, dt_f, dt, dt_y, x)
#                 dt_y = dt_f
#                 continue
#
#             else:
#                 break
#         else:
#             x = dt - datetime.timedelta(minutes=1)
#             dt_y = dt_f
#     print("dt", dt, "x", x, "dt_f", dt_f, "dt_y", dt_y)
#     y += 1

list = []


def drop_day(df, current_id):
    result = df.iloc[current_id]
    str_day = str(pd.to_datetime(result.name).date())
    kk = df.loc[str_day]
    df.drop(labels=kk.index, axis='index', inplace=True)
    df.to_csv("asdfasdfa.csv")
    return df


def get_last(df, i):
    result = df.iloc[i]
    if result['1. open'] != 1.1111111111111111111111:
        return i
    else:
        return get_last(df, i - 1)


def get_first(df, i):
    result = df.iloc[i]
    if result['1. open'] != 1.1111111111111111111111:
        return i
    else:
        return get_first(df, i + 1)


def check_consistency(inconsistent_df):
    print(len(inconsistent_df))
    for index, row in inconsistent_df.iterrows():

        try:
            r = row.copy()
            if r['1. open'] == 1.1111111111111111111111:
                # try:
                #     if pd.to_datetime(r.name).time() == pd.to_datetime(r.name).time().replace(hour=9, minute=31, second=0,
                #                                                                               microsecond=0):
                id = inconsistent_df.index.get_loc(row.name)
                prev = inconsistent_df.iloc[id - 1]

                # else:
                #     prev = inconsistent_df.loc[index - datetime.timedelta(minutes=1)]

                # if pd.to_datetime(r.name).time() == pd.to_datetime(r.name).time().replace(hour=15, minute=59, second=0,
                #                                                                           microsecond=0):
                #     id = inconsistent_df.index.get_loc(index)
                future = inconsistent_df.iloc[id + 1]
                # else:
                # future = inconsistent_df.loc[index + datetime.timedelta(minutes=1)]

                if prev['1. open'] == 1.1111111111111111111111:
                    current_id = inconsistent_df.index.get_loc(index)
                    last_id = get_last(inconsistent_df, current_id)
                    prev = inconsistent_df.iloc[last_id]

                if future['1. open'] == 1.1111111111111111111111:
                    current_id = inconsistent_df.index.get_loc(index)
                    last_id = get_first(inconsistent_df, current_id)

                    future = inconsistent_df.iloc[last_id]
                    if last_id - current_id > 100:
                        inconsistent_df = drop_day(inconsistent_df, current_id)
                        continue

                r['1. open'] = (prev['1. open'] + future['1. open']) / 2
                r['2. high'] = (prev['2. high'] + future['2. high']) / 2
                r['3. low'] = (prev['3. low'] + future['3. low']) / 2
                r['4. close'] = (prev['4. close'] + future['4. close']) / 2
                r['5. volume'] = (prev['5. volume'] + future['5. volume']) / 2
                inconsistent_df.loc[index] = r

        except KeyError as ex:
            # print(ex)
            # inconsistent_df = drop_day(inconsistent_df, current_id)
            continue

    return inconsistent_df


def main():
    x=0
    stock_list = get_list_of_symbols_from_db()[0]
    for i in stock_list:
        print(x,"/",len(stock_list),"    ",i)
        df = get_dataframe(i)
        df = clean_data_and_sort(df)
        df = set_index_for_time_series(df)
        df = resample_and_fill_in_na(df)
        df = drop_non_business_days_and_trim_hours(df)
        df = drop_incomplete_days(df)
        df = check_consistency(df)
        df.to_csv("qqqqqqqqqqqqqqqq.csv")
        break




main()
