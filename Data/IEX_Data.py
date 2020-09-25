import requests
import datetime


class Stock:
    __baseURL = 'https://cloud.iexapis.com/stable/'  # IEX base url
    __tokenList = ['pk_cf785a0c68894671b2ea14dae273c2a0']  # Token List - We can add more tokens if we need more
    __token = __tokenList[0]

    __sandboxBaseUrl = 'https://sandbox.iexapis.com/stable/'
    __sandboxToken = 'Tpk_de94e88066424a5f8758d1a1297b9c99'

    def __init__(self, ticker='', sandbox=False):
        self.__ticker = ticker
        self.__baseURL = Stock.__baseURL
        self.__token = Stock.__token
        self.__sandboxBaseUrl = Stock.__sandboxBaseUrl
        self.__sandboxToken = Stock.__sandboxToken
        self.__url = (Stock.__sandboxBaseURL if sandbox else Stock.__baseURL)

    @staticmethod
    def getSupportedStocks():
        url = 'https://cloud.iexapis.com/beta/ref-data/symbols?token=' + Stock.__token
        resp = requests.get(url)
        if resp.status_code != 200:
            print('Something went wrong!')
        supported_stocks = []
        for item in resp.json():
            supported_stocks.append(item['symbol'])
        return supported_stocks

    @staticmethod
    def changeToken(i):
        Stock.__token = Stock.__tokenList[i]

    def get_ohlc(self, days_back):
        ohlc = []
        i = 0
        while i < days_back:
            time_delta = datetime.timedelta(days=i)
            today = datetime.date.today()
            current_day = today - time_delta
            date = '{:02d}{:02d}{:02d}'.format(current_day.year, current_day.month, current_day.day)
            url = self.__url + 'stock/' + self.__ticker + '/chart/date/' + date + '/?chartByDay=true&token=' + self.__token
            resp = requests.get(url)
            if resp.status_code != 200:
                print('Something went wrong!')
            if not(len(resp.json()) > 0):
                days_back += 1
            for item in resp.json():
                ohlc.append({'date': item['date'], 'open': item['open'], 'high': item['high'], 'low': item['low'], 'close': item['close']})
            i += 1
        return ohlc


def main():

    #   Static Methods
    #   These methods can be used without a class instance
    #   getSupportedStocks()    -> Returns an array of IEX supported symbols
    #                           -> We can filter the symbols as needed
    #   changeToken()           -> Use this method to iterate through tokens

    #   Class Instantiation
    #   Stock(ticker, sandbox)           -> ticker is a string from the list of supported IEX tickers
    #                                    -> sandbox can be set to True if you want to use test data (no limit on calls) [default=False]
    #   Instance Methods
    #   These methods must be called by a class instance
    #   get_ohlc(param)              -> returns a list of Open, High, Low, and Close price for single days
    #                                -> param is number of days back.

    # print(Stock.getSupportedStocks()) # Uncomment this line to get a list of IEX supported stocks

    # Uncomment the lines below to create an instance and retrieve the OHLC data for the previous 5 days for Apple Inc.
    # stk = Stock('AAPL')

    pass  # remove this before running the code.


main()
