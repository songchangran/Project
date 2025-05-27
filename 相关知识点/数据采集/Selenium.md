## Selenium

作业1：使用Selenium自动化抓取猫眼票房数据并存储到数据库中

```python
import time
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# 采集数据
def get_data(url):
    # 伪装 Selenium
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled") # 隐藏 webdriver 特征
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    # 用来暂时存放数据
    titles, phs, zhpfs, pfzbs, ppccs, ppzbs, cjrcs, szls = [], [], [], [], [], [], [], []

    web = webdriver.Chrome(options=options)
    web.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  # 进一步隐藏
    web.get(url=url)
    # print(web.page_source)
    # 电影标题
    title = web.find_elements(By.XPATH, '//p[@class="moviename-name"]')
    for i in title:
        # print(i.text)
        titles.append(i.text)
    # 票房排行
    ph = web.find_elements(By.XPATH, '//p[@class="moviename-index"]')
    for i in ph:
        # print(i.text)
        phs.append(i.text)
    # 综合票房
    zhpf = web.find_elements(By.XPATH, '//div[@class="mtsi-num-pos"]')
    for i in zhpf:
        # print(i.text)
        zhpfs.append(i.text)
    # 其他字段
    movies = web.find_elements(By.XPATH, '//tr')
    for i in movies:
        # 票房占比
        pfzb = i.find_elements(By.XPATH, './td[3]')
        for j in pfzb:
            # print(j.text)
            pfzbs.append(j.text)
        # 排片场次
        ppcc = i.find_elements(By.XPATH, './td[4]')
        for j in ppcc:
            # print(j.text)
            ppccs.append(j.text)
        # 排片占比
        ppzb = i.find_elements(By.XPATH, './td[5]')
        for j in ppzb:
            # print(j.text)
            ppzbs.append(j.text)
        # 场均人次
        cjrc = i.find_elements(By.XPATH, './td[6]')
        for j in cjrc:
            # print(j.text)
            cjrcs.append(j.text)
        # 上座率
        szl = i.find_elements(By.XPATH, './td[7]')
        for j in szl:
            # print(j.text)
            szls.append(j.text)
    time.sleep(5)
    web.quit()
    return titles, phs, zhpfs, pfzbs, ppccs, ppzbs, cjrcs, szls

# 写入数据到MySQL数据库中
def write_to_mysql(titles, phs, zhpfs, pfzbs, ppccs, ppzbs, cjrcs, szls):
    # 官方建议使用passwors，不建议使用passwd，里面可以指定数据库，还有一个属性autocommit=True（默认False），自动提交事务
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', autocommit=True)
    cursor = conn.cursor()
    cursor.execute('create database if not exists maoyanpiaofang')
    cursor.execute('use maoyanpiaofang')
    cursor.execute('create table if not exists maoyanpiaofangdata (title varchar(255), '
                   'ph int(11) primary key, zhpf varchar(255), pfzb varchar(255), '
                   'ppcc varchar(255), ppzb varchar(255), cjrc varchar(255), szls varchar(255))')
    j = 0
    for i in zip(titles, phs, zhpfs, pfzbs, ppccs, ppzbs, cjrcs, szls):
        # print(i)
        cursor.execute('insert into maoyanpiaofangdata (title, ph, zhpf, pfzb, ppcc, ppzb, cjrc, szl) values (?,?,?,?,?,?,?,?)', [(item,) for item in i])
        print(f'{titles[j]}写入数据库成功！')
        j += 1


url = 'https://piaofang.maoyan.com/dashboard/movie'
titles, phs, zhpfs, pfzbs, ppccs, ppzbs, cjrcs, szls = get_data(url)
write_to_mysql(titles, phs, zhpfs, pfzbs, ppccs, ppzbs, cjrcs, szls)
```



### Selenium是什么

Selenium 是一个用于 **自动化 Web 应用测试** 的开源工具，支持多种编程语言（如 Python、Java、C# 等）和浏览器（如 Chrome、Firefox、Edge 等）。它主要用于 **模拟用户操作**，比如点击按钮、填写表单、滚动页面等。



### **Selenium 的核心组件**：

1. **Selenium WebDriver**：
   - 提供 API 来与不同浏览器交互，模拟用户操作。
   - 适用于 Web 自动化测试，也可用于 Web 爬虫。
2. **Selenium IDE**（集成开发环境）：
   - 是一个浏览器扩展，可以录制和回放用户操作，无需编程。
3. **Selenium Grid**：
   - 用于 **分布式测试**，可以在多个设备或浏览器上并行运行测试。



### **Selenium 的常见应用**：

- **自动化测试**：可以用于功能测试、回归测试等，提高测试效率。
- **Web 爬虫**：用于爬取网页数据，代替 `requests` 处理动态加载的页面。
- **RPA（机器人流程自动化）**：模拟用户操作网页，提高办公自动化水平。



### Python使用Selenium的流程

1. 安装模块：pip install selenium
2. 查看当前浏览器版本，根据浏览器版本下载并安装浏览器驱动（将浏览器驱动放在Python解释器的同级目录里）
3. ps：在 Selenium 4.6.0 及以上版本，**不需要手动导入浏览器驱动**，可以直接使用 `webdriver.Chrome()`，Selenium 会自动管理驱动。



### Python使用Selenium的常用操作

```python
# 导入谷歌浏览器的类
from selenium.webdriver import Chrome
# 创建浏览器对象
web = Chrome()
# 向url发送请求
web.get(url)
# 最大化窗口
web.maximize_window()
# 关闭浏览器
web.quit()
# 找到百度输入框并输入4399（可以在这里直接输入回车）
web.find_element_by_xpath('//*[@id="kw"]').send_keys('4399')
# 找到百度一下按钮，通过click()点击事件点击
el1 = web.find_element_by_xpath('//*[@id="su"]').click()
# 获取当前页面源码
web.page_source
# 窗口的切换
web.switch_to.window(web.window_handles[1])
```



### 无头模式

```python
from selenium.webdriver import Chrome
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
opt = Options()
opt.add_argument('--headless') # 关闭窗口
opt.add_argument('--disable-gup') # 禁止显卡使用
web = Chrome(options=opt) # 将参数都加到浏览器中
```

示例

```python
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
opt = Options()
# opt.add_argument('--headless') # 关闭窗口
# opt.add_argument('--disable-gup') # 禁止显卡使用
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
opt.add_argument(f'user-agent={user_agent}')
# window.navigator.webdriver 改为false
opt.add_argument('--disable-blink-features=AutomationControlled')
# 关闭谷歌正受到自动化...控制
opt.add_experimental_option('excludeSwitches',['enable-automation'])
web = Chrome(options=opt) # 将参数都加到浏览器中
web.get('https://www.baidu.com')
```





















