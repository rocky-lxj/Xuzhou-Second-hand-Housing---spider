#导包
import pandas as pd
import csv

#向csv文件中添加列属性
filename = 'xz.csv'#路径名称
data = ['总价','单价', '所在区域', '小区名称', '房屋类型', '所在楼层', '建筑面积', '户型结构','建筑类型', '房屋朝向', '装修情况', '配备电梯']
with open(filename, 'r', newline='', encoding='gb18030') as file:
    reader = csv.reader(file)
    rows = list(reader)#收集数据
rows.insert(0, data)
with open(filename, 'w', newline='', encoding='gb18030') as file:
    writer = csv.writer(file)
    writer.writerows(rows)#写入数据
#筛选非法行，若无数据则认定为非法行
csv_file = pd.read_csv('xz.csv', encoding='gb18030')
csv_file.replace('暂无数据', pd.NA, inplace=True)#替换成nan值
csv_file.dropna(how='any', inplace=True)#删除含有nan值的行
csv_file['所在楼层'] = csv_file['所在楼层'].str[:3]#将所在楼层列只保留前三个字符
csv_file['建筑面积'] = csv_file['建筑面积'].str.replace('㎡','')#删除㎡
local = {'yunlongqu/': '云龙区', 'gulouqu/': '鼓楼区', 'quanshanqu/': '泉山区',
             'tongshanqu/': '铜山区', 'jinshanqiaokaifaqu/': '金山桥开发区',
             'xinchengqu3/': '新城区', 'jiawangqu/': '贾汪区',
             'pizhoushi/': '邳州市', 'xinyishi/': '新沂市',
             'suiningxian/': '睢宁县', 'peixian/': '沛县', 'fengxian1/': '丰县'}
#将所在区域变换成文字
for key, value in local.items():
    csv_file.replace(key, value, inplace=True)
csv_file.to_csv('xz.csv', encoding='gb18030')#保存csv
csv_file = pd.read_csv('xz.csv', encoding='gb18030')
csv_file.head()
csv_file.shape
csv_file.describe