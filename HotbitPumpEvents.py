import mexc_spot_v3
import time
from telethon import TelegramClient
from telethon.sync import TelegramClient
import requests

symbols = []
req = requests.get('https://www.mexc.com/open/api/v2/market/api_default_symbols')
print(req.text)
#for i in req.text:
#    print(i)
#    try:
#        symbols.append(i)
#    except Exception:
#        pass
#print(symbols)

hosts = "https://api.mexc.com"
mexc_key = "your apiKey"
mexc_secret = "your secretKey"

name = 'anon1'
api_id = 13024076                  # API ID (получается при регистрации приложения на my.telegram.org)
api_hash = "911a5d0e19b025a6913c2328ce7b03a0"              # API Hash (оттуда же)
phone_number = "+6281770997011"    # Номер телефона аккаунта, с которого будет выполняться код
chat = 'HotbitPumpEvents'


# Spot Trade
def buy(symb):
    for i in range(3):
        trade = mexc_spot_v3.mexc_trade(mexc_key=mexc_key, mexc_secret=mexc_secret, mexc_hosts=hosts)
        params = {
            "symbol": f"{symb}USDT",
            "side": "BUY",
            "type": "MARKET",
            "quoteOrderQty": 10,
        }
        response= trade.post_order(params)
        print(response)
    exit()
        #params = {
        #    "symbol": "BTCUSDT",
        #    "side": "BUY",
        #    "type": "LIMIT",
        #    "quantity": 10,
        #    "price": 10
        #}
        #response= trade.post_order(params)
        #print(response)



while True:
    with TelegramClient(name, api_id, api_hash) as client2:
        print('Идет поиск')
        for message in client2.iter_messages(chat, limit=50):
            try:
                if message.text in req.text:
                    print(message.text)
                    buy(message.text)
            except Exception:
                pass


