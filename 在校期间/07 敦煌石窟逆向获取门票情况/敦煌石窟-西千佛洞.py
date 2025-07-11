import time
import math
import execjs
import requests

headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.mgk.org.cn",
    "Referer": "https://www.mgk.org.cn/ticket",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "sendinfoDhPc": "s%3ABnNNgCcEPt3NpuSFbdFCXYcGmQPc87Ps.QR4ZkzQp3dvwtu77%2BYQtdB%2FNj%2FgVueBzRPYEgZpqKxg",
    "Hm_lvt_43b18e3ab4b4ac9f3d1679e922eee451": "1749899842,1749948450,1750124497",
    "HMACCOUNT": "C883C18708F9D3DD",
    "tgw_l7_route": "139345d5b33e5d7f237234ee0d951c66",
    "Hm_lpvt_43b18e3ab4b4ac9f3d1679e922eee451": "1750124548",
    "SECKEY_ABVK": "wjzCnjp+JVKaq4CmPggYSyhaQTjJQwTbX6WvH0vpiEg%3D",
    "BMAP_SECKEY": "T1P9XmklKVvgEj3vl2zdidYAYh4YBZ8t-2cQXzqazteCFPnLAl0RuYEDTur__CNiWavZDdZHJhG_ZMJB64bdj6L_SsLqSRT_tJnoOTH-sUO0zcMyAEItNkhucTRbvHy7ZUzlXQHLd-ii6o5Z7OjqwAoRZcIiTYi1D759DmuCx9MGCDOYUJqIfG82JhIVuRPl"
}
url = "https://www.mgk.org.cn/head/calendar"

with open('敦煌石窟.js', 'r') as f:
    f = f.read()
current_time = math.ceil(time.time()*1000)
print('当前时间为:')
print(current_time)

data = execjs.compile(f).call('get_data', current_time)
print('js解密data参数为:')
print(data)

response = requests.post(url, headers=headers, cookies=cookies, data=data)
result = response.json()[0]['data']
print('获取门票情况如下：')
for i in result:
    # print(i)
    day = i['DAY']
    sum_num = i['sumNum']
    a_num = i['A_num']
    print(f'{day}:{sum_num}\n旺季票:{a_num}')