import csv
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyecharts.charts import WordCloud
from pyecharts import options as opts
plt.rcParams['font.sans-serif']=['FZSongYi-Z13S']
plt.rcParams['font.serif'] = ['FZSongYi-Z13S']
import matplotlib.pyplot as plt
from pyecharts.globals import ThemeType,SymbolType,ChartType
from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode


csv_file = pd.read_csv('xz.csv', encoding='gb18030')

data = csv_file['小区名称'].value_counts()

a = []
b = []
for i in data.index:
    a.append(i)
for j in data.values:
    b.append(j)
c = pd.DataFrame({'一':a,'二':b})
d = c.values

c = WordCloud() # 创建词云
c.add("次数", d, word_size_range=[20, 80])
c.set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-基本示例"))
c.render('小区名称词云.html')