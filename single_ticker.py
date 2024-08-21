#do look for your python version when installing vectorbt
import vectorbt as vbt
import plotly


btc_price = vbt.YFData.download(
    "BTC-USD",
    missing_index = "drop").get('Close')

rsi = vbt.RSI.run(btc_price,window=14)
#print(rsi.rsi)
entries = rsi.rsi_crossed_below(30)
exits = rsi.rsi_crossed_above(70)

pf = vbt.Portfolio.from_signals(btc_price,entries,exits)
print(pf.stats())
print(pf.total_return())
plotly.offline.plot(pf.plot(), filename="plotly version of an mpl figure")
