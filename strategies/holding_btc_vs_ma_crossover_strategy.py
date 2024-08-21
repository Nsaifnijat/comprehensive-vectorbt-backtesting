# -*- coding: utf-8 -*-

import vectorbt as vbt

#getting data for bitcoin
price = vbt.YFData.download('BTC-USD').get('Close')


#executing backtest, holding strategy, here is how much we could make if we held btc from 2014
pf = vbt.Portfolio.from_holding(price, init_cash=100)
print(pf.total_profit())



#Buy whenever 10-day SMA crosses above 50-day SMA and sell when opposite:
fast_ma = vbt.MA.run(price, 10)
slow_ma = vbt.MA.run(price, 50)
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=100)
print(pf.total_profit())







