from re import U
import ccxt
import datetime
import pprint
import time
import pandas as pd

#api키 입력
api_key = 'LPEmD9XK5nVUqNhvLpCS4RxNii29QHerFr4R3KFNKUTCUPvbyXsuItdWLMP6tc7u'
secret = 'RNJY4sAAggH1GokfNufib5kE1DeQzwdH5m1vHn8dh5orObNgH4o91mAir45s0Ucb' 

# binance 객체 생성
binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True, 
})

def pprice(): #현재가
    binance = ccxt.binance()
    ticker = binance.fetch_ticker('BTC/USDT')
    return(ticker['open'], ticker['high'], ticker['low'], ticker['close'])

def asset(): #잔고조회
    balance = binance.fetch_balance(params={"type": "future"})
    return balance['USDT']

def longbuy(n): #롱 포지션 진입
    order = binance.create_market_buy_order(
    symbol="BTC/USDT",
    amount=n)
    return order

def longsell(n): #롱 포지션 정리
    order = binance.create_market_sell_order(
    symbol="BTC/USDT",
    amount=n)
    return order

def shortbuy(n): #숏 진입
    order = binance.create_market_sell_order(
    symbol="BTC/USDT",
    amount=n, )
    return order

def shortsell(n): #숏 정리
    order = binance.create_market_buy_order(
    symbol="BTC/USDT",
    amount=n, )
    return order

def leverage(n): #레버리지 설정
    markets = binance.load_markets()
    symbol = "BTC/USDT"
    market = binance.market(symbol)
    leverage = n

    resp = binance.fapiPrivate_post_leverage({
        'symbol': market['id'],
        'leverage': leverage
    })
    return leverage

def ma(n): #n일 이동평균선
    btc = binance.fetch_ohlcv(
    symbol="BTC/USDT", 
    timeframe='1s', 
    since=None, 
    limit=10)
    df = pd.DataFrame(btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    ma = df['close'].rolling(n).mean().iloc[-1]
    return ma

def masl(n):
    btc = binance.fetch_ohlcv(
    symbol="BTC/USDT", 
    timeframe='1s', 
    since=None, 
    limit=10)
    df = pd.DataFrame(btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    ma = df['close'].rolling(n).mean().iloc[-1]
    sl = ma['599'] - ma['589']
    return sl

while True:
    if ma(5)['599'] == ma(20)['599']:
        if masl(5) > masl(20):
            leverage(20)
            longbuy(asset()*80/100)
        elif masl(5) > masl(20):
            leverage(20)
            shortbuy(asset()*80/100)
        else:
            print('....... 대기.........')
    else:
        print('.....한조 대기중....')
    break