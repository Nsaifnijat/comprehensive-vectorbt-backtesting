#do look for your python version when installing vectorbt
import vectorbt as vbt
import datetime

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

pf = vbt.Portfolio.from_signals(btc_price,entries,exits)
print(pf.stats())
print(pf.total_return())
print(btc_price)