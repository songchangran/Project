## 作业：拉勾网Python岗位数据采集、分析及预测

### 1 数据采集（Pyppeteer自动化+小象IP代理+PyQuery解析数据）

```python
import asyncio
import pandas as pd
from pyppeteer import launch
from pyquery import PyQuery as pq

def get_proxy_info():
    # 自己的隧道代理信息
    proxy_user = '1229248023675424768'
    proxy_pass = 'nW07aj7M'
    proxy_ip = 'http-dynamic.xiaoxiangdaili.com:10030'

    return proxy_ip, proxy_user, proxy_pass


async def main(proxy_ip, proxy_user, proxy_pass):
    browser = await launch(
        headless=False,
        executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        args=[
            '--no-sandbox',
            '--disable-gpu',
            '--disable-dev-tools',
            '--disable-infobars',
            '--start-maximized'
        ],
        defaultViewport=None
    )
    """
    ,
            f'--proxy-server=http://{proxy_ip}'
    """
    page = await browser.newPage()
    # 设置隧道代理的认证信息
    await page.authenticate({
        'username': proxy_user,
        'password': proxy_pass
    })
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    )
    await page.goto('https://www.lagou.com/wn/zhaopin?fromSearch=true&kd=python&city=%E5%85%A8%E5%9B%BD')
    await page.waitForSelector('[name="account"]')
    await page.type('[name="account"]', '15732471620')
    await page.waitForSelector('[name="password"]')
    await page.type('[name="password"]', '@SCRscr1')
    button = await page.xpath('//*[@id="lg-passport-box"]/div/div[2]/div/div[4]/div[2]/div')
    await button[0].click()
    login = await page.xpath('//*[@id="lg-passport-box"]/div/div[2]/div/div[3]/button')
    await login[0].click()
    # 由于验证码形式会更改，所以这里选择手动打码
    await asyncio.sleep(20)
    # x遮挡了了搜索按钮，手动处理一下
    # x1 = await page.xpath('//*[@id="lg_tbar"]/div[2]/ul/li[4]/div[2]/div/div/div[4]')
    # await x1[0].click()
    # await asyncio.sleep(1)
    # x2 = await page.xpath('//*[@id="lg_tbar"]/div[2]/ul/li[3]/div[2]/div/div/span')
    # await x2[0].click()
    # await asyncio.sleep(1)
    # 搜索岗位
    await page.waitForSelector('#search_input')
    await asyncio.sleep(3)
    await page.type('#search_input', 'python')
    await asyncio.sleep(10)
    await page.waitForSelector('#search_input')
    await page.click('#search_button')
    await asyncio.sleep(20)
    pages = await browser.pages()  # 返回所有打开的标签页
    target_page = pages[2]
    await target_page.bringToFront()
    job_title_list, region_list, salary_range_list, experience_list, education_list, company_list, business_list, finance_list, people_list, description_list = [[] for _ in range(10)]
    recruit_dict = {
        '岗位名': [],
        '岗位位置': [],
        '薪资范围': [],
        '经验要求': [],
        '学历要求': [],
        '公司名': [],
        '主要业务': [],
        '融资情况': [],
        '人员规模': [],
        '岗位描述': []
    }
    j = 0
    old_yz = ''
    while j < 29:
        j += 1
        await asyncio.sleep(3)
        html = await target_page.content()
        doc = pq(html)
        # 获取岗位名和岗位位置
        data1 = doc('#openWinPostion')
        for i in data1.items():
            new_yz = i.text()
            job_title = i.text().split('[')[0]
            region = i.text().split('[')[1].strip(']')
            job_title_list.append(job_title)
            region_list.append(region)
        if new_yz == old_yz:
            print('页面未刷新，重新采集第{}页数据'.format(j-1))
            await target_page.click('.lg-pagination-next')
            j -= 1
            continue
        else:
            print(f'开始采集第{j}页数据')
            old_yz = new_yz

        # 获取薪资范围，经验要求以及学历
        data2 = doc('[class*="p-bom"]')
        for i in data2.items():
            salary_range = i.text().split(' / ')[0].split('经验')[0]
            experience = '经验' + i.text().split(' / ')[0].split('经验')[1]
            education = i.text().split(' / ')[1]
            salary_range_list.append(salary_range)
            experience_list.append(experience)
            education_list.append(education)
        # 获取公司名
        data3 = doc('[class*="company-name"]')
        for i in data3.items():
            company = i.text()
            company_list.append(company)
        # 获取公司主要业务，融资情况以及人员规模
        data4 = doc('[class*="industry__"]')
        for i in data4.items():
            business = i.text().split(' / ')[0]
            financing = i.text().split(' / ')[1]
            people = i.text().split(' / ')[2]
            business_list.append(business)
            finance_list.append(financing)
            people_list.append(people)
        # 获取岗位描述
        data5 = doc('[class*="item-bom__"]')
        for _ in data5.items():
            data6 = _.children().eq(1)
            for i in data6.items():
                description = i.text()
                description_list.append(description)
        # 将每一条完整的数据加入到字典中，为 pandas 写入 csv 文件做准备
        for i in zip(job_title_list, region_list, salary_range_list, experience_list,education_list,company_list,business_list,finance_list,people_list,description_list):
            recruit_dict['岗位名'].append(i[0])
            recruit_dict['岗位位置'].append(i[1])
            recruit_dict['薪资范围'].append(i[2])
            recruit_dict['经验要求'].append(i[3])
            recruit_dict['学历要求'].append(i[4])
            recruit_dict['公司名'].append(i[5])
            recruit_dict['主要业务'].append(i[6])
            recruit_dict['融资情况'].append(i[7])
            recruit_dict['人员规模'].append(i[8])
            recruit_dict['岗位描述'].append(i[9])

        # 翻到下一页
        await target_page.click('.lg-pagination-next')

    await browser.close()
    return recruit_dict


def write_to_csv(recruit_dict):
    df = pd.DataFrame(recruit_dict)
    df.index = df.index + 1
    df.to_csv('招聘数据.csv', mode='a', index_label='编号')

if __name__ == '__main__':
    proxy_ip, proxy_user, proxy_pass = get_proxy_info()
    recruit_dict = asyncio.run(main(proxy_ip, proxy_user, proxy_pass))
    write_to_csv(recruit_dict)
```

运行结果（采集Python岗位共计6363条数据）：

![image-20250415151403074](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250415151403074.png)

### 2 数据分析及可视化（Pandas进行数据处理与分析，re处理数据，scikit-learn进行数据归一化，Matplotlib和Seaborn进行数据可视化）

```python
# 导包
import re
import warnings
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# 加载数据
df = pd.read_csv('./招聘数据.csv')

# 数据预览
print(df.head())

# 数据预处理

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 忽略未来版本警告
warnings.filterwarnings('ignore')

# 提取城市
df['城市'] = df['岗位位置'].str.extract(r'(\w+)')
# print(df['城市'])

# 处理薪资范围，转为月均值（单位k）
def parse_salary(s):
    match = re.findall(r'(\d+)[kK]', s)
    if len(match) == 2:
        return (int(match[0]) + int(match[1])) / 2
    elif len(match) == 1:
        return int(match[0])
    else:
        return None
        
df['平均薪资(k)'] = df['薪资范围'].apply(parse_salary)

# 创建一个 2x4 的子图
fig, axes = plt.subplots(2, 4, figsize=(16, 12))

# 1 城市招聘数量 Top10
top_cities = df['城市'].value_counts().head(10)
sns.barplot(x=top_cities.index, y=top_cities.values, palette='Blues_d', ax=axes[0, 0])
axes[0, 0].set_title('招聘数量最多的城市 Top10')
axes[0, 0].set_ylabel('岗位数量')
axes[0, 0].set_xlabel('城市')

# 2 平均薪资分布
sns.histplot(df['平均薪资(k)'].dropna(), bins=30, kde=True, color='orange', ax=axes[0, 1])
axes[0, 1].set_title('岗位平均薪资分布')
axes[0, 1].set_xlabel('平均薪资 (k/月)')
axes[0, 1].set_ylabel('岗位数量')

# 3 学历要求分布
edu_counts = df['学历要求'].value_counts()
sns.barplot(x=edu_counts.index, y=edu_counts.values, palette='Greens_d', ax=axes[0, 2])
axes[0, 2].set_title('学历要求分布')
axes[0, 2].set_ylabel('岗位数量')
axes[0, 2].set_xlabel('学历')

# 4 经验要求分布
exp_counts = df['经验要求'].value_counts()
sns.barplot(x=exp_counts.index, y=exp_counts.values, palette='Purples', ax=axes[0, 3])
axes[0, 3].set_title('经验要求分布')
axes[0, 3].set_ylabel('岗位数量')
axes[0, 3].set_xlabel('经验要求')
axes[0, 3].tick_params(axis='x', rotation=45)  # 旋转横坐标标签，避免重叠

# 5 融资情况分布
fin_counts = df['融资情况'].value_counts().head(10)
sns.barplot(x=fin_counts.index, y=fin_counts.values, palette='Reds', ax=axes[1, 0])
axes[1, 0].set_title('融资情况分布')
axes[1, 0].set_ylabel('公司数量')
axes[1, 0].set_xlabel('融资情况')
axes[1, 0].tick_params(axis='x', rotation=45)  # 旋转横坐标标签，避免重叠

# 6 公司人员规模分布
size_counts = df['人员规模'].value_counts().head(10)
sns.barplot(x=size_counts.index, y=size_counts.values, palette='coolwarm', ax=axes[1, 1])
axes[1, 1].set_title('公司人员规模分布')
axes[1, 1].set_ylabel('公司数量')
axes[1, 1].set_xlabel('人员规模')

# 7 城市平均薪资 Top10
city_avg_salary = df.groupby('城市')['平均薪资(k)'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=city_avg_salary.index, y=city_avg_salary.values, palette='coolwarm', ax=axes[1, 2])
axes[1, 2].set_title('城市平均薪资 Top10')
axes[1, 2].set_xlabel('城市')
axes[1, 2].set_ylabel('平均薪资 (k/月)')
axes[1, 2].tick_params(axis='x', rotation=45)  # 旋转横坐标标签，避免重叠

# 8 城市综合评分（对Python岗位最友好）
# 经验要求评分
def experience_score(exp):
    if '经验不限' in exp:
        return 1
    elif '1-3年' in exp:
        return 0.8
    elif '3-5年' in exp:
        return 0.6
    elif '5年以上' in exp:
        return 0.4
    else:
        return 0
df['经验要求评分'] = df['经验要求'].apply(experience_score)
# 学历要求评分
def education_score(edu):
    if '本科' in edu:
        return 1
    elif '硕士' in edu:
        return 0.8
    elif '博士' in edu:
        return 0.6
    else:
        return 0
df['学历要求评分'] = df['学历要求'].apply(education_score)
# 公司规模评分
def company_size_score(size):
    if '少于15人' in size:
        return 0.6
    elif '15-50人' in size:
        return 0.8
    elif '50-150人' in size:
        return 1
    elif '150人以上' in size:
        return 0.7
    else:
        return 0
df['公司规模评分'] = df['人员规模'].apply(company_size_score)
# 按城市统计每个城市的相关数据
city_stats = df.groupby('城市').agg(
    岗位数量=('岗位名', 'count'),
    平均薪资=('平均薪资(k)', 'mean'),
    经验要求评分=('经验要求评分', 'mean'),
    学历要求评分=('学历要求评分', 'mean'),
    公司规模评分=('公司规模评分', 'mean')
).reset_index()
# 归一化数据
scaler = MinMaxScaler()
columns_to_normalize = ['岗位数量', '平均薪资', '经验要求评分', '学历要求评分', '公司规模评分']
city_stats[columns_to_normalize] = scaler.fit_transform(city_stats[columns_to_normalize])
# 假设各个维度的权重均等（α = β = γ = δ = 1），可根据需求调整权重
weights = {
    '岗位数量': 1,
    '平均薪资': 1,
    '经验要求评分': 1,
    '学历要求评分': 1,
    '公司规模评分': 1
}
# 计算综合得分
city_stats['综合得分'] = (weights['岗位数量'] * city_stats['岗位数量'] +
                          weights['平均薪资'] * city_stats['平均薪资'] +
                          weights['经验要求评分'] * city_stats['经验要求评分'] +
                          weights['学历要求评分'] * city_stats['学历要求评分'] +
                          weights['公司规模评分'] * city_stats['公司规模评分'])
# 按综合得分排序，得到对 Python 岗位最友好的城市
city_stats_sorted = city_stats.sort_values(by='综合得分', ascending=False)
# 输出排名前几的城市
# print(city_stats_sorted.head())
top_friendly = city_stats_sorted.head(10)
sns.barplot(x=top_friendly['城市'], y=top_friendly['综合得分'], palette='YlGnBu', ax=axes[1, 3])
axes[1, 3].set_title('城市对 Python 友好度 Top10')
axes[1, 3].set_ylabel('综合得分')
axes[1, 3].set_xlabel('城市')
axes[1, 3].tick_params(axis='x', rotation=45)

# 调整布局，确保图表不重叠
plt.tight_layout()

# 显示所有图表
plt.show()
```

运行结果：

![image-20250415153249985](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250415153249985.png)

## 协程

### 协程的定义

- 是一种轻量级的线程，由用户自己控制切换
- 关键点：单线程内通过切换的方式实现高效率



### 协程的Python实现

1. `async def 函数名():`：定义协程函数
2. `await`：表示可以等待的对象
3. 事件循环驱动（自动/手动管理事件循环）



### 协程的实现

```python
import asyncio

# 点餐协程函数
async def order(name):
    print('{}开始点餐'.format(name))
    # 协程挂起，但不会阻塞整个线程，在等待期间，允许事件循环执行其他协程任务，最大化利用 CPU 时间
    await asyncio.sleep(2)
    print(f'{name}点餐结束了')
    return 'order'

# 结账协程函数
async def paying(name):
    print(f'{name}开始结账')
    await asyncio.sleep(2)
    print(f'{name}完成支付了')
    return 'paying'

async def main():
    # 将协程对象转换成 Task 对象，并立即将其加入事件循环的任务队列
    task1 = asyncio.create_task(order('小a'))
    task2 = asyncio.create_task(paying('小b'))
    # 将传入的任务并发启动，并按照传入顺序返回执行结果
    a,b = await asyncio.gather(task1, task2)
    return a, b

if __name__ == '__main__':
    # 启动事件循环并获取返回值进行解包（自动管理事件循环）
    # a, b = asyncio.run(main())
    # print(a, b)

    # 手动管理事件循环
    loop = asyncio.new_event_loop()  # 创建新循环
    asyncio.set_event_loop(loop)  # 设置为当前线程的默认循环
    try:
        # 注意这里需要调用 main() 生成协程对象
        a, b = loop.run_until_complete(main())  # 正确执行协程
        print(a, b)
    finally:
        # 必须关闭循环释放资源
        if not loop.is_closed():
            loop.close()
        asyncio.set_event_loop(None)  # 清理线程状态
```



## PyQuery

### PyQuery的定义

`PyQuery` 是一个基于` Python` 的第三方库，它允许开发者使用类似 `jQuery`的语法来解析和操作 `HTML/XML` 文档。它的核心目标是简化对网页内容的解析和提取。



### PyQuery的安装

- `pip install pyquery`



### PyQuery常见用法示例

```python
# 加载HTML
from pyquery import PyQuery as pq

# 从字符串加载
html = """
<div class="container">
  <h1 id="title">Hello PyQuery</h1>
  <ul class="list">
    <li class="item">Item1</li>
    <li class="item active">Item2</li>
    <li class="item">Item3</li>
  </ul>
</div>
"""
doc = pq(html)  # 创建PyQuery对象

# 从URL加载（自动下载）
# doc = pq(url='https://www.example.com')

# 从文件加载
# doc = pq(filename='demo.html')

# 选择器基础
# 选择所有<li>元素
items = doc('li')  
print(f"找到 {len(items)} 个列表项")

# ID选择器
title = doc('#title')  
print("标题文本:", title.text())

# 类选择器 + 链式调用
active_item = doc('.list').find('.active')  
print("激活项:", active_item.text())

# 层级选择器
second_item = doc('ul > li:nth-child(2)')  
print("第二个项:", second_item.text())

# 属性与内容的操作
# 获取属性
container = doc('.container')
print("容器类名:", container.attr('class'))

# 修改属性
active_item.attr('data-id', '1001')  # 添加/修改属性
print("新属性:", active_item.attr('data-id'))

# 获取HTML内容
print("列表HTML:", doc('ul').html())

# 修改文本内容
title.text('修改后的标题')  
print("新标题:", title.text())

# 遍历与过滤
# 遍历所有列表项
print("\n遍历列表项:")
for li in doc('li').items():  # 注意要使用.items()
    print(f"内容: {li.text()}, 类名: {li.attr('class')}")

# 过滤元素
active_items = doc('li').filter('.active')  
print("\n激活项数量:", len(active_items))

# 查找子元素
ul_element = doc('.container').find('ul')  
print("找到UL元素:", ul_element.html())
```



## Pypperteer

### Pyppeteer的安装

- `pip install pyppeteer2`

  

### Pyppeteer代码示例

```python
# 示例1
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

async def demo():
    # 启动浏览器
    web = await launch(headless=False)
    # 创建页面
    page = await web.newPage()
    # 设置窗口大小
    await page.setViewport({'width': 1920, 'height': 1080})
    # 设置请求头
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36')
    # 向目标网站发起请求
    url = 'https://www.maoyan.com/board'
    await page.goto(url, {'waitUntil': 'domcontentloaded'})
    # 获取网页的HTML源码
    html = await page.content()
    print(html)
    # 让浏览器等待20s
    await asyncio.sleep(2)
    # 关闭浏览器
    await web.close()
if __name__ == '__main__':
    asyncio.run(demo())
    
# 示例2
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

async def main():
    browser = await launch(
        headless=True,
        executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        args=['--no-sandbox', '--disable-gpu']
    )
    page = await browser.newPage()
    await page.goto('https://www.douban.com/doulist/147386000/')
    html = await page.content()
    # print(html)
    doc = pq(html)
    divs = doc('.doulist-item')
    for div in divs.items():
        numbers = div.find('.pos').text()
        name = div.find('.title').text()
        print(numbers, name)
    await asyncio.sleep(10)
    await browser.close()

asyncio.run(main())
```



### Pyppeteer模拟登录

```python
import asyncio
from pyppeteer import launch
async def login(url,username,password):
    web = await launch(headless=False, args=['--disable-blinkfeatures=AutomationControlled','--start-maximized'])
    page = await web.newPage()
    await page.setViewport({'width':1920,'height':1080})
    try:
        await page.goto(url)
        #定位用户名的输入框
        username_input_xpath = '//*[@id="app"]/div[1]/div[2]/div/div[1]/div/div[2]/div[3]/form/div[1]/div/div/input'
        username_input = await page.waitForXPath(username_input_xpath)
        await username_input.type(username)
        # 定位密码的输入框
        password_input = await page.waitForXPath('//*[@id="app"]/div[1]/div[2]/div/div[1]/div/div[2]/div[3]/form/div[2]/div/div/input')
        await password_input.type(password)
        # 定位勾选框
        await page.click('#app > div.login > div.escrool > div > div.elscrollbar__wrap > div > div.source_space > div.ri > form > div.agreement > label> span > span')
        await page.click('#app > div.login > div.escrool > div > div.elscrollbar__wrap > div > div.source_space > div.ri > form > div.login')
        await asyncio.sleep(30)
    finally:
        await web.close()

async def main():
    url = 'https://sso.icve.com.cn/sso/auth?'
    mode='simple&redirect=https%3A%2F%2Fzjy2.icve.com.cn%2Fadmin%2Fpedding&source=15'
    uesrname = '20205076'
    password = 'xxxxxx'
    await login(url,uesrname,password)
        
asyncio.run(main())
```



### Pyppeteer使用ip代理

```python
import asyncio

import requests
from pyppeteer import launch

# 用户名密码认证(私密代理/独享代理)
app_key = 'app_key'
app_secret = 'app_secret'
# 提取代理API接口，获取1个代理IP
api_url = "https://api.xiaoxiangdaili.com/ip/get" + "?appKey=" + app_key + "&appSecret=" + app_secret + "&cnt=1&wt=text"
# 获取API接口返回的代理IP
proxy_ip = requests.get(api_url).text
proxy = "http://" + proxy_ip


def accounts():
    account = {"username": app_key, "password": app_secret}
    return account


async def main():
    # 要访问的目标网页
    target_url = "http://httpbin.org/ip"

    browser = await launch({'headless': False, 'args': ['--disable-infobars', '--proxy-server=' + proxy]})
    page = await browser.newPage()
    # await page.authenticate(accounts())  # 白名单方式，注释本行（需提前设置白名单）
    await page.setViewport({'width': 1920, 'height': 1080})
    # 使用代理IP发送请求
    await page.goto(target_url)
    await asyncio.sleep(209)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
```



### Pyppeteer和selenium的区别

- 底层协议不同：`Pyppeteer`使用`chromdevtools`协议（无需通过中间代理，速度恒快），`selenium`使用`webdreiver`协议（首先与浏览器驱动通信，再由驱动控制浏览器，多了一层中转）

- 内存占用：`Pyppeteer`更低，`Selenium`更改

- 支持的语言：`Pyppeteer`只支持`python` ；`selenium`支持`java c# js php`等等

- 异步支持：基于`asyncio`;`selneium `需要配合多线程以及第三方库实现异步
- 反爬绕过e能力：`Pyppeteer`更强(可以隐藏自动化特征) ；`selenium 较弱`（`webdriver`很容易被检测）











