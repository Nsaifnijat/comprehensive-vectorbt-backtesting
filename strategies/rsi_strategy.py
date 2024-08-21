# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from datetime import datetime

import vectorbt as vbt

# Prepare data
start = '2019-01-01 UTC'  # crypto is in UTC
end = '2020-01-01 UTC'
btc_price = vbt.YFData.download('BTC-USD', start=start, end=end).get('Close')

print(btc_price)

fast_ma = vbt.MA.run(btc_price, 10, short_name='fast')
slow_ma = vbt.MA.run(btc_price, 20, short_name='slow')

entries = fast_ma.ma_crossed_above(slow_ma)
print(entries)


exits = fast_ma.ma_crossed_below(slow_ma)
print(exits)

pf = vbt.Portfolio.from_signals(btc_price, entries, exits)
print(pf.total_return())



# Multiple strategy instances: (10, 30) and (20, 30)
fast_ma = vbt.MA.run(btc_price, [10, 20], short_name='fast')
slow_ma = vbt.MA.run(btc_price, [30, 30], short_name='slow')

print(slow_ma)
entries = fast_ma.ma_crossed_above(slow_ma)
print(entries)


exits = fast_ma.ma_crossed_below(slow_ma)
print(exits)

pf = vbt.Portfolio.from_signals(btc_price, entries, exits)
pf.total_return()


# Multiple strategy instances and instruments
eth_price = vbt.YFData.download('ETH-USD', start=start, end=end).get('Close')
comb_price = btc_price.vbt.concat(eth_price,
     keys=pd.Index(['BTC', 'ETH'], name='symbol'))
comb_price.vbt.drop_levels(-1, inplace=True)
print(comb_price)

fast_ma = vbt.MA.run(comb_price, [10, 20], short_name='fast')
slow_ma = vbt.MA.run(comb_price, [30, 30], short_name='slow')

entries = fast_ma.ma_crossed_above(slow_ma)
print(entries)


exits = fast_ma.ma_crossed_below(slow_ma)
print(exits)


pf = vbt.Portfolio.from_signals(comb_price, entries, exits)
pf.total_return()

mean_return = pf.total_return().groupby('symbol').mean()
mean_return.vbt.barplot(xaxis_title='Symbol', yaxis_title='Mean total return')

# Multiple strategy instances, instruments, and time periods
mult_comb_price, _ = comb_price.vbt.range_split(n=2)
print(mult_comb_price)


fast_ma = vbt.MA.run(mult_comb_price, [10, 20], short_name='fast')
slow_ma = vbt.MA.run(mult_comb_price, [30, 30], short_name='slow')

entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

pf = vbt.Portfolio.from_signals(mult_comb_price, entries, exits, freq='1D')
print(pf.total_return())


mean_return = pf.total_return().groupby(['split_idx', 'symbol']).mean()
mean_return.unstack(level=-1).vbt.barplot(
     xaxis_title='Split index',
     yaxis_title='Mean total return',
     legend_title_text='Symbol')







