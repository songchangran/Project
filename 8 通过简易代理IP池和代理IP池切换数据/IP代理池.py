import time
import json
import redis
import requests

with open('./url.json', 'r', encoding='utf-8') as f:
    url = json.load(f)['url']
    print(url)

# 连接 Redis 数据库， decode_responses 表示返回的是字符串
r = redis.Redis(host='127.0.0.1', port=6379,db=0,decode_responses=True)

while True:
    if r.llen('my_proxy') < 5:
        source = requests.get(url).text
        ip = source + '|0'
        print(ip)
        r.lpush("my_proxy",ip)
    else:
        time.sleep(2)
        print('代理IP池已经满了')

