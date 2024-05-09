import random #随机分配
from lxml import etree #xpath
import chardet #转化页面文件操作
import requests #爬取页面get操作
from tqdm.asyncio import tqdm #进程可视化操作
import pandas as pd #数据读写
from concurrent.futures import ThreadPoolExecutor, as_completed #线程池操作，多线程

all_urls = []

def url_manage():
    user_agent = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; InfoPath.2; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; 360SE) ",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0) ",
        "Mozilla/5.0 (Windows NT 5.1; zh-CN; rv:1.9.1.3) Gecko/20100101 Firefox/8.0",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; TencentTraveler 4.0; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    ]
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "User-Agent": random.choice(user_agent)
    }
    return headers


def download(new_url):
    response = requests.get(headers=url_manage(), url=new_url)
    response.encoding = chardet.detect(response.content)['encoding']
    response = response.text
    html_text = etree.HTML(response)
    path = '//*[@id="content"]/div[1]/ul/li/a/@href'
    result = html_text.xpath(path)
    for j in result:
        all_urls.append([j, key])


def analysis(new_url, name):
    response = requests.get(headers=url_manage(), url=new_url)
    response.encoding = chardet.detect(response.content)['encoding']
    text = response.text
    path = 'xz'+str(id)+'.csv'
    info_table = pd.DataFrame(
        columns=['总价','单价', '所在区域', '小区名称', '房屋类型', '所在楼层', '建筑面积', '户型结构',
                 '建筑类型', '房屋朝向', '装修情况', '配备电梯'])
    html_text = etree.HTML(text)
    total_load = html_text.xpath('/html/body/div[5]/div[2]/div[2]/div/span[1]/ text()')[0]
    average_load = html_text.xpath('/html/body/div[5]/div[2]/div[2]/div/div[1]/div[1]/span/text()')[0]
    community_name_load = html_text.xpath('/html/body/div[5]/div[2]/div[4]/div[1]/a[1]/ text()')[0]
    house_layout_load = html_text.xpath('/ html / body / div[7] / div[1] / div[1] / div / div / div[1] / div[2] / ul / li[1] / text()')[0]
    floor_load = html_text.xpath('/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[2]/text()')[0]
    floor_space_load = html_text.xpath('/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[3]/text()')[0]
    unit_structure_load = html_text.xpath('/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[4]/text()')[0]
    build_type_load = html_text.xpath('/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[6]/text()')[0]
    house_orientation_load = html_text.xpath('/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[7]/text()')[0]
    renovation_load = html_text.xpath('/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[9]/text()')[0]
    lift_load = html_text.xpath('/html/body/div[7]/div[1]/div[1]/div/div/div[1]/div[2]/ul/li[11]/text()')[0]
    datas = {
        '总价': total_load,'单价':average_load, '所在区域': name, '小区名称': community_name_load, '房屋类型': house_layout_load,
        '所在楼层': floor_load, '建筑面积': floor_space_load,
        '户型结构': unit_structure_load,'建筑类型': build_type_load, '房屋朝向': house_orientation_load,
        '装修情况': renovation_load,'配备电梯': lift_load
    }
    info_table.loc[0]=datas
    info_table.to_csv(path, mode='a+', index=False, header=False, encoding='gb18030')




if __name__ == "__main__":
    url = 'https://xz.lianjia.com/ershoufang/'
    local = {'yunlongqu/': 100, 'gulouqu/': 100, 'quanshanqu/': 100,
             'tongshanqu/': 100, 'jinshanqiaokaifaqu/': 48,
             'xinchengqu3/': 100, 'jiawangqu/': 100,
             'pizhoushi/': 16, 'xinyishi/': 1,
             'suiningxian/': 20, 'peixian/': 15, 'fengxian1/': 100}

    for key, value in local.items():
        print("\n现在下载", key)
        urls = []
        for i in range(1, value + 1):
            new_url = url + key
            if i != 1:
                new_url = new_url + 'pg' + str(i) + '/'
            urls.append(new_url)
        with tqdm(total=len(urls)) as progress_bar:
            with ThreadPoolExecutor(max_workers=20) as executor:
                tasks = [executor.submit(download, i) for i in urls]
                for completed_task in as_completed(tasks):
                    progress_bar.update(1)
    print("正式爬取")
    with tqdm(total=len(all_urls)) as progress_bar:
        with ThreadPoolExecutor(max_workers=20) as executor:
            tasks = [executor.submit(analysis, i[0],i[1]) for i in all_urls]
            for completed_task in as_completed(tasks):
                progress_bar.update(1)