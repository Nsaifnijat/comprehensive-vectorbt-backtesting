#do look for your python version when installing vectorbt
import vectorbt as vbt
import datetime
import plotly
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days = 3 )

#to get multiple tickers

btc_price = vbt.YFData.download(
    ["BTC-USD"],
    #putting the timeframe, put start and end dates
    interval = "1m",
    start = start_date,
    end = end_date,
    missing_index = "drop").get('Close')


fast_ma = vbt.MA.run(btc_price,window=50)
slow_ma = vbt.MA.run(btc_price, window = 200)
#print(rsi.rsi)
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)
pf = vbt.Portfolio.from_signals(btc_price,entries,exits)

plotly.offline.plot(pf.plot(), filename="plotly version of an mpl figure")

#plot each separately

plotly.offline.plot(pf.trades.plot_pnl(), filename="plotly version of an mpl figure")
plotly.offline.plot(pf.trades.plot(), filename="plotly version of an mpl figure")
plotly.offline.plot(pf.orders.plot(), filename="plotly version of an mpl figure")

#to extract orders and trades data
orders = pf.orders.records_arr

trades = pf.trades.records_arr
