import json
import execjs
import pymysql
import requests
from datetime import datetime

# 初始化mysql数据库
def mysql_init():
    conn = pymysql.connect(host='localhost', port=3306,user='root', passwd='123456', autocommit=True)
    cur = conn.cursor()
    sql = 'create database if not exists db'
    cur.execute(sql)
    sql = 'use db'
    cur.execute(sql)
    sql = (
        "create table if not exists xn_database ("
        "id int(11) primary key auto_increment comment '数据编号',"
        "name varchar(255) comment '行业名称',"
        "is_new varchar(10) comment '是否是新兴行业',"
        "is_hot varchar(10) comment '是否是热门行业',"
        "event varchar(255) comment '行业热点事件',"
        "create_time varchar(255) comment '创建时间',"
        "update_time varchar(255) comment '更新时间',"
        "companies varchar(255) comment '行业下公司名称'"
        ")"
    )
    cur.execute(sql)
    return cur

# 持久化操作
def write_to_mysql(cur, data):
    sql = ('insert into xn_database'
           '(name, is_new, is_hot, event, create_time, update_time, companies)'
           'VALUES (%s, %s, %s, %s, %s, %s, %s)')
    for i in data:
        print('写入数据：', i)
        cur.execute(sql, (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "origin": "https://www.xiniudata.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.xiniudata.com/industry/newest?from=data",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
}
url = "https://www.xiniudata.com/api2/service/x_service/person_industry_list/list_industries_by_sort"
with open('烯牛数据.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# 获取数据
def get_data(start):
    n = {
        "payload": {
            "sort": 1,
            "start": start,
            "limit": 20
        }
    }
    lists = execjs.compile(js_code).call('get_list', n)
    payload = lists[0]
    sig = lists[1]
    data = {
        "payload": payload,
        "sig": sig,
        "v": 1
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, data=data)
    d = response.json()['d']
    contents = execjs.compile(js_code).call('get_content', d)
    name_list, is_new_list, is_hot_list, event_list, create_time_list, update_time_list, companies_list = [[] for i in range(7)]
    for i in contents['list']:
        # 行业名称
        name = i['name']
        name_list.append(name)
        # 是否是新兴行业
        is_new = '是' if i['isNew'] else '否'
        is_new_list.append(is_new)
        # 是否是热门行业
        is_hot = '是' if i['isHot'] else '否'
        is_hot_list.append(is_hot)
        # 行业热点事件
        event = i['event']
        event_list.append(event)
        # 创建时间
        create_time = datetime.fromtimestamp(i['createTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        create_time_list.append(create_time)
        # 更新时间
        update_time = datetime.fromtimestamp(i['updateTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        update_time_list.append(update_time)
        j_list = []
        for j in i['companyVOs']:
            j_list.append(j['name'])
        # 行业下公司数量及名称
        companies = '；'.join(j_list)
        companies_list.append(companies)
    return zip(name_list, is_new_list, is_hot_list, event_list, create_time_list, update_time_list, companies_list)

if __name__ == '__main__':
    cur = mysql_init()
    start = 0
    data_num = 0
    data = None
    while True:
        try:
            data = get_data(start)
        except:
            print('暂无数据')
        start += 1
        write_to_mysql(cur, data)
        data_num += 20
        print(f'已写入{data_num}条数据')