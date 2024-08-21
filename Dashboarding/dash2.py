#do look for your python version when installing vectorbt
import vectorbt as vbt
import datetime
import plotly
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days = 3 )

#using themes, types = seaborn, dark, light
vbt.settings.set_theme("seaborn")
vbt.settings['plotting']['layout']['width'] =  800
vbt.settings['plotting']['layout']['height'] =  300


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

fig = btc_price.vbt.plot(trace_kwargs=dict(name="Price",line=dict(color="red")))
fig = fast_ma.ma.vbt.plot(trace_kwargs=dict(name="Fast_ma",line=dict(color="blue")),fig=fig)
fig = slow_ma.ma.vbt.plot(trace_kwargs=dict(name="slow_ma",line=dict(color="green")),fig=fig)
fig = entries.vbt.signals.plot_as_entry_markers(btc_price, fig=fig)
fig = exits.vbt.signals.plot_as_exit_markers(btc_price, fig=fig)



plotly.offline.plot(fig, filename="plotly version of an mpl figure")


