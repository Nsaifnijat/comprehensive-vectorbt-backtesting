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


def custom_indicator(close, rsi_window = 14, ma_window= 50):
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
    trend = np.where( rsi > 70, -1, 0)
    #trend = np.where( rsi < 30, 1, trend)
    trend = np.where( (rsi < 30) & (close < ma), 1, trend)
    return trend

ind = vbt.IndicatorFactory(
    class_name = "Combination",
    short_name = "comb",
    input_names = ["close"],
    param_names = ["rsi_window","ma_window"],
    output_names = ["value"]
    ).from_apply_func(
        custom_indicator,
        rsi_window = 14,
        ma_window = 50,
        #by default the close price we provide to the indicator will be converted to numpy
        #if we need pd then use the following
        keep_pd = True)
"""        
result = ind.run(
    btc_price,
    rsi_window = 21,
    ma_window = 50)
#print(result.value.to_string())
#running multiple params for ma
result = ind.run(
    btc_price,
    rsi_window = 21,
    ma_window = [50,70,100])
#different params for both in pairs
result = ind.run(
    btc_price,
    rsi_window = [21,30,50],
    ma_window = [50,60,100])
"""
#combination with all
result = ind.run(
    btc_price,
    rsi_window = [21,30,50],
    ma_window = [50,60,100],
    param_product = True)


entries = result.value == 1.0
exits = result.value == -1.0

pf = vbt.Portfolio.from_signals(btc_price, entries, exits)
#print(pf.stats())
print(pf.total_return())