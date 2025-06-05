import redis
from datetime import datetime, timedelta

r = redis.Redis(host='43.143.173.241', port=6379, password='123456', db=1, decode_responses=True)
base_url = 'https://e0430d16720e4211b5e072c26205c890.z3c.jin10.com/get/data?date='
redis_key = 'jinshishuju:start_urls'

start_date = datetime.strptime("2020-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2025-05-16", "%Y-%m-%d")

current = start_date
while current <= end_date:
    date_str = current.strftime("%Y-%m-%d")
    full_url = f"{base_url}{date_str}&category=cj"
    r.lpush(redis_key, full_url)
    print("Pushed:", full_url)
    current += timedelta(days=1)