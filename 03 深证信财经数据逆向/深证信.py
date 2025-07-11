import pymysql
import requests
import execjs
from datetime import datetime, timedelta

def get_args():
    with open('深证信.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    accept_encKey = execjs.compile(js_code).call('getResCode')
    # print(accept_encKey)
    headers = {
        "Accept": "*/*",
        "Accept-EncKey": accept_encKey,
        "Accept-Language": "zh,en;q=0.9,zh-CN;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://webapi.cninfo.com.cn",
        "Referer": "https://webapi.cninfo.com.cn/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = "https://webapi.cninfo.com.cn/api/sysapi/p_sysapi1007"
    return url, headers

def get_data(start_date, end_date):
    start_time = datetime.strptime(start_date, '%Y-%m-%d')
    end_time = datetime.strptime(end_date, '%Y-%m-%d')
    while start_time <= end_time:
        data = {
            "tdate": start_time.strftime('%Y-%m-%d'),
            "market": "SZE"
        }
        yield data
        start_time += timedelta(days=1)

def init_mysql():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', autocommit=True)
    cur = conn.cursor()
    cur.execute('create database if not exists db')
    cur.execute('use db')
    cur.execute('create table if not exists szx_database('
                'id int primary key auto_increment comment "数据编号",'
                'trade_date varchar(20) comment "交易日期",'
                'exchange varchar(20) comment "交易所",'
                'stock_name varchar(50) comment "证券简称",'
                'stock_code varchar(20) comment "证券代码",'
                'currency varchar(10) comment "币种",'
                'open_price decimal(10,2) comment "开盘价",'
                'high_price decimal(10,2) comment "最高价",'
                'low_price decimal(10,2) comment "最低价",'
                'close_price decimal(10,2) comment "收盘价",'
                'price_change decimal(10,2) comment "涨跌",'
                'pct_change varchar(10) comment "涨跌幅",'
                'volume bigint comment "成交数量",'
                'amount decimal(20,2) comment "成交金额")')
    return cur
def parse_data(securities):
    records = securities.get('records', [])
    if not records:
        return
    else:
        for i in records:
            yield (
                i['交易日期'],
                i['交易所'],
                i['证券简称'],
                i['证券代码'],
                i['币种'],
                i['开盘价'],
                i['最高价'],
                i['最低价'],
                i['收盘价'],
                i['涨跌'],
                i['涨跌幅'],
                i['成交数量'],
                i['成交金额']
            )

def write_to_mysql(cur, data_tuple):
    sql = '''
    insert into szx_database (
        trade_date, exchange, stock_name, stock_code, currency,
        open_price, high_price, low_price, close_price,
        price_change, pct_change, volume, amount
    ) values (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cur.execute(sql, data_tuple)

def get_recard(cur):
    cur.execute('select count(*) from szx_database')
    result = cur.fetchone()
    return result[0]

def main():
    # 从 2003-06-18 开始
    start_date = '2000-01-01'
    end_date = '2025-07-11'
    cur = init_mysql()
    for data in get_data(start_date, end_date):
        url, headers = get_args()
        response = requests.post(url, headers=headers, data=data)
        securities = response.json()
        parsed = list(parse_data(securities))
        if parsed:
            for data_tuple in parse_data(securities):
                    write_to_mysql(cur, data_tuple)
            print(f'{data["tdate"]}数据采集完毕')
            print('共采集{}条数据'.format(get_recard(cur)))
        else:
            print(f'{data["tdate"]}数据为空')



if __name__ == '__main__':
    main()