# -*- coding: utf-8 -*-

import vectorbt as vbt
import numpy as np

btc_price =  vbt.YFData.download('BTC-USD',start='2016-01-01',end='2021-12-01')
#print(whole dataframe)
#print(btc_price.get())
price = btc_price.get('Close')

figure = price.vbt.ohlcv.plot(trace_names=['Price'], width=1280,height=720)
figure.show()


windows = np.arange(10,50)

fast_ma, slow_ma = vbt.MA.run_combs(price,windows)

entries= fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

#direction makes it buy and sell 
portfolio = vbt.Portfolio.from_signals(price, entries, exits, freq='1D',direction='both')
print(portfolio.total_return().sort_values().to_string())