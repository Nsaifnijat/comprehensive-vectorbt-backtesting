
# TA-lib-> using talib boosts speeds, as talib is written in assembly and is fast
import vectorbt as vbt
import pandas as pd
import numpy as np
import datetime
import plotly
import talib
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days = 2 )


btc_price = pd.read_csv("data.csv")
btc_price['Datetime'] = pd.to_datetime(btc_price["Datetime"])
btc_price.set_index("Datetime", inplace=True)


#we can also use talib wrapper instead of talib directly
RSI = vbt.IndicatorFactory.from_talib('RSI')

def custom_indicator(close, rsi_window = 14, entry = 30, exitt = 70):
   
    #using the above wrapper, now we can use even many symbosl
    rsi = RSI.run(close, rsi_window).real
   
    trend = np.where( rsi > exitt, -1, 0)
    trend = np.where( (rsi < entry) , 1, trend)
    return trend

ind = vbt.IndicatorFactory(
    class_name = "Combination",
    short_name = "comb",
    input_names = ["close"],
    param_names = ["rsi_window","entry","exitt"],
    output_names = ["value"]
    ).from_apply_func(
        custom_indicator,
        rsi_window = 14,
        entry = 30,
        exitt = 70,
        to_2d = False,
        )


result = ind.run(
    btc_price,
    rsi_window = np.arange(10,40, step=3,dtype=int),
  
    entry = np.arange(10,40, step=4, dtype=int),
    exitt = np.arange(60,85, step=4,dtype=int),
    param_product = True)



entries = result.value == 1.0
exits = result.value == -1.0

pf = vbt.Portfolio.from_signals(btc_price, entries, exits)

#grouping and mapping
returns = pf.total_return()
print(returns.to_string())
print(returns.max())
print(returns.idxmax())





