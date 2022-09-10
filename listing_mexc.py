import mexc_spot_v3
import time
from datetime import datetime, date

print('ДА')


def mexc_listing(api, secret, price=None, now_task=None, date_task=None):

    print('ДА')
    price = price
    flag = False
    while True:
        if flag == True:
            break
        current_date_0 = []
        now = datetime.now()
        current_date = str(date.today())
        current_date_1 = current_date.split('-')
        #print(current_date_1)
        current_date_0.append(current_date_1[-1])
        current_date_0.append(current_date_1[-2])
        current_date_0.append(current_date_1[-3])
        current_date = '/'.join(current_date_0)
        #print(current_date)
        current_time = str(now.strftime("%H:%M"))
        print(current_time)
        print(now_task)
        if current_time == now_task:
            flag = True
            buy(api, secret, price)



def buy(api, secret, price=None):
    hosts = "https://api.mexc.com"
    mexc_key = api
    mexc_secret = secret
    while True:
        """place an order"""
        try:
            trade = mexc_spot_v3.mexc_trade(mexc_key=mexc_key, mexc_secret=mexc_secret, mexc_hosts=hosts)
            params = {
               "symbol": "OMNOMUSDT",
               "side": "BUY",
               "type": "LIMIT",
               "quantity": 10,
               "price": '0.00000016'
            }
            response = trade.post_order(params)
            print(response)
            break

        except Exception as e:
            print(e)
            break

mexc_listing(432, 342, now_task='18:57', date_task='01/09/2022')