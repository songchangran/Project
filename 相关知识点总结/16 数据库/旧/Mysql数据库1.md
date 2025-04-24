### 作业1：爬取刺猬猫并写入MySQL数据库

```python
import time
import pymysql
import requests
from lxml import etree
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

# 获取该书的书名和章节URL，返回bookname和章节URL
def get_chapters(book_url):
    response = requests.get(book_url, headers=headers)
    # print(response.status_code)
    tree = etree.HTML(response.text)
    book_name = tree.xpath('/html/body/div[5]/div/div[2]/div[1]/div/div[1]/h3/text()')[0]
    ul = tree.xpath('/html/body/div[5]/div/div[2]/div[1]/div/div[2]/div/div/ul')
    chapter_urls = []
    for li in ul:
        chapter_url = li.xpath('./li/a/@href')
        # 从他开始包括它是付费章节 112585364
        for i in chapter_url:
            if i == 'https://www.ciweimao.com/chapter/112590091':
                break
            chapter_urls.append(i)
        # print(chapter_urls)
    return book_name,chapter_urls

# 获取章节URL里面的标题和内容，返回title和content
def get_content(chapter_urls):
    title_content = {}
    for chapter_url in chapter_urls:
        driver = webdriver.Chrome()
        driver.get(chapter_url)
        # print(driver.page_source)
        tree = etree.HTML(driver.page_source)
        title = tree.xpath('//div[@class="read-hd"]/h1/text()')[0]
        # print(title)

        old_content = tree.xpath('//div[@class="read-bd"]/p/text()')
        old_content = ''.join(old_content).split('\u3000')
        new_content = ''
        for i in old_content:
            new_content += i + '\n'
        # print(new_content.strip().replace('\n\n','\n'))
        content = new_content.strip().replace('\n\n','\n')
        time.sleep(2)
        # print(title,content)
        title_content.update({title:content})
        print(f'[{title}]爬取完毕')
    # print(title_content)
    return title_content

# 将爬取到的数据写入MySQL数据库
def write_to_mysql(book_name,title_content):
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='123456',charset='utf8',autocommit=True)
    cur = conn.cursor()
    cur.execute('create database if not exists books')
    cur.execute('use books')
    cur.execute(f'create table if not exists book(book_id int(11) primary key auto_increment,book_name varchar(20),title varchar(20), content text)')
    try:
        for keys, values in title_content.items():
            cur.execute(f'insert into book (book_name,title,content) values ("{book_name}","{keys}","{values}")')
    except Exception as e:
        print(e)

book_url = 'https://www.ciweimao.com/chapter-list/100426105/book_detail'
book_name,chapter_urls = get_chapters(book_url)
# print(chapter_urls)
title_content = get_content(chapter_urls)
write_to_mysql(book_name,title_content)
```

**运行结果**

![image-20250326162546612](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250326162546612.png)

![image-20250326162559113](C:\Users\31923\AppData\Roaming\Typora\typora-user-images\image-20250326162559113.png)



### 数据库按数据模型分类

- 关系型数据库（RDBMS）：例如MySQL，SQL Server
- 非关系型数据库（NoSQL）：例如MongoDB，Redis



### 数据库的四个基本概念

- 数据：是数据库中存储的基本单位，是描述事物的符号记录（例如某个学生的学号，姓名等信息）
- 数据库：是存储数据的集合
- 数据库管理系统：用于管理数据库的软件
- 数据库系统：由 **数据库（DB）+ 数据库管理系统（DBMS）+ 硬件 + 软件 + 用户** 组成的完整系统。



### 理解MySQL数据库

- 库中存放表，表中存放数据
- 库可以有多个表，表中有唯一的标识
- 表由列组成，数据按行存储



### MySQL数据库数据

|                             术语                             |                      描述                      |
| :----------------------------------------------------------: | :--------------------------------------------: |
|                   Row（行）/Record（记录）                   |                 表中的一条数据                 |
|                  Column（列）/Field（字段）                  |                 表的属性/字段                  |
|                         View（视图）                         |    基于查询结果创建的虚拟表，不存储实际数据    |
| xxxxxxxxxx 主键：主关键字外键：关联两个表    一对一关联    一对多关联    多对多关联注：1.外键关联必须是其他表的主键   2.外键数据存储的类型必须和关联的数据类型是一致的  -- CREATE TABLE student(id INT(10) UNSIGNED not null auto_increment,-- name VARCHAR(30) NOT NULL,sex enum('男','女')NOT NULL,birthday DATE DEFAULT NULL , PRIMARY KEY (id))ENGINE=INNODB  CHARSET=utf8mb4;​-- INSERT INTO student(id,name,sex,birthday)VALUES('1','中国','男','1949-10-01');-- INSERT INTO student(name,sex,birthday)VALUES('美国','男','1888-01-01');-- INSERT INTO student(name,sex,birthday)VALUES('英国','男','1871-11-02');-- INSERT INTO student(name,sex,birthday)VALUES('小日本','女','1969-05-01');-- INSERT INTO student(name,sex,birthday)VALUES('俄罗斯','男','1689-10-01');-- INSERT INTO student(name,sex,birthday)VALUES('印度','男','1866-2-01');-- INSERT INTO student(name,sex,birthday)VALUES('法国','男',null);-- ​-- 课程表​-- CREATE TABLE course(id TINYINT UNSIGNED PRIMARY KEY auto_increment,-- name VARCHAR(25) not NULL)ENGINE=INNODB CHARSET=utf8mb4;​​-- INSERT INTO course (id,name)VALUES(1,'python');-- INSERT INTO course (name)VALUES('python');-- INSERT INTO course (name)VALUES('python');-- INSERT INTO course (name)VALUES('python');-- INSERT INTO course (name)VALUES('python');-- INSERT INTO course (name)VALUES('python');-- INSERT INTO course (name)VALUES('python');​​-- 成绩表-- FOREIGN KEY(需要设置外键的字段名称)  references 外键引用哪一张表（那个字段）-- CREATE table score(id int UNSIGNED PRIMARY KEY auto_increment,-- sid INT(10) UNSIGNED,cid TINYINT UNSIGNED,grade DECIMAL(5,1),-- FOREIGN KEY(sid) REFERENCES student(id),FOREIGN KEY(cid) REFERENCES course(id))ENGINE=INNODB CHARSET=utf8mb4;​-- INSERT INTO score(id,sid,cid,grade)VALUES(1,1,1,9999.9);-- INSERT INTO score(sid,cid,grade)VALUES(2,2,8888.9);-- INSERT INTO score(sid,cid,grade)VALUES(3,3,7777.9);-- INSERT INTO score(sid,cid,grade)VALUES(4,4,6666.9);-- INSERT INTO score(sid,cid,grade)VALUES(5,5,5555.9);-- INSERT INTO score(sid,cid,grade)VALUES(6,6,4444.9);-- INSERT INTO score(sid,cid,grade)VALUES(7,7,3333.9);​​​-- -- 多表查询-- SELECT sc.id AS '编号',--           stu.name AS '姓名',--           co.name AS '课程名称',--           sc.grade AS '成绩'-- FROM--          score AS sc,--          course AS co,--          student AS stu-- WHERE --          sc.sid = stu.id-- AND--          sc.cid = co.id;​​-- COUNT()-- SELECT COUNT(*) as '学生人数' from student WHERE sex='男';​-- MAX()-- SELECT MAX(grade) FROM score;​-- min()-- SELECT min(grade) FROM score;-- -- -- avg()-- SELECT AVG(grade) FROM score;-- -- SELECT SUM(grade) FROM score;​​-- 分组查询-- GROUP BY  关键字可以将查询结果按照某个字段或者多个字段进行分组-- HAVING 条件表达式 ：用于限制分组后的显示，符合条件的结果输出​​-- 每个学生的平均分...-- SELECT sid,avg(grade) FROM score GROUP BY sid;-- SELECT sid,sum(grade) FROM score GROUP BY sid;​-- -- 每门课程平均分...-- SELECT cid,AVG(grade) FROM score GROUP BY cid;-- -- -- SELECT cid,AVG(grade) FROM score GROUP BY cid HAVING AVG(grade) > 6555;​-- 内连接-- SELECT * FROM 表1 INNER JOIN 表2 on 表1.字段=表2.字段-- SELECT * FROM student INNER JOIN score on student.id =score.id;​-- 左连接  将左侧表的所有的数据和右侧表的相关联的数据查询出来，没有关联就返回null​-- SELECT * FROM student LEFT JOIN score ON student.name = score.id;​sql | 唯一标识表中每一行数据的字段（唯一的、非空的） |
|                     Foregin Key（外键）                      |        连接两张表的字段，保证数据一致性        |
|                      Unique（唯一约束）                      |                  确保字段唯一                  |
|                     Not Null（非空约束）                     |                限制字段不能为空                |
|                      Default（默认值）                       |                为字段提供默认值                |
|                    DDL（数据库定义语言）                     | 定义数据库结构，例如create table，alter table  |
|                    DML（数据库操作语言）                     |      操作数据，例如insert，delete，update      |
|                    DQL（数据库查询语言）                     |              查询数据，例如select              |
|                     DCL（权限控制语言）                      |          权限管理，例如grant，revoke           |
|                     TCL（事务控制语言）                      |         事务管理，例如commit，rollback         |
|                        Cursor（游标）                        |             逐行处理查询结果的机制             |
|                     Transaction（事务）                      |        保证数据操作的完整性（ACID原则）        |



### 相关操作

- DDL

  - create table：创建数据表
  - alter table：修改表结构
  - drop table：删除表
  - create index：创建索引
  - drop index：删除索引

- DML

  - insert：添加/插入数据
  - delete：删除数据
  - update：修改数据

- DQL

  - select：查询数据

- DCL

  - grant：授予访问权限
  - revoke：撤销访问权限

- TCL

  - commit：提交事务

  - rollback：回滚事务
  - savepoint：设置保存点
  - lock：对数据的特定部分进行锁定



### 数据类型

- 数值

  - 整型

    |   类型   | 长度（字节） |
    | :------: | :----------: |
    | tinyint  |      1       |
    | smallint |      2       |
    | mediuint |      3       |
    |   int    |      4       |
    |  bigint  |      8       |

  - 浮点型

    |  类型   | 长度（字节） |
    | :-----: | :----------: |
    |  float  |      4       |
    | double  |      8       |
    | decimal |     变长     |

    

- 字符串

  |             类型              |         长度          |
  | :---------------------------: | :-------------------: |
  | char(n)（适用于固定长度数据） | 固定长度（n表示长度） |
  | varchar（适用于可变长度文本） |         变长          |
  |     text（适用于大文本）      |         变长          |
  | blob（适用于存储二进制数据）  |         变长          |
  |    enum（适用于有限选项）     |          1~2          |
  |     set（适用于多选字段）     |          1~8          |

  

- 日期

  |                             类型                             | 长度 |        格式         |
  | :----------------------------------------------------------: | :--: | :-----------------: |
  |                    date（适用于存储日期）                    |  3   |     YYYY-MM-DD      |
  |               datetime（适用于精确到秒的时间）               |  8   | YYYY-MM-DD HH:mm:ss |
  | timestamp（适用于存储系统日志、记录创建时间、修改时间等，受时区影响） |  4   | YYYY-MM-DD HH:mm:ss |
  |                  time（适用于存储时间间隔）                  |  3   |      HH:mm:ss       |
  |                    year（适用于存储年份）                    |  1   |        YYYY         |



### 数据库的常用操作

|                             格式                             |         描述         |
| :----------------------------------------------------------: | :------------------: |
|                      mysql -u 用户名 -p                      |      登录数据库      |
|                        show databases                        | 查询已有的数据库列表 |
| create database 数据库名 库选项（create database students charset utf8）（注意utf8） |      创建数据库      |
| alter database 数据库名 库选项（alter database stu charset gbk） |      修改数据库      |
| drop database if exists 数据库名 （drop database if exists stu） |      删除数据库      |
|                    use database 数据库名                     |      指定数据库      |

PS：修改数据库名只能手动迁移数据，还有注意分号的使用



### 数据库表的常用操作

|                             格式                             |    描述    |
| :----------------------------------------------------------: | :--------: |
| create table 表名（字段1 数据类型 约束条件，……）<br />（create table student(stu_id primary key auto_increment,stu_name varchar(10),score int(11))） |   创建表   |
|                          desc 表名                           | 查看表结构 |
|                    show columns from 表名                    | 查看表结构 |
| alter table 表名 add column 字段名称 数据类型（长度） 约束条件 |  添加字段  |
| alter table 表名 change 原始名称 新名称 数据类型（长度） 约束条件 |  修改字段  |
|                alter table 表名 drop 字段名称                |  删除字段  |
|          insert into 表名(字段1，……) value(值1，……)          |  插入数据  |
|               delete from 表名 （where 条件）                |  删除数据  |
|       updata 表名 SET 字段1 = 值1 （where 字段2=值2）        |  修改数据  |
|              select * from 表名 （where 条件）               |  查询数据  |
|                       drop table 表名                        |   删除表   |
|                         show tables                          | 查看所有表 |

ps：注意分号的使用，exit；退出数据库



### Python操作MySQL

```python
# 安装mypython：pip install pymysql

# 导入模块
import pymysql

# 连接数据库
# 官方建议使用passwors，不建议使用passwd，里面可以指定数据库，还有一个属性autocommit=True（默认False），自动提交事务
conn = pymysql.connect(host='localhost', port=3306, user='root',password='123456',autocommit=True)

# 通过游标操作数据库（游标是数据库连接和数据库之间的中介）
cur = conn.cursor()
cur.execute('create database if not exists stu')
cur.execute('use stu')
create_students = 'create table if not exists students (stu_id int(11) primary key auto_increment,stu_name varchar(255),score float)'
cur.execute(create_students)
cur.execute('insert into students (stu_name,score) values ("scr",100)')
"""
    fetchall()：获取所有结果，返回一个包含所有结果的列表，每一行是一个元组。
    fetchone()：获取查询结果的第一行，返回一个元组。如果没有更多结果，则返回 None。
    fetchmany(n)：获取指定数量的结果，返回一个包含前 n 行的列表，每一行是一个元组。
"""
cur.execute('select * from students')
results = cur.fetchall()
for i in results:
    print(i)
```

