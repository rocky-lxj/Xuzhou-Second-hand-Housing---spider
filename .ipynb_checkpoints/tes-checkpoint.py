import csv
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts.charts import WordCloud
from pyecharts import options as opts
import jieba

plt.rcParams['font.sans-serif']=['FZSongYi-Z13S']
plt.rcParams['font.serif'] = ['FZSongYi-Z13S']
csv_file = pd.read_csv('xz.csv', encoding='gb18030')
#直方图
grouped_data = csv_file.groupby('所在区域')['总价'].mean()
print(grouped_data)
plt.bar(grouped_data.index, grouped_data.values)
plt.xlabel('所在区域')
plt.ylabel('总价的平均值')
plt.title('按区域分组的总价平均值')
plt.show()

#饼图
elevator_counts = csv_file['配备电梯'].value_counts()
elevator_percentage = elevator_counts / len(csv_file) * 100
labels = elevator_percentage.index
sizes = elevator_percentage.values
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.axis('equal')
plt.title('配备电梯的占比')
plt.show()

name = csv_file['小区名称'].unique()
value = csv_file['小区名称'].value_counts()
word = [{'name': i, 'value': value[i]} for i in name]

c = WordCloud()
c.add("", word, word_size_range=[10, 100])
c.set_global_opts(title_opts=opts.TitleOpts(title="二手房小区"))
c.render_notebook()