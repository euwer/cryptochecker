import requests
import numpy as np
import talib

# Binance API anahtarlarınızı buraya girin
api_key = 'Binance_API_anahtarınız'
api_secret = 'Binance_API_anahtar_şifreniz'

# Binance testnet API URL'si
api_base_url = 'https://testnet.binance.vision/api/v3'

# Bütün coinlerin fiyatlarını çeken fonksiyon
def get_all_prices():
    endpoint = '/ticker/price'
    url = api_base_url + endpoint
    response = requests.get(url)
    data = response.json()
    return data

# RSI hesaplaması için fiyat verilerini çeken fonksiyon
def get_historical_prices(symbol, interval):
    endpoint = '/klines'
    url = api_base_url + endpoint + '?symbol=' + symbol + '&interval=' + interval
    response = requests.get(url)
    data = response.json()
    prices = np.array([float(entry[4]) for entry in data])  # Kapanış fiyatlarını al
    return prices

# RSI hesaplaması
def calculate_rsi(prices, period=14):
    rsi = talib.RSI(prices, timeperiod=period)
    return rsi

# Tüm coinlerin fiyatlarını ve RSI'larını yazdıran ana fonksiyon
def main():
    prices = get_all_prices()

    for coin in prices:
        symbol = coin['symbol']
        price = coin['price']

        # Coin'in son 15 dakikalık RSI değerini al
        prices_15m = get_historical_prices(symbol, '15m')
        rsi_15m = calculate_rsi(prices_15m)[-1]

        # Coin'in son 5 dakikalık RSI değerini al
        prices_5m = get_historical_prices(symbol, '5m')
        rsi_5m = calculate_rsi(prices_5m)[-1]

        # Coin'in son 3 dakikalık RSI değerini al
        prices_3m = get_historical_prices(symbol, '3m')
        rsi_3m = calculate_rsi(prices_3m)[-1]

        print(f"Coin: {symbol}")
        print(f"Fiyat: {price}")
        print(f"RSI (15 dakika): {rsi_15m}")
        print(f"RSI (5 dakika): {rsi_5m}")
        print(f"RSI (3 dakika): {rsi_3m}")
        print("-------------------------------------")

if __name__ == '__main__':
    main()
