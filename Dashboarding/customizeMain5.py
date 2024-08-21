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



fig = pf.plot(subplots=
              [
                  ("price", dict(
                      title="Price",
                      yaxis_kwargs = dict(title = "Price"))),
                  
                   ("MovingAvg", dict(
                      title="Price",
                      yaxis_kwargs = dict(title = "Price"))),
                   
                  "orders",
                  "trade_pnl",
                  "cum_returns",
                  "drawdowns"],
                  #add other columns
                  #make_suplots_kwargs=dict(rows=10, cols=2)
              )

 
scatter = vbt.plotting.Scatter(
    data = btc_price,
    x_labels = btc_price.index,
    trace_names = ["Price"],
    add_trace_kwargs = dict(row=1, col=1),
    fig = fig
    )


fast_ma = vbt.plotting.Scatter(
    data = fast_ma.ma,
    x_labels = fast_ma.ma.index,
    trace_names = ["Fast_ma"],
    trace_kwargs = dict(line=dict(color="green")),
    add_trace_kwargs = dict(row=2, col=1),
    fig = fig
    )


slow_ma = vbt.plotting.Scatter(
    data = slow_ma.ma,
    x_labels = slow_ma.ma.index,
    trace_names = ["Slow_am"],
    trace_kwargs = dict(line=dict(color="blue")),
    add_trace_kwargs = dict(row=2, col=1),
    fig = fig
    )

"""
entries = entries.vbt.signals.plot_as_entry_markers(entries, 
                                                add_trace_kwargs = dict(row=2,col=1),
                                                fig=fig)
#exits = exits.vbt.signals.plot_as_exit_markers(exits,
                                             add_trace_kwargs=dict(row=2,col=1),
                                             fig=fig)

fig.add_hline(y=38000,
              line_color="#FFFFFF",
              row=2,
              col=1,
              line_width =20)
"""


plotly.offline.plot(fig, filename="plotly version of an mpl figure")


