#do look for your python version when installing vectorbt
import vectorbt as vbt
import datetime
import plotly
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days = 3 )

#to get multiple tickers

btc_price = vbt.YFData.download(
    ["BTC-USD","ETH-USD"],
    #putting the timeframe, put start and end dates
    interval = "1m",
    start = start_date,
    end = end_date,
    missing_index = "drop").get('Close')


rsi = vbt.RSI.run(btc_price,window=[14,21])
#print(rsi.rsi)
entries = rsi.rsi_crossed_below(30)
exits = rsi.rsi_crossed_above(70)

"""
pf = vbt.Portfolio.from_signals(
    btc_price,
    entries,
    exits,
    #stoploss
    sl_stop = 0.005,
    #tp
    tp_stop = 0.001,
    #enable trailing sl
    sl_trail = True,
     )
"""
pf = vbt.Portfolio.from_signals(
    btc_price,
    entries,
    exits,
    #stoploss
    sl_stop = 0.005,
    
    #enable trailing sl
    sl_trail = True,
    #enters another trade (double the size) once stop or tp is hit, or if you set to 'Close',it will be closed, also look 'CloseReduce
    upon_stop_exit = vbt.portfolio.enums.StopExitMode.Reverse,
     )

#making short trades
pf = vbt.Portfolio.from_signals(
    btc_price,
    short_exits = entries,
    short_entries = exits,
     )

#making both long and short
pf = vbt.Portfolio.from_signals(
    btc_price,
    entries = entries2,
    exits = exits2,
    short_exits = entries,
    short_entries = exits,
     )

fig = pf.plot()
plotly.offline.plot(fig, filename="plotly version of an mpl figure")
