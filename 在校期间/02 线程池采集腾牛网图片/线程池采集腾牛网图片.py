import os
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# 伪装请求头
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

# 准备
def prepare(url):
    if not os.path.exists('img'):
        os.mkdir('img')
    response = requests.get(url, headers=headers)
    return response.text

# 采集数据
def get_data(html_data):
    img_data_list = []
    soup = BeautifulSoup(html_data, 'lxml')
    data1 = soup.find('ul', class_='g-gxlist-imgbox')
    for i in data1.find_all('img'):
        img_data_list.append(i.get('src'))
    return img_data_list

# 存储数据
def write_to_img(img_data_list, number):
    j = 0
    for i in img_data_list:
        j += 1
        reponse = requests.get(i, headers=headers)
        path_name = './img/' + number + '_' + str(j) + '.jpg'
        with open(path_name, 'ab') as f:
            f.write(reponse.content)

# 程序入口
if __name__ == '__main__':
    with ThreadPoolExecutor(3) as executor:
        for i in range(1, 207):
            time.sleep(1)
            html_data = executor.submit(prepare, f'https://www.qqtn.com/tx/haokantx_{i}.html').result()
            img_data_list = executor.submit(get_data, html_data).result()
            executor.submit(write_to_img, img_data_list, number=str(i))
            print(f'第{i}页输入写入完毕')
    print('程序执行完毕')
