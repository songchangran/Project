import time
import pymysql
import redis
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 隧道代理
# # 应用账号（请替换为真实账号）
# app_key = '1227398998999322624'
# # 应用密码（请替换为真实密码）
# app_secret = 'XWWJtL5G'
# # 获取代理IP的接口地址
# api_url = "https://api.xiaoxiangdaili.com/ip/get"
# 请求url
urls = [f'https://bj.lianjia.com/ershoufang/pg{i}/' for i in range(1,101)]
# 伪装请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://bj.lianjia.com/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-Ch-Ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Host": "bj.lianjia.com"
}
# 伪装cookie实现模拟登录
# cookies = {
#     "lianjia_token": "2.0014598fc944a45f2505f4a6f8c00b8f27",
#     "lianjia_token_secure": "2.0014598fc944a45f2505f4a6f8c00b8f27",
#     "security_ticket": "mft6122dgxQkNC2fsy913Va49Qwbdq8LpxDxPbWIjKBUDSsWLKZp2ETIflp7+E0Ld5KGKqWCJNGi33lTVDxJgAGJSNmHGEhIT0UnPFTYNH3GMmKynx/ZOBjuDqWhQU5aII4PLZ1U7+DM9GrK9UMJwRp7GpABSG/A6+0veQOHOy0=",
#     "login_ucid": "2000000442416384",
#     "lianjia_uuid": "03804b99-3cc7-4e3e-b3b4-66436362b1fe",
#     "lianjia_ssid": "1baa1e34-d3a8-4acb-9096-51960ede2739",
#     "select_city": "110000"
# }
cookies = {
    "lianjia_uuid": "8d69198a-1eb0-4469-8d6d-f4b63dca30e2",
    "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%22197d3811eab7eb-0c47761d8d1481-26011e51-1327104-197d3811eac381%22%2C%22%24device_id%22%3A%22197d3811eab7eb-0c47761d8d1481-26011e51-1327104-197d3811eac381%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D",
    "crosSdkDT2019DeviceId": "-775xyi--lq585y-s1jfhar384dmltc-m5s0wncaz",
    "_ga": "GA1.2.688314358.1751600156",
    "ftkrc_": "c15971e7-62a2-4c32-8f11-9134b7e4e2fe",
    "lfrc_": "7058c1ea-8d8c-4bdf-8c6f-9f36a1a9392c",
    "select_city": "110000",
    "lianjia_ssid": "263b8a58-d72c-4a8a-b23a-c0fbde0573a4",
    "Hm_lvt_46bf127ac9b856df503ec2dbf942b67e": "1751600144,1752237789",
    "HMACCOUNT": "B99C3CDDF14602F8",
    "_jzqa": "1.2925928037185358000.1751600144.1751600144.1752237789.2",
    "_jzqc": "1",
    "_jzqckmp": "1",
    "srcid": "eyJ0Ijoie1wiZGF0YVwiOlwiOTdlZjRkNzQ4OGY2ZWY2NWRmZWFmYTkyODQ0NWI2MjMxYjRiODlkZGE4YTM3YzlkMzk1YTcxNmY0MzQ4OWI2NTg3MjFmZmRjYmI0ZDk2ZjEwMWRiOGNiMzAxZTcxMjY2MDY5NWE0ZGQzMzY4ZmFmMjA3ZDQ2NWJiNTIxYjdmZGNjNTJkOWE1ZjE3NmU5ODZlMWQ4MDg1N2M3YzI4ZmVkOGNhYmJiNjYwMDYwNmE5MjdjZmFjMDUzNmY0MjY1Nzg3MmIxYjkzM2U3YTVmYzhlMmVhMzY4ZTM2OWYxZjJhYTI1YTUwZjAwZWJjZDAwYjNlZDM5ZWVlNTNlMDE4MTczMVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJiMDZlMjU3MlwifSIsInIiOiJodHRwczovL2JqLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvcGcxLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9",
    "_qzjc": "1",
    "_gid": "GA1.2.2109017969.1752237800",
    "_gat": "1",
    "_gat_past": "1",
    "_gat_global": "1",
    "_gat_new_global": "1",
    "_gat_dianpu_agent": "1",
    "_ga_KJTRWRHDL1": "GS2.2.s1752237801$o2$g0$t1752237801$j60$l0$h0",
    "_ga_QJN1VP0CMS": "GS2.2.s1752237801$o2$g0$t1752237801$j60$l0$h0",
    "Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e": "1752237806",
    "_qzja": "1.643176291.1751600144552.1751600144552.1752237789660.1752237789660.1752237805982.0.0.0.5.2",
    "_qzjb": "1.1752237789659.2.0.0.0",
    "_qzjto": "2.1.0",
    "_jzqb": "1.2.10.1752237789.1"
}

# 获取代理IP
# def getProxy():
#     res = requests.get(api_url, params={'appKey': app_key, 'appSecret': app_secret, 'wt': 'text', 'cnt': 1})
#     content = str(res.content,'utf-8')
#     # print("API response: " + content)
#     return content

# 使用代理IP去访问目标网站并获取响应
def get_content(url):
    max_retries = 10 # 最大重试次数
    retries = 0
    while retries < max_retries:
        #     p = getProxy()
        #     proxyMeta = "http://%(user)s:%(pass)s@%(proxy)s" % {
        #         "proxy": p,
        #         "user": app_key,
        #         "pass": app_secret,
        #     }
        #     proxies = {
        #         'http': proxyMeta,
        #         'https': proxyMeta,
        #     }
        # print(r.keys())
        h = r.zrevrange('proxies:universal', 0, 0)[0]
        print(h)
        proxies = {
            'http': 'http://' + h,
            'https': 'http://' + h
        }
        print(proxies)
        try:
            response = requests.get(url=url, proxies=proxies, headers=headers, cookies=cookies)
            response.raise_for_status()  # 如果响应状态码不是200，抛出异常
            return response.text
        except Exception as e:
            retries += 1
            print(f"Attempt {retries} failed: {e}")
            time.sleep(3)  # 等待3秒后重新尝试
    print("超过最大重试次数，无法获取内容")

# 解析响应的数据
def get_data(content):
    house_types_list, area_list, orientation_list, decoration_list, floor_levels_list, build_time_list, building_types_list = [[] for _ in range(7)] # 注意一定不要 a = b = c = [], 这样复制是一个对象
    tree = etree.HTML(content)
    # 小区名
    community_names_list = tree.xpath('//div[@class="positionInfo"]/a[1]/text()')
    # print(community_names)
    # 区域
    region_list = tree.xpath('//div[@class="positionInfo"]/a[2]/text()')
    # print(region)
    # 单价（单位：元/平）
    price_list = tree.xpath('//div[@class="unitPrice"]/span/text()')
    # print(total_price)
    # 总价（单位：万元）
    total_price_list = tree.xpath('//div[@class="totalPrice totalPrice2"]/span/text()')
    # print(price)
    houses = tree.xpath('//div[@class="houseInfo"]//text()')
    # print(houses)
    for house in houses:
        house = house.split(' | ')
        # 户型
        house_types = house[0]
        # 面积
        area = house[1]
        # 朝向
        orientation = house[2]
        # 装修
        decoration = house[3]
        # 层数类型及层数
        floor_levels = house[4]
        if len(house) == 6:
            # 建成时间
            build_time = ''
            # 建筑形式
            building_types = house[5]
        else:
            build_time = house[5]
            building_types = house[6]
        house_types_list.append(house_types)
        area_list.append(area)
        orientation_list.append(orientation)
        decoration_list.append(decoration)
        floor_levels_list.append(floor_levels)
        build_time_list.append(build_time)
        building_types_list.append(building_types)
    return community_names_list, region_list, price_list, total_price_list, house_types_list, area_list, orientation_list, decoration_list, floor_levels_list, build_time_list, building_types_list

# 获取记录条数
def get_record_count():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='lj_ershoufang')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM lj_ershoufangdata')
    count = cursor.fetchone()[0]
    conn.close()
    return count

# 向数据库中写入数据
def write_to_mysql(community_names_list, region_list, price_list, total_price_list, house_types_list, area_list, orientation_list, decoration_list, floor_levels_list, build_time_list, building_types_list):
    # 官方建议使用passwors，不建议使用passwd，里面可以指定数据库，还有一个属性autocommit=True（默认False），自动提交事务
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', autocommit=True)
    cursor = conn.cursor()
    cursor.execute('create database if not exists db')
    cursor.execute('use db')
    cursor.execute('create table if not exists lj_ershoufangdata (id int(11) primary key auto_increment, community_names varchar(255), region  varchar(255), price  varchar(255), total_price  varchar(255), house_types varchar(255), area varchar(255), orientation varchar(255), decoration varchar(255), floor_levels varchar(255), build_time varchar(255), building_types varchar(255))')
    for i in zip(community_names_list, region_list, price_list, total_price_list, house_types_list, area_list, orientation_list, decoration_list, floor_levels_list, build_time_list, building_types_list):
        cursor.execute(
            'insert into lj_ershoufangdata (community_names, region, price, total_price, house_types, area, orientation, decoration, floor_levels, build_time, building_types) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[(item,) for item in i])
    # 输出当前记录数和进度
    record_count = get_record_count()
    progress = record_count / 3000 * 100
    print(f'当前数据库记录数: {record_count}，完成度: {progress:.2f}%')

if __name__ == '__main__':
    with ThreadPoolExecutor(5) as executor:
        for url in urls:
            content = executor.submit(get_content, url)
            content = content.result()
            if content:
                future_data = executor.submit(get_data, content)
                community_names_list, region_list, price_list, total_price_list, house_types_list, area_list, orientation_list, decoration_list, floor_levels_list, build_time_list, building_types_list = future_data.result()
                executor.submit(write_to_mysql, community_names_list, region_list, price_list, total_price_list, house_types_list, area_list, orientation_list, decoration_list, floor_levels_list, build_time_list, building_types_list)
    print('执行完毕！')