# -*- coding: utf-8 -*-

import vectorbt as vbt
import numpy as np

btc_price =  vbt.YFData.download('BTC-USD',start='2016-01-01',end='2021-12-01')
#print(whole dataframe)
#print(btc_price.get())
price = btc_price.get('Close')

#n is data division, set_lens that 108 is out of sample len
figure = price.vbt.rolling_split(n=20,window_len=360,set_lens=(108,), left_to_right=False,plot=True)
figure.update_layout(width=1280,height=720)
figure.show()

#the following returns tuples when we unpack
(in_sample_prices,in_sample_dates),(out_sample_prices,out_sample_dates)= price.vbt.rolling_split(n=20,window_len=360,set_lens=(108,), left_to_right=False)

#print(in_sample_dates)
#print(out_sample_dates)

windows = np.arange(10,50)

fast_ma, slow_ma = vbt.MA.run_combs(in_sample_prices,windows)

entries= fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

#direction makes it buy and sell 
portfolio = vbt.Portfolio.from_signals(in_sample_prices, entries, exits, freq='1D',direction='both')
performance = portfolio.sharpe_ratio()

print(performance[performance.groupby('split_idx').idxmax()].index)