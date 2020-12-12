import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import mpl_finance as mpf
from matplotlib.ticker import Formatter
import numpy as np
import matplotlib.ticker as ticker

ag = pd.read_csv('csv/ochl.csv')
ochl = pd.DataFrame(ag, columns=['OpenPrice', 'ClosePrice', 'HighPrice', 'LowPrice'])
df = ag.iloc[:, 0:5]
ochl['Time'] = pd.to_datetime(df)
col_name = ['Time', 'OpenPrice', 'HighPrice', 'LowPrice', 'ClosePrice']
ochl = ochl[col_name]

fmt = '%Y%m%d %H:%M'
ochl['Time'] = ochl['Time'].apply(lambda x: dates.date2num(x) * 1440)

#  ========   To attain each time period, select ONE line from behind to run each time  =====================
data_mat = ochl.values[0:181]  # 2020/06/17 20:59 – 2020/06/17 23:59
# data_mat=ochl.values[181:332]   # 2020/06/18 0:00 – 2020/06/18 2:30
# data_mat=ochl.values[332:469]  # 2020/06/18 9:00 – 2020/06/18 11:30
# data_mat=ochl.values[469:560]   # 2020/06/18 13:30 – 2020/06/18 15:00
# ===========================================================================================================


fig, ax = plt.subplots(figsize=(1200 / 36, 480 / 72))

mpf.candlestick_ohlc(ax, data_mat, colordown='green', colorup='r', width=0.6, alpha=1.0)


class MyFormatter(Formatter):
    def __init__(self, dates, fmt='%Y-%m-%d %H:%M'):
        self.dates = dates
        self.fmt = fmt

    def __call__(self, x, pos=0):
        'Return the label for time x at position pos'
        ind = int(np.round(x))
        return dates.num2date(ind / 1440).strftime(self.fmt)


formatter = MyFormatter(data_mat[:, 0])
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.xaxis.set_major_formatter(formatter)

for label in ax.get_xticklabels():
    label.set_rotation(90)
    label.set_horizontalalignment('right')

plt.grid(True)
plt.show()
