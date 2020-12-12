import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import mpl_finance as mpf
from matplotlib.ticker import Formatter
import numpy as np
import matplotlib.ticker as ticker
ag = pd.read_csv('csv/ochl60.csv')
ochl = pd.DataFrame(ag, columns=['OpenPrice', 'ClosePrice', 'HighPrice', 'LowPrice'])
df = ag.iloc[:, 0:4]
ochl['Time'] = pd.to_datetime(df)
col_name = ['Time', 'OpenPrice', 'HighPrice', 'LowPrice', 'ClosePrice']
ochl = ochl[col_name]

fmt = '%Y%m%d %H'
ochl['Time'] = ochl['Time'].apply(lambda x: dates.date2num(x) * 24)

data_mat = ochl.values[:]


fig, ax = plt.subplots(figsize=(1200 / 36, 480 / 72))
fig.subplots_adjust(bottom=0)
mpf.candlestick_ohlc(ax, data_mat, colordown='green', colorup='r', width=0.5, alpha=1.0)



class MyFormatter(Formatter):
    def __init__(self, dates, fmt='%Y%m%d %H:00'):
        self.dates = dates
        self.fmt = fmt

    def __call__(self, x, pos=0):
        'Return the label for time x at position pos'
        ind = int(np.round(x))
        # ind就是x轴的刻度数值，不是日期的下标

        return dates.num2date(ind / 24).strftime(self.fmt)


formatter = MyFormatter(data_mat[:, 0])

plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
plt.gca().xaxis.set_major_formatter(formatter)

for label in ax.get_xticklabels():
    label.set_rotation(90)
    label.set_horizontalalignment('right')

plt.grid(True)
plt.show()

