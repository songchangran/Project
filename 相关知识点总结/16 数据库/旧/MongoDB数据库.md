### 作业：按照歌手提取歌曲名以及歌词并写入MongoDB

```python
import pymongo
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'referer':'https://music.163.com/'
}
params = {
    'params':'cSagMM0NFBjmu/I0wP8B09U+0jrfiCGJJlQagiCLHUOG1Z7PGBw/YPrpb9CVqyEVUC6tCgcwJ9VPcH6ehwGBCzHH+QaAVqdV0cFxqEbzlgFVkhwyR+cGhgUM0A/ywFXh',
    'encSecKey':'5578425b0f43026338bacf18c1a1e97ce37b7dc8fad099b219a25d43467066305bac3f60fc7f186c92034d89d712458a57bdf56315aa88010482c6ec43bb7c074b5e60e29d9a6f3bc96a1306020076e49647f515ec8afadf7828b5ef6aebb2ed71e41402b0e819778b65549100d8d4330855ada55953fcba5802ddde1e5719c8'
}

# 获取歌手id
def get_gsid():
    url = "https://music.163.com/weapi/artist/top?csrf_token="
    reponse = requests.post(url, headers=headers, params=params)
    # print(reponse.status_code)
    data = reponse.json()
    name_id = {}
    num_id = {}
    for i in data['artists']:
        data_name = i['name']
        data_id = i['id']
        name_id[data_name] = data_id
    count = 0
    for i in name_id.keys():
        count += 1
        num_id[count] = i
        print(count, i)

    num = int(input('请输入歌手序号：'))
    # 拿到歌手id
    id = name_id[num_id[num]]
    return id

# 以列表形式返回歌曲url
def get_song(id):
    # 歌手id页
    gs_url = "https://music.163.com/#/artist?id=%s"%(id)
    # 配置无头浏览器
    options = Options()
    options.add_argument("--headless")  # 无界面模式
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    # 访问歌手页面
    driver.get(gs_url)
    # 切换至iframe（网易云音乐的嵌套结构）
    driver.switch_to.frame("g_iframe")
    # 获取渲染后的完整HTML
    rendered_html = driver.page_source
    # print(rendered_html)
    soup = BeautifulSoup(rendered_html, 'lxml')
    ids = soup.find_all('tr')
    song_urls = []
    for id in ids:
        song_id = "https://music.163.com/#/song?id={id}".format(id=id['id'][0:10])
        # print(song_id)
        song_urls.append(song_id)
    return song_urls
# 将获取到的歌曲名和歌词写入MongoDB
def write_to_database(song_urls):
    for song_url in song_urls:
        # 配置无头浏览器
        options = Options()
        options.add_argument("--headless")  # 无界面模式
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
        # 访问歌手页面
        driver.get(song_url)
        # 切换至iframe（网易云音乐的嵌套结构）
        driver.switch_to.frame("g_iframe")
        # 获取渲染后的完整HTML
        rendered_html = driver.page_source
        # print(rendered_html)
        soup = BeautifulSoup(rendered_html, 'lxml')
        song_name = soup.find('em').text
        song_content = soup.find('div', id='lyric-content').text
        client = pymongo.MongoClient('localhost', 27017)
        db = client.bigdata
        collection = db.songs
        collection.insert_one({'歌曲名': song_name, '歌词': song_content})
        print(f'{song_name}写入完毕')


id = get_gsid()
song_urls = get_song(id)
write_to_database(song_urls)
```

运行结果：

![image-20250317110024191](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250317110024191.png)

![image-20250317110111707](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250317110111707.png)

### MongoDB

- MongoDB的安装与环境配置以及启动MongoDB服务

- Navicat连接MongoDB以及使用MongoDB

- python操作MongoDB

  1. 安装相关模块

     ```python
     pip install pymongo
     ```

  2. 建立连接

     ```python
     client = pymongo.MongoClient(host='127.0.0.1', port=27017)
     
     client = pymongo.MongoClient("mongodb://localhost:27017/")
     ```

  3. 创建库

     ```python
     db = clinet.bigdata
     ```

  4. 创建集合（类似于关系型数据库中的表）

     ```python
     collection = db.students
     ```

  5. 获取数据库

     ```python
     db = client["douban_movies"]
     ```

  6. 增删改查

     ```python
     # 插入操作
     insert_one()
     insert_many()
     
     # 查找操作（可以使用运算符以及正则表达式）
     find()
     
     # 修改操作
     updata()
     
     # 删除操作
     remove()
     delete_one()
     
     # 清空集合
     db.movies.delete_many({})
     ```



MongoDB练习

```python
import pymongo

# 连接数据库
client = pymongo.MongoClient("mongodb://localhost:27017")

# 创建数据库
db = client.bigdata

# 1.创建集合（类似于关系型数据库中的集合）
collection = db.students

# 2.使用“students”集合
collection_students = db["students"]

data1 = {
    "stu_id":1,
    "stu_name":"宋长燃",
    "stu_age":23,
    "stu_gender":"M"
}
data2 = {
    "stu_id":2,
    "stu_name":"长燃",
    "stu_age":30,
    "stu_gender":"F"
}
data3 = {
    "stu_id":3,
    "stu_name":"宋燃",
    "stu_age":20,
    "stu_gender":"M"
}

# 插入单条数据
result_insert1 = collection.insert_one(data1)
print(result_insert1)
# 插入多条数据
result_insert2 = collection.insert_many([data2, data3])
print(result_insert2)

# 查找单条数据
student1 = collection.find_one({"stu_name":"宋长燃"})
print(student1)
# 查找多条数据（可以使用运算符和正则）
student2 = collection.find({"stu_gender":"M"})
for student in student2:
    print(student)
# 查找年龄大于等于23岁的学生
student3 = collection.find({"stu_age":{"$gte":23}})
for student in student3:
    print(student)
# 查找名字中以”燃"结尾的学生
student4 = collection.find({"stu_name":{"$regex":"^.燃$"}})
for student in student4:
    print(student)

# 修改数据（原理是先查找在=再删除），注意更新需要添加更新操作符，否则会替换整个文档
result_update = collection.update_one({"stu_name":"宋长燃"},{"$set":{"stu_name":"宋长燃宋长燃宋长燃"}})
print(result_update)

# 删除单条数据（第一条匹配的文档，所有_one同理）
result_delete1 = collection.delete_one({"stu_id":1})
print(result_delete1)

# 删除多条数据（所有匹配的文档，所有_many同理）
#清空所有文档
result_delete2 = collection.delete_many({})
print(result_delete2)
```

![image-20250317082623135](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250317082623135.png)