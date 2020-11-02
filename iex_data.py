import requests
import datetime as dt
from datetime import datetime
import pandas as pd
from urllib import parse
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert
import numpy as np


def get_list_of_symbols_from_db():
    df = pd.read_sql("stocks", create_engine_for_db())
    df = df.sort_values(by=['date_updated'])
    return df['stock'].values.tolist()


def get_list_of_symbol_date_from_db():
    df = pd.read_sql("stocks", create_engine_for_db())
    df = df.sort_values(by=['date_updated'])
    print(df.info())
    return df['date_updated'].astype(str).tolist()


x = -1


def create_engine_for_db():
    engine = create_engine('postgresql://django@68.226.133.212:5440/inner_db')
    return engine


def store_data_to_csv(df, ticker):
    engine = create_engine_for_db()
    metadata = MetaData(bind=None)
    stocks = Table('stocks', metadata, autoload=True, autoload_with=engine)
    stmt = insert(stocks).values(stock=ticker, date_created=datetime.now(), date_updated=datetime.now(),
                                 data_points=len(df))
    stmt = stmt.on_conflict_do_update(
        index_elements=['stock'],
        set_=dict(date_updated=datetime.now(),
                  data_points=len(df))
    )
    engine.execute(stmt)
    print('done', end=" ")
    df.to_sql(ticker, create_engine_for_db(), if_exists='append', method='multi')


class Stock:
    __baseURL = 'https://cloud.iexapis.com/stable/'  # IEX base url
    __tokenList = ['pk_cf785a0c68894671b2ea14dae273c2a0', 'pk_a43a4343e4af4e22b96aedb4975c05b1',
                   'pk_4971e9711afb4eefa25eaff6af898275',
                   'pk_6d72dc3e12c446cfb9c73a6c8a0930a8']  # Token List - We can add more tokens if we need more
    __token = __tokenList[0]
    __sandbox = False
    __save_path = "./data/stockdata/"
    __error_path = "./data/error/stock_error.csv"

    __sandboxBaseURL = 'https://sandbox.iexapis.com/stable/'
    __sandboxToken = 'Tpk_de94e88066424a5f8758d1a1297b9c99'

    def __init__(self, ticker='', sandbox=False):
        self.__ticker = parse.quote(ticker)
        self.__url = Stock.__baseURL
        self.__token = Stock.__token
        self.__sandboxBaseUrl = Stock.__sandboxBaseURL
        self.__sandboxToken = Stock.__sandboxToken
        if sandbox:
            self.__url = Stock.__sandboxBaseURL
            self.__token = Stock.__sandboxToken
            self.__sandbox = True
            self.__save_path = "../data/stockdata/test/"

    @staticmethod
    def getSupportedStocks():
        url = 'https://cloud.iexapis.com/beta/ref-data/symbols?token=' + Stock.__token
        print(url)
        resp = requests.get(url)
        if resp.status_code != 200:
            print('Something went wrong!')
        supported_stocks = []
        for item in resp.json():
            supported_stocks.append(item['symbol'])
        return supported_stocks

    def changeToken(self):
        global x
        x += 1
        if x > len(self.__tokenList) - 1:
            x = 0

        self.__token = self.__tokenList[x]
        return self.__token

    @staticmethod
    def change_datestring_to_dateobj(date):
        date_day = datetime.strptime(date, '%Y-%m-%d %H:%M')
        return date_day

    def get_ohlc_day(self, days_back):
        ohlc = []
        i = 0
        while i < days_back:
            time_delta = dt.timedelta(days=i)
            today = dt.date.today()
            current_day = today - time_delta
            date = '{:02d}{:02d}{:02d}'.format(current_day.year, current_day.month, current_day.day)
            url = self.__url + 'stock/' + self.__ticker + '/chart/date/' + date + '/?chartByDay=true&token=' + self.__token
            resp = requests.get(url)
            if resp.status_code != 200:
                print('Something went wrong!')
            if not (len(resp.json()) > 0):
                days_back += 1
            for item in resp.json():
                ohlc.append({'date': item['date'], 'open': item['open'], 'high': item['high'], 'low': item['low'],
                             'close': item['close']})
            i += 1
        return ohlc

    def get_ohlc_minute(self, days_back=None, start_date=None, end_date=None):

        today = dt.date.today()
        i = 0
        if start_date and end_date:
            days_back_time = datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
            days_back = days_back_time.days
            today = datetime.strptime(end_date, '%Y-%m-%d').date()

        while i < days_back:
            print(i, "/", days_back, "    ", self.__ticker)
            time_delta = dt.timedelta(days=i)
            current_day = today - time_delta

            if current_day.weekday() != 6:
                if current_day.weekday() != 5:
                    if not self.__sandbox:
                        current_day = str(current_day).replace("-", '')
                        url = self.__url + 'stock/' + self.__ticker + '/intraday-prices/date/' + current_day + '/?chartIEXOnly=true&token=' + self.__token
                    if self.__sandbox:
                        url = self.__url + 'stock/' + self.__ticker + '/intraday-prices/' + current_day + '/?chartIEXOnly=true&format=json&token=' + self.__token

                    resp = requests.get(url)
                    try:
                        json_resp = resp.json()

                        if resp.status_code != 200 or not (len(json_resp) > 0):
                            error = ""
                            if resp.status_code != 200:
                                error = "Response is invalid"
                            if not (len(json_resp) > 0):
                                error = "No response"
                            data = [[datetime.now(), current_day, self.__ticker, resp.status_code, error]]
                            df = pd.DataFrame(data, columns=['current', 'date', 'symbol', 'status_code', 'exception'])
                            df.to_csv(self.__error_path, mode='a', header=False)

                        df = pd.DataFrame(json_resp)  # turn response to pandas df
                        df['date'] = df['date'] + " " + df['minute']  # concat date and min cols
                        df['date'] = df['date'].apply(lambda iter_date: self.change_datestring_to_dateobj(
                            iter_date))  # iter over date and strip the string into datetime obj
                        df = df.drop(labels=["minute", "label", "average", "numberOfTrades", "notional"],
                                     axis=1)  # dropped unused cols
                        df = df.rename(
                            columns={"open": "1. open", "high": "2. high", "low": "3. low", "close": "4. close",
                                     "volume": "5. volume"})  # store this df to db or csv for reprocessing
                        store_data_to_csv(df, self.__ticker)

                    except Exception as ex:
                        if 'date' in str(ex):
                            ex = "No data returned"

                        data = [[datetime.now(), current_day, self.__ticker, resp.status_code, ex]]
                        df = pd.DataFrame(data, columns=['current', 'date', 'symbol', 'status_code', 'exception'])
                        df.to_csv(self.__error_path, mode='a', header=False)
                        print('erre', end=" ")

                        self.changeToken()

                    self.changeToken()
                else:
                    print('wend', end=" ")
            else:
                print('wend', end=" ")
            i += 1

        return df


def check_for_skip():
    df = pd.read_csv("data/error/stock_error.csv")
    # df = df.drop_duplicates()
    df = df.dropna()
    print(df.head())
    gb = df.groupby('symbol').aggregate(np.count_nonzero).reset_index()
    print(gb)
    tf = gb[gb['current'] > 400].reset_index()
    print(tf.head())
    return tf['symbol'].values.tolist()


def main():
    z = 0
    list_stocks = get_list_of_symbols_from_db()
    print(len(list_stocks))
    drop_list = check_for_skip()
    list_O_stocks = [i for i in list_stocks if i not in drop_list]
    print(len(list_O_stocks))
    for i in range(256):
        drop_list = check_for_skip()
        print(drop_list)
        stock = [x for x in get_list_of_symbols_from_db() if x not in drop_list][i]
        print(z, "/", len(list_O_stocks), "    ", stock, "     Last Updated:", get_list_of_symbol_date_from_db()[z])
        stock = Stock(stock)
        stock.get_ohlc_minute(start_date='2018-09-30', end_date='2020-09-30')
        z += 1


main()
