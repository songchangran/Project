### 作业1：ciweimao小说爬取

```python
import time
import random
import pymysql
import requests
from lxml import etree

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}
cookies = {
    "Hm_lvt_1dbadbc80ffab52435c688db7b756e3a": "1742955933,1743080623,1743205682",
    "HMACCOUNT": "323003FD651D1131",
    "cwmwapthememip": "white%2C28%2Ctsu-right",
    "Hm_lvt_c1d9813fabdc1c8cc76556965039c251": "1743210479",
    "ci_session": "fedajtpq1b1qj0mf0agaotq8o9g1bj3v",
    "Hm_lpvt_c1d9813fabdc1c8cc76556965039c251": "1743211043",
    "Hm_lpvt_1dbadbc80ffab52435c688db7b756e3a": "1743211114"
}
# 书籍url
url = 'https://www.ciweimao.com/chapter-list/100434189/book_detail'

# 获取章节url,返回书名（str）和章节的url（list）
def get_chapter(url):
    response = requests.get(url, headers=headers)
    html = response.text
    # print(html)
    tree = etree.HTML(html)
    book_name = tree.xpath('//div[@class="hd"]/h3/text()')[0]
    # print(book_name)
    chapter_urls = tree.xpath('//ul[@class="book-chapter-list"]//@href')
    # print(chapter_urls)
    return book_name, chapter_urls

# 获取章节名称（str）和章节内容（）
def get_content(chapter_urls):
    title_content = {}
    for chapter_url in chapter_urls:
        chapter_url = chapter_url.replace('www','mip')
        retry_count = 0
        while retry_count < 100:
            try:
                response = requests.post(url=chapter_url, headers=headers, timeout=10)
                # 如果请求成功，解析并退出循环
                if response.status_code == 200:
                    html = response.text
                    tree = etree.HTML(html)
                    title = tree.xpath('//h1[@class="read-hd"]/text()')[0].replace('\n', '').replace('\t', '')
                    content = "".join(tree.xpath('//div[@class="read-bd"]//text()')).replace('\n', '').replace('\t', '').replace('\u3000', '').replace('IV73P', '\n')
                    # print(title)
                    # print(content)
                    title_content[title] = content
                    print(f"[{title}]爬取成功")
                    break

                # 提示503错误，等待1-3s重试
                elif response.status_code == 503:
                    print(f"503 错误，第{retry_count + 1}次重试...")
                    retry_count += 1
                    time.sleep(random.uniform(1, 3))
                    continue

            except requests.exceptions.RequestException as e:
                print(f"请求异常：{e}，第 {retry_count + 1}次重试...")
                retry_count += 1
                time.sleep(random.uniform(1, 3))
        else:
            print(f"多次尝试仍然失败：{chapter_url}")
    return title_content

            # # new_chapter_url = chapter_url.replace('www','wap')
            # # print(new_chapter_url)
            # response = requests.post(url=chapter_url, headers=headers)
            # # print(response.url)
            # # print(response.text)
            # html = response.text
            # # 返回的json的章节内容是加密的
            # # html = response.json()
            # # print(html)
            # tree = etree.HTML(html)
            # title = tree.xpath('//h1[@class="read-hd"]/text()')[0]
            # print(title)
            # content = tree.xpath('//div[@class="read-bd"]//text()')
            # print(content)

def write_to_mysql(book_name,title_content):
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='123456',charset='utf8',autocommit=True)
    cur = conn.cursor()
    cur.execute('create database if not exists books')
    cur.execute('use books')
    cur.execute(f'create table if not exists book(chapter_id int(11) primary key auto_increment,book_name varchar(20),title varchar(20), content text)  character set utf8mb4')
    try:
        for keys, values in title_content.items():
            cur.execute(f'insert into book (book_name,title,content) values ("{book_name}","{keys}","{values}")')
            print(f"{keys}写入数据库成功")
    except Exception as e:
        print(e)

book_name, chapter_urls = get_chapter(url)
# print(chapter_urls)
# chapter_urls = ['https://mip.ciweimao.com/chapter/113120032']
title_content = get_content(chapter_urls)
write_to_mysql(book_name, title_content)
```

运行结果：

![image-20250329111541157](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250329111541157.png)

![image-20250329111600579](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250329111600579.png)



### Mysql 进阶

```sql
-- 创建数据库
create database 数据库名;
-- 使用数据库
use 数据库名;
-- 创建表
create table 表名(字段1 约束条件1,字段2 约束条件2……) character set 编码格式;
-- 展示表的信息
show tables;
-- 更改表的结构
alter table 表名 change 字段 约束条件;
-- 插入数据
insert into 表名 (字段1,字段2，……)value(字段1,字段2……);
-- 查询数据
select * from 表名;
-- 修改数据
update 表名 set 字段=字段值 where 条件;
-- 删除数据
delete from 表名 where 条件;
```



### mysql 条件语句

|       条件语句（运算符）        |             描述             |
| :-----------------------------: | :--------------------------: |
| =    !=     >    <     >=    <= |        列名 运算符 值        |
|     between 开始  and 结束      | 范围     id between 2 and 4  |
|               in                |  成员运算符    id in (2,4)   |
|        and            &         |            逻辑与            |
|          or        \|           |            逻辑或            |
|          not        !           |            逻辑非            |
|             is null             |       查询结果为空的值       |
|           is not null           |      查询结果不为空的值      |
|            order by             |    排序（从小到大）  desc    |
|              like               | 模糊查询      name like %长% |



```sql
-- 查询语法
-- SELECT 列名1,... from 库名.表名 where 条件

-- 比较运算

-- SELECT * from student where id !=1;
-- SELECT * from student where bday > '1998-01-01';

-- SELECT * FROM student where bday BETWEEN '1998-01-01' and '2000-04-15';   

-- SELECT * FROM student WHERE id in (2,4,6);

-- SELECT * from student WHERE id in (2,4,6) and sex='女';

-- SELECT * FROM student WHERE id in (5,6) or sex='男';

-- SELECT * from student where id not in (2,4);

-- SELECT * FROM student WHERE not sex='女';

-- SELECT * FROM student WHERE bday is NULL;

-- SELECT * FROM student WHERE bday is not NULL;

-- SELECT * FROM student ORDER BY bday;
-- 逆序
-- SELECT * FROM student ORDER BY bday  desc;  


-- SELECT * FROM student WHERE NAME like '%佳%';

-- SELECT * FROM student LIMIT 2,5;
```



### 多表查询

```sql
主键：主关键字
外键：关联两个表
	一对一关联
	一对多关联
	多对多关联
注：1.外键关联必须是其他表的主键
   2.外键数据存储的类型必须和关联的数据类型是一致的
 
 
-- CREATE TABLE student(id INT(10) UNSIGNED not null auto_increment,
-- name VARCHAR(30) NOT NULL,sex enum('男','女')NOT NULL,birthday DATE DEFAULT NULL , PRIMARY KEY (id))ENGINE=INNODB  CHARSET=utf8mb4;

-- INSERT INTO student(id,name,sex,birthday)VALUES('1','中国','男','1949-10-01');
-- INSERT INTO student(name,sex,birthday)VALUES('美国','男','1888-01-01');
-- INSERT INTO student(name,sex,birthday)VALUES('英国','男','1871-11-02');
-- INSERT INTO student(name,sex,birthday)VALUES('小日本','女','1969-05-01');
-- INSERT INTO student(name,sex,birthday)VALUES('俄罗斯','男','1689-10-01');
-- INSERT INTO student(name,sex,birthday)VALUES('印度','男','1866-2-01');
-- INSERT INTO student(name,sex,birthday)VALUES('法国','男',null);
-- 

-- 课程表

-- CREATE TABLE course(id TINYINT UNSIGNED PRIMARY KEY auto_increment,
-- name VARCHAR(25) not NULL)ENGINE=INNODB CHARSET=utf8mb4;


-- INSERT INTO course (id,name)VALUES(1,'python');
-- INSERT INTO course (name)VALUES('python');
-- INSERT INTO course (name)VALUES('python');
-- INSERT INTO course (name)VALUES('python');
-- INSERT INTO course (name)VALUES('python');
-- INSERT INTO course (name)VALUES('python');
-- INSERT INTO course (name)VALUES('python');


-- 成绩表
-- FOREIGN KEY(需要设置外键的字段名称)  references 外键引用哪一张表（那个字段）
-- CREATE table score(id int UNSIGNED PRIMARY KEY auto_increment,
-- sid INT(10) UNSIGNED,cid TINYINT UNSIGNED,grade DECIMAL(5,1),
-- FOREIGN KEY(sid) REFERENCES student(id),FOREIGN KEY(cid) REFERENCES course(id))ENGINE=INNODB CHARSET=utf8mb4;

-- INSERT INTO score(id,sid,cid,grade)VALUES(1,1,1,9999.9);
-- INSERT INTO score(sid,cid,grade)VALUES(2,2,8888.9);
-- INSERT INTO score(sid,cid,grade)VALUES(3,3,7777.9);
-- INSERT INTO score(sid,cid,grade)VALUES(4,4,6666.9);
-- INSERT INTO score(sid,cid,grade)VALUES(5,5,5555.9);
-- INSERT INTO score(sid,cid,grade)VALUES(6,6,4444.9);
-- INSERT INTO score(sid,cid,grade)VALUES(7,7,3333.9);



-- -- 多表查询
-- SELECT sc.id AS '编号',
-- 			 stu.name AS '姓名',
-- 			 co.name AS '课程名称',
-- 			 sc.grade AS '成绩'
-- FROM
-- 			score AS sc,
-- 			course AS co,
-- 			student AS stu
-- WHERE 
-- 			sc.sid = stu.id
-- AND
-- 			sc.cid = co.id;


-- COUNT()
-- SELECT COUNT(*) as '学生人数' from student WHERE sex='男';

-- MAX()
-- SELECT MAX(grade) FROM score;

-- min()
-- SELECT min(grade) FROM score;
-- 
-- -- avg()
-- SELECT AVG(grade) FROM score;
-- 
-- SELECT SUM(grade) FROM score;


-- 分组查询
-- GROUP BY  关键字可以将查询结果按照某个字段或者多个字段进行分组
-- HAVING 条件表达式 ：用于限制分组后的显示，符合条件的结果输出


-- 每个学生的平均分...
-- SELECT sid,avg(grade) FROM score GROUP BY sid;
-- SELECT sid,sum(grade) FROM score GROUP BY sid;

-- -- 每门课程平均分...
-- SELECT cid,AVG(grade) FROM score GROUP BY cid;
-- 
-- 
-- SELECT cid,AVG(grade) FROM score GROUP BY cid HAVING AVG(grade) > 6555;

-- 内连接
-- SELECT * FROM 表1 INNER JOIN 表2 on 表1.字段=表2.字段
-- SELECT * FROM student INNER JOIN score on student.id =score.id;

-- 左连接  将左侧表的所有的数据和右侧表的相关联的数据查询出来，没有关联就返回null

-- SELECT * FROM student LEFT JOIN score ON student.name = score.id;

```
