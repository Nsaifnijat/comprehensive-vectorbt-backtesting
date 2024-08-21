

# TA-lib-> using talib boosts speeds, as talib is written in assembly and is fast
import vectorbt as vbt
import pandas as pd
import numpy as np
import datetime
import plotly
from numba import njit
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days = 2 )


btc_price = pd.read_csv("data.csv")
btc_price['Datetime'] = pd.to_datetime(btc_price["Datetime"])
btc_price.set_index("Datetime", inplace=True)

RSI = vbt.IndicatorFactory.from_talib('RSI')

#the following converts the code to machine code
@njit
def produce_signals(rsi, entry, exitt):
    trend = np.where( rsi > exitt, -1, 0)
    trend = np.where( (rsi < entry) , 1, trend)
    return trend
def custom_indicator(close, rsi_window = 14, entry = 30, exitt = 70):
   
    #using the above wrapper, now we can use even many symbosl
    rsi = RSI.run(close, rsi_window).real.to_numpy()
    return produce_signals(rsi, entry, exitt)

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
        )

        
rsi_window = np.arange(10,40, step=1,dtype=int)
master_returns = []
#you can use loop or loop inside loop to divide work on the ram to avoid hang
for window in rsi_window:
    
    result = ind.run(
        btc_price,
        rsi_window = window,
        entry = np.arange(10,40, step=1, dtype=int),
        exitt = np.arange(60,85, step=1,dtype=int),
        param_product = True)
    entries = result.value == 1.0
    exits = result.value == -1.0
    pf = vbt.Portfolio.from_signals(btc_price, entries, exits)
    master_returns.append(pf.total_return())

returns = pd.concat(master_returns)

#grouping and mapping
returns = pf.total_return()
print(returns.to_string())
print(returns.max())
print(returns.idxmax())







