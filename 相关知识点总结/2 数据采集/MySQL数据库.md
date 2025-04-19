## MySQL数据库

### 常用操作

```python
# 读取 json 格式的文件
with open('account.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# 解析字典，获取用户名和密码
username = data['username']
password = data['password']
# 连接数据库，参数如下：host（ip地址（远程或本地）：回环地址：localhost/127.0.0.1），端口号，用户名，密码，自动事务管理
conn = pymysql.connect(host='localhost', port=3306, user=username, password=password, autocommit=True)
# 通过游标执行数据库相关操作
cursor = conn.cursor()
# 创建数据库
cursor.execute('create database if not exists patents')
# 使用数据库
cursor.execute('use patents')
# 创建表（字段相关属性，primary key：主键，auto_increment：自动增长，comment：字段以及表格的描述）
cursor.execute("create table if not exists patents_data ("
               "id int(11) primary key auto_increment comment '编号',"
               "title varchar(255) comment '发明公布名',"
               "publication_id varchar(255) comment '申请公布号',"
               "publication_date varchar(255) comment '申请公布日',"
               "application_id varchar(255) comment '申请号',"
               "application_date varchar(255) comment '申请日',"
               "proposer varchar(255) comment '申请人',"
               "inventor varchar(255) comment '发明人',"
               "address varchar(255) comment '地址',"
               "class varchar(255) comment '分类号',"
               "abstract text comment '摘要'"
               ")")
```

