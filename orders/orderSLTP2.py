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


#making both long and short
pf = vbt.Portfolio.from_signals(
    btc_price,
    entries = entries2,
    exits = exits2,
    short_exits = entries,
    short_entries = exits,
    #when both signals happen on the same candle, which one to choose, we choose short and ignore long
    upon_dir_conflict = vbt.portfolio.enums.DirectionConflictMode.Short,
     )

fig = pf.plot()
plotly.offline.plot(fig, filename="plotly version of an mpl figure")
# -*- coding: utf-8 -*-

