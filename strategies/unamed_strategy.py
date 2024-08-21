# -*- coding: utf-8 -*-


import vectorbt as vbt
import numpy as np

btc_price =  vbt.YFData.download('EURUSD=X',start='2020-01-01',end='2021-12-01')
price = btc_price.get('Close')
print(price[0])
fast_ma = vbt.MA.run(price, 10, short_name='fast')
slow_ma = vbt.MA.run(price, 20, short_name='slow')

ma50 = vbt.MA.run(price, 50, short_name='50ma')
ma200 = vbt.MA.run(price, 200, short_name='200ma')


rsi =  vbt.RSI.run(price)

ent1 = rsi.rsi_below(30)
ex1 =  rsi.rsi_above(70)

entries= (fast_ma.ma_crossed_above(slow_ma) & rsi.rsi_above(70) & ma50.ma_above(ma200))
print(entries)
exits = fast_ma.ma_crossed_below(slow_ma) & rsi.rsi_below(30) & ma50.ma_below(ma200)

#direction makes it buy and sell 
portfolio = vbt.Portfolio.from_signals(price, entries, exits, freq='1D')

print(portfolio.total_return())