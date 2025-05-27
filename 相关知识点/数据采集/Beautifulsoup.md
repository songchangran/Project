### 作业：豆瓣top250

```python
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

urls = ['https://movie.douban.com/top250?start={}&filter='.format(number) for number in range(0, 226, 25)]

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

os.makedirs('./top250/', exist_ok=True)

movie_dict = {}
temp_title, temp_director, temp_time, temp_score, temp_pjnum = [], [], [], [], []
count = 0
for url in urls:
    count += 1
    data = requests.get(url, headers = headers).text

    bs = BeautifulSoup(data, 'lxml')

    movies = bs.select('div .info')

    for movie in movies:
        title = movie.select_one('.title').text
        # print(title)
        director, time = movie.select('.bd p')[0].text.strip().split('\n')
        time = time.strip()[0:5]
        # print(director)
        # print(time)
        score = movie.select_one('.rating_num').text
        # print(score)
        pj_num = movie.select_one('.bd div').text.split('\n')[-2]
        # print
        temp_title.append(title)
        temp_director.append(director)
        temp_time.append(time)
        temp_score.append(score)
        temp_pjnum.append(pj_num)
    print(f'第{count}页爬取完毕，还有{10 - count}页')

movie_dict.update({'电影名：':temp_title, '导演及主演：':temp_director, '上映时间：':temp_time, '评分：':temp_score, '评价人数：':temp_pjnum})
df = pd.DataFrame(movie_dict)

df.to_excel('./top250/top250.xlsx')
```

运行结果：

![image-20250315093520722](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250315093520722.png)

![image-20250315093639346](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250315093639346.png)



### BeautifulSoup

- 安装：pin install bs4

- 解析原理

  - 实例化BeautifulSoup对象，将html源码加载到这个对象中
  - 通过调用bs对象的相关属性或方法进行标签定位、提取数据

- 常用的方法和属性

  - tagname：返回第一次出现的tagname
  - find
    - find('tagname')：等同与tagname
    - find_all()：以列表形式返回文档中的所有tagname标签
  - select选择器
    - select('id、class、trgname'）：以列表的形式返回
    - select('.guji > ul > a')：层级选择器（> 代表一个层级）
    - sellect('.guji a')：层级选择器（空格代表任意层级）
  - 文本提取
    - text：获取当前标签中的所有文本
    - get_text:获取当前标签中的所有文本内容
    - string：只能获取该标签的直系文本内容
  - 属性名提取
    - tagname['属性名']

- 获取元素属性

  link = a_tag['href']

  img_src = img_tag.get('src', '')  # 安全获取属性

- 获取元素内容

​	text_content = div.text          # 包含子元素文本
​	clean_text = div.get_text(strip=True)  # 清理空白字符

- 遍历嵌套元素

​	for li in soup.ul.find_all('li'):
​    	print(li.text)