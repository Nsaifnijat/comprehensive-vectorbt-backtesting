import vectorbt as vbt
import pandas as pd
import numpy as np
import datetime


end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days = 2 )


btc_price = vbt.YFData.download(
    "BTC-USD",
    #putting the timeframe, put start and end dates
    interval = "1m",
    start = start_date,
    end = end_date,
    missing_index = "drop").get('Close')


def custom_indicator(close, window= 14):
    
    rsi = vbt.RSI.run(close,window = window)
    return rsi.rsi

ind = vbt.IndicatorFactory(
    class_name = "Combination",
    short_name = "comb",
    input_names = ["close"],
    param_names = ["window"],
    output_names = ["value"]
    ).from_apply_func(
        custom_indicator,
        window = 14)
        
result = ind.run(
    btc_price,
    window = 21)
print(result.value)