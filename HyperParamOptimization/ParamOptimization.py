import vectorbt as vbt
import pandas as pd
import numpy as np
import datetime


end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days = 2 )


btc_price = vbt.YFData.download(
    ["BTC-USD","ETH-USD"],
    #putting the timeframe, put start and end dates
    interval = "1m",
    start = start_date,
    end = end_date,
    missing_index = "drop").get('Close')


def custom_indicator(close, rsi_window = 14, ma_window= 50, entry = 30, exitt = 70):
    close_5m = close.resample("5T").last() 
    #rsi = vbt.RSI.run(close,window = rsi_window).rsi.to_numpy()
    rsi = vbt.RSI.run(close_5m ,window = rsi_window).rsi
    rsi, _ = rsi.align(close,
                       #index matching, 0 is index, we mathc based on th eindex 
                       broadcast_axis = 0,
                       method = "ffill",
                       #take keys from the right table only,
                       join="right")
    #now lets convert the above to numpy
    close = close.to_numpy()
    rsi = rsi.to_numpy()
    ma = vbt.MA.run(close, ma_window).ma.to_numpy()
    #where rsi > 70 put 01 else put 0
    trend = np.where( rsi > exitt, -1, 0)
    #trend = np.where( rsi < 30, 1, trend)
    trend = np.where( (rsi < entry) & (close < ma), 1, trend)
    return trend

ind = vbt.IndicatorFactory(
    class_name = "Combination",
    short_name = "comb",
    input_names = ["close"],
    param_names = ["rsi_window","ma_window","entry","exitt"],
    output_names = ["value"]
    ).from_apply_func(
        custom_indicator,
        rsi_window = 14,
        ma_window = 50,
        entry = 30,
        exitt = 70,
        #by default the close price we provide to the indicator will be converted to numpy
        #if we need pd then use the following
        keep_pd = True)

#combination with all
result = ind.run(
    btc_price,
    rsi_window = [21,30,50],
    ma_window = [50,60,100],
    entry = [30,40],
    exitt = [60,70],
    param_product = True)


#second method
result = ind.run(
    btc_price,
    rsi_window = np.arange(10,40, step=3,dtype=int),
    ma_window = np.arange(20,200, step=20, dtype=int),
    entry = np.arange(10,40, step=4, dtype=int),
    exitt = np.arange(60,85, step=4,dtype=int),
    param_product = True)



entries = result.value == 1.0
exits = result.value == -1.0

pf = vbt.Portfolio.from_signals(btc_price, entries, exits)

returns = pf.total_return()
print(returns.max())
print(returns.idxmax())


#get the returns for a specific symbol

returns = returns[ returns.index.isin(['ETH-USD'],level="symbol")]
print(returns.max())
print(returns.idxmax())








