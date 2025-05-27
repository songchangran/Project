### 作业1（正则版）

```python
import re
import csv
import requests

urls = (f'https://movie.douban.com/top250?start={i}&filter=' for i in range(0, 250, 25))

with open('./top250（正则）.csv', 'a', encoding='utf-8', newline='') as f:

    writer = csv.writer(f)
    writer.writerow(['电影名', '主演', '年份', '评分', '评价人数'])

    for url in urls:

        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        }

        response = requests.get(url,headers=headers)

        print(response.status_code)

        data = response.text

        pattern = re.compile(r'<span class="title">(?P<title>.*?)</span>.*?'
                             r'<span class="title">.*?<p>(?P<starts>.*?)<br>.*?'
                             r'(?P<time>.*?)&nbsp.*?'
                             r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
                             r'<span>(?P<pj>.*?)</span>',re.S)

        results = re.finditer(pattern,data)

        for result in results:
            title = result.group('title')
            starts = result.group('starts').strip()
            time = result.group('time').strip() + '年'
            score = result.group('score')
            pj = result.group('pj')
            writer.writerow([title, starts, time, score,pj])
```

运行结果：

![image-20250310115738575](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250310115738575.png)

### 作业1（xpath版）

```python
import requests
import pandas as pd
from lxml import etree

urls = (f'https://movie.douban.com/top250?start={i}&filter=' for i in range(0, 250, 25))

headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}

# 拿到单个页面url
count = 0
for url in urls:
    count += 1
    response = requests.get(url, headers=headers)
    # print(response.text)
    print(response.status_code)

    tree = etree.HTML(response.text)

    # 为数据写入做准备
    movies_dict = {'电影名':[], '导演及主演':[], '评分':[], '评价人数':[]}

    movies = tree.xpath('//div/div[1]/ol')

    for movie in movies:
        titles = movie.xpath('./li/div/div[2]/div/a/span[1]/text()')
        dirs = movie.xpath('./li/div/div[2]/div[2]/p[1]/text()[1]')
        scores = movie.xpath('./li/div/div[2]/div[2]/div/span[2]/text()')
        pjs = movie.xpath('./li/div/div[2]/div[2]/div/span[4]/text()')
        movies_dict['电影名'].extend(titles)
        movies_dict['导演及主演'].extend(dirs)
        movies_dict['评分'].extend(scores)
        movies_dict['评价人数'].extend(pjs)
        # print(len(movies_dict['电影名']))
        # print(len(movies_dict['导演及主演']))
        # print(len(movies_dict['评分']))
        # print(len(movies_dict['评价人数']))
        pd.DataFrame(movies_dict).to_csv('./top250.csv',mode='a')
    print(f'第{count}页爬取完毕')
```

运行结果：

![image-20250310164542940](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250310164542940.png)

![image-20250310164600140](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250310164600140.png)



### 作业2（正则版）

```python
import re
import time
import requests

# 目录界面url
url = 'https://www.najjdd.com/shu/17517/'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}

r = requests.get(url, headers=headers)

# print(r.status_code)
# print(r.text)


# 获取书名
pattern1 = re.compile(r'<div id="info"><a name="top"></a>.*?<h1>(?P<bookname>.*?)</h1>', re.S)

result1 = re.findall(pattern1, r.text)[0]

bookname = result1
# print(bookname)

# 获取章节名

pattern2 = re.compile(r'<dd><a href="//www.najjdd.com/.*?.html">(?P<chapter>.*?)</a></dd>')

result2 = re.finditer(pattern2, r.text)

chapters = []

#将章节名添加到列表里
for result in result2:
    # print(result.group('chapter'))
    chapters.append(result.group('chapter'))

# 在目录界面获取每一张小说的url
pattern_url = re.compile(r' <dd><a href="//(?P<chapters>.*?)">.*?</a></dd>',re.S)

result_url = re.findall(pattern_url, r.text)
# print(result_url)

with open(f'{bookname}.txt', 'a', encoding='utf-8') as f:
    f.write('书名：' + bookname)
    f.write('\n')
    f.write('目录：\n')
    for chapter in chapters:
        f.write(chapter + '\n')


# 在每一张小说里爬取内容
for url in result_url:
    # print(url)
    url = 'https://' + url
    time.sleep(2)
    response2 = requests.get(url, headers=headers)

    # 获取每一章节的源码
    chapter_content = response2.text

    # print(chapter_content)
    title = re.findall(r'<h1>(.*?)</h1>',chapter_content)
    # print(title[0])

    title = title[0]

    content = re.findall(r'<div id="content">(.*?)</div>', chapter_content, re.S)

    content = content[0].strip().replace('<p>','').replace('</p>','\n')

    # print(content)

    # 书名：bookname，章节名chapters（list），章节名title，内容content

    with open(f'{bookname}.txt', 'a', encoding='utf-8') as f:
        f.write(title + '\n')
        f.write(content)
        print(f'{title}爬取完毕，共{len(chapters)}章内容')
```

运行结果：

![image-20250310150408805](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250310150408805.png)

![image-20250310150348911](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250310150348911.png)

### 作业2（xpath版）

```python
from lxml import etree
import requests

url = 'https://www.najjdd.com/shu/17517/'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

tree = etree.HTML(response.text)

# 书名
bookname = tree.xpath('//*[@id="info"]/h1/text()')[0]

# 章节名
chapters = tree.xpath('//*[@id="list"]/dl/dd/a/text()')

with open(f'./{bookname}.txt', 'a', encoding='utf-8') as f:
    f.write(bookname)
    f.write('\n')
    for chapter in chapters:
        f.write(chapter + '\n')

new_urls = tree.xpath('//*[@id="list"]/dl/dd/a/@href')
count = 0
for url in new_urls:
    count += 1
    url = 'https:' + url
    # print(url)
    response = requests.get(url, headers=headers)
    tree = etree.HTML(response.text)
    # 标题
    title = tree.xpath('//*[@id="wrapper"]/div[4]/div/div[2]/h1/text()')[0]
    # 内容
    content = tree.xpath('//*[@id="content"]//text()')
    content = ''.join(content).strip()
    with open(f'./{bookname}.txt', 'a', encoding='utf-8') as f:
        f.write(title)
        f.write('\n')
        f.write(content)
        f.write('\n')
        print(f'第{count}章爬取完毕，共{len(chapters)}章')
```

运行结果：

![image-20250310172610520](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250310172610520.png)

![image-20250310172636845](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250310172636845.png)





### 搜狗关键字抓取

```python
import requests

ipt = input('请输入你要搜索的内容:')

url = 'https://www.sogou.com/web?'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}

params = {
    'query':ipt
}

response = requests.get(url, headers=headers, params=params)

new_url = response.url

print(new_url)

print(response.status_code)

f = open(f'./{ipt}.html','w',encoding='utf-8')

f.write(response.text)

f.close()
```



### xpath

1、XPath 是一门在 XML 文档中查找信息的语言。

| 表达式   | 描述                                                         |
| :------- | :----------------------------------------------------------- |
| nodename | 选取此节点的所有子节点。                                     |
| /        | 从根节点选取（取子节点）。                                   |
| //       | 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置（取子孙节点）。 |
| .        | 选取当前节点。                                               |
| ..       | 选取当前节点的父节点。                                       |
| @        | 选取属性。                                                   |

| 路径表达式      | 结果                                                         |
| :-------------- | :----------------------------------------------------------- |
| bookstore       | 选取所有名为 bookstore 的节点。                              |
| /bookstore      | 选取根元素 bookstore。注释：假如路径起始于正斜杠( / )，则此路径始终代表到某元素的绝对路径！ |
| bookstore/book  | 选取属于 bookstore 的子元素的所有 book 元素。                |
| //book          | 选取所有 book 子元素，而不管它们在文档中的位置。             |
| bookstore//book | 选择属于 bookstore 元素的后代的所有 book 元素，而不管它们位于 bookstore 之下的什么位置。 |
| //@lang         | 选取名为 lang 的所有属性。                                   |

| 路径表达式                          | 结果                                                         |
| :---------------------------------- | :----------------------------------------------------------- |
| /bookstore/book[1]                  | 选取属于 bookstore 子元素的第一个 book 元素。                |
| /bookstore/book[last()]             | 选取属于 bookstore 子元素的最后一个 book 元素。              |
| /bookstore/book[last()-1]           | 选取属于 bookstore 子元素的倒数第二个 book 元素。            |
| /bookstore/book[position()<3]       | 选取最前面的两个属于 bookstore 元素的子元素的 book 元素。    |
| //title[@lang]                      | 选取所有拥有名为 lang 的属性的 title 元素。                  |
| //title[@lang='eng']                | 选取所有 title 元素，且这些元素拥有值为 eng 的 lang 属性。   |
| /bookstore/book[price>35.00]        | 选取 bookstore 元素的所有 book 元素，且其中的 price 元素的值须大于 35.00。 |
| /bookstore/book[price>35.00]//title | 选取 bookstore 元素中的 book 元素的所有 title 元素，且其中的 price 元素的值须大于 35.00。 |

| 通配符 | 描述                 |
| :----- | :------------------- |
| *      | 匹配任何元素节点。   |
| @*     | 匹配任何属性节点。   |
| node() | 匹配任何类型的节点。 |

| 路径表达式   | 结果                              |
| :----------- | :-------------------------------- |
| /bookstore/* | 选取 bookstore 元素的所有子元素。 |
| //*          | 选取文档中的所有元素。            |
| //title[@*]  | 选取所有带有属性的 title 元素。   |

| 路径表达式                       | 结果                                                         |
| :------------------------------- | :----------------------------------------------------------- |
| //book/title \| //book/price     | 选取 book 元素的所有 title 和 price 元素。                   |
| //title \| //price               | 选取文档中的所有 title 和 price 元素。                       |
| /bookstore/book/title \| //price | 选取属于 bookstore 元素的 book 元素的所有 title 元素，以及文档中所有的 price 元素。 |



### Ajax

1、异步的 JavaScript 和 XML

2、在不重新加载整个页面的情况下，可以与服务器交换数据并更新部分网页内容