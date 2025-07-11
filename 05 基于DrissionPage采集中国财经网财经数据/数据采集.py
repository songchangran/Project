from DrissionPage import Chromium
from DrissionPage import ChromiumOptions
import redis
import pymongo
import hashlib

# 初始化 Mongo
def init_mongo():
    client = pymongo.MongoClient('localhost', 27017)
    # 选择数据库
    db = client['datas']
    # 选择集合
    collection = db['cj_datas']
    return collection

# 初始化 Redis
def init_redis():
    r = redis.Redis(host='localhost', port=6379, db=1)
    return r

# 用于存储自增计数器的集合
counter_collection = init_mongo()["counters"]

def get_next_sequence_value(sequence_name):
    # 使用 findAndModify 保证原子性
    counter = counter_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,  # 如果不存在该计数器则插入
        return_document=True
    )
    return counter["sequence_value"]

# 持久化数据到 Mongo中
def write_to_mongo(collection, data):
    # 获取自增 ID
    sequence_value = get_next_sequence_value("my_id_sequence")
    # 将自增值添加到文档数据中
    data["_id"] = sequence_value
    collection.insert_one(data)

def get_fingerprint(data):
    # 获取数据的哈希值（MD5）
    return hashlib.md5(data.encode('utf-8')).hexdigest()

def check_and_add(data, r):
    fingerprint = get_fingerprint(data)
    if r.sismember('data_fingerprints', fingerprint):
        return False
    else:
        r.sadd('data_fingerprints', fingerprint)
        return True

# 主流程函数
def opration(collection, r):
    co = ChromiumOptions()
    co.set_argument('--start-maximized')

    browser = Chromium(co)
    page = browser.latest_tab

    page.get('http://www.ce.cn/')
    # 点击财经
    page.ele('x:/html/body/div[2]/div/ul/li[3]/span/a').click()
    page = browser.latest_tab
    # 点击银行
    page.ele('x:/html/body/div[3]/ul/li[9]').click()
    for i in range(1, 41):
        browser.get_tab(-1).close()
        page.wait(2)
        page = browser.latest_tab
        for ul in page.eles('.list2'):
            content = ul.text
            data = content.strip('· ').split('\n· ')
            for d in data:
                news = d.split('[ ')[0]
                times = d.split('[ ')[1].strip(' ]')
                if check_and_add(news, r):
                    write_to_mongo(collection,
                                   {
                                       'news': news,
                                       'times': times,
                                   })
                else:
                    print('数据已存在')
        print(f'第{i}页采集完毕')
        page.ele('text=下一页>').click()

if __name__ == '__main__':
    collection = init_mongo()
    r = init_redis()
    opration(collection, r)