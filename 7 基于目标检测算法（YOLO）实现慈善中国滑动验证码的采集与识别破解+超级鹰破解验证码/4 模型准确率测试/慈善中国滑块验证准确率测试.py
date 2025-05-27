import cv2
import os.path
from ultralytics import YOLO
from DrissionPage import Chromium
from DrissionPage.common import ChromiumOptions

# 加载模型
model = YOLO('last.pt')

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
    images = cv2.imread(f'images/image{i}.jpg')
    results = model(images)
    for result in results:
        boxes = result.boxes.xyxy
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            print(f"滑动距离: {x1 - 50}")
    page.actions.move_to('x://*[@id="slider"]').hold().move(offset_x=x1 - 50, duration=1.5)
    page.ele('.captchaContainer').get_screenshot(path=f'results/image{i}.jpg')
    page.ele('x://*[@id="captchadiv"]/div[1]/img').click()
    page.wait(2)