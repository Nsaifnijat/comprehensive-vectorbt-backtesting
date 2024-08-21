import vectorbt as vbt
import datetime
import plotly
import numpy as np
import talib
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days = 7 )

#to get multiple tickers

btc_price = vbt.YFData.download(
    "BTC-USD",
    #putting the timeframe, put start and end dates
    interval = "1m",
    start = start_date,
    end = end_date,
    missing_index = "drop")
print(help(vbt.indicators.__all__))
#print(btc_price.data['BTC-USD'].columns)
btc_price = btc_price.data['BTC-USD']
def custom_indicator(close, sma_30, sma_200, cci_len):
    #if (df['close'].iloc[-2] > df['close'].iloc[-3]) and (df['close'].iloc[-2] < df['sma_30'].iloc[-2]) and (df['close'].iloc[-2] < df['sma_200'].iloc[-2]) and (df['cci_20'].iloc[-2] > -90) and (df['cci_20'].iloc[-3] < -90):
    
    close['ma_30'] = talib.SMA(close['Close'], sma_30)
    close['ma_200'] = talib.SMA(close['Close'],sma_200)
    close['cci_20'] = talib.CCI(close['High'],close['Low'],close['Close'],20)
    
    
custom_indicator(btc_price, 30, 200, 20)   
ind = vbt.IndicatorFactory(
    class_name = "Combination",
    short_name = "comb",
    input_names = ["close"],
    param_names = ["sma_30","sma_200","cci_len"],
    output_names = ["value"]
    ).from_apply_func(
        custom_indicator,
        sma_30 = 30,
        sma_200 = 200,
        cci_len = 20,
        #by default the close price we provide to the indicator will be converted to numpy
        #if we need pd then use the following
        keep_pd = True)

#combination with all
result = ind.run(
    btc_price,
     sma_30 = 30,
     sma_200 = 200,
     cci_len = 20,
    param_product = True)





pf = vbt.Portfolio.from_signals(
    btc_price,
    entries,
    exits,
    #stoploss
    sl_stop = 0.005,
    #tp
    tp_stop = 0.001,
    #enable trailing sl
    sl_trail = True,)

fig = pf.plot()
plotly.offline.plot(fig, filename="plotly version of an mpl figure")
