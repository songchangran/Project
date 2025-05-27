import json
import os.path
from DrissionPage import Chromium
from chaojiying import Chaojiying_Client
from DrissionPage.common import ChromiumOptions

with open('./account.json', 'r') as f:
    data = json.load(f)

username = data['username']
password = data['password']
soft_id = data['soft_id']

# 启动设置
co = ChromiumOptions().auto_port()
co.set_argument('--start-maximized')
browser = Chromium(co)
page = browser.get_tab()
page.get('https://cszg.mca.gov.cn/platform/login.html')
page.ele('.content1_search_button').click()
page.wait(2)

if not os.path.exists('images'):
    os.makedirs('images')
if not os.path.exists('results'):
    os.makedirs('results')

for i in range(1, 10):
    page.wait.ele_displayed('x://*[@id="cutImg"]')
    page.ele('.captchaContainer').get_screenshot(path=f'images/image{i}.jpg')
    chaojiying = Chaojiying_Client(username, password, soft_id)
    im = open(f'images/image{i}.jpg', 'rb').read()
    result = chaojiying.PostPic(im, 9900)['pic_str']
    x1, y1, x2, y2 = result.split('|')[0].split(',')
    x3, y3, x4, y4 = result.split('|')[1].split(',')
    print(f"滑动距离: {int(x3)-int(x1)-42}")
    page.actions.move_to('x://*[@id="slider"]').hold().move(offset_x=int(x3)-int(x1)-42, duration=1.5)
    page.ele('.captchaContainer').get_screenshot(path=f'results/image{i}.jpg')
    page.ele('x://*[@id="captchadiv"]/div[1]/img').click()
    page.wait(2)