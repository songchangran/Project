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
co.set_user_agent(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
)
# 创建浏览器对象
browser = Chromium(co)
# 创建 page 对象并进行相关操作
page = browser.get_tab()
page.get('https://www.douban.com/')
page.wait.load_start()
# 点击“密码登录”
page.ele('x:/html/body/div[1]/div[1]/ul[1]/li[2]').click()
# 输入用户名
page.ele('x://*[@id="username"]').clear().input('12345678901')
# 输入密码
page.ele('x://*[@id="password"]').clear().input('qwe123')
# 点击“登录豆瓣”
page.ele('x:/html/body/div[1]/div[2]/div[1]/div[5]/a').click()
if not os.path.exists('img1'):
    os.makedirs('img1')
if not os.path.exists('img2'):
    os.makedirs('img2')

for i in range(10):
    page.wait(2)
    iframe = page.get_frame('x://*[@id="tcaptcha_iframe_dy"]')
    iframe.get_screenshot(path=f'img1/slic_{i+1}.jpg')
    image_path = f'img1/slic_{i+1}.jpg'
    image = cv2.imread(image_path)

    results = model(image)
    found = False  # 用于标记是否识别到了滑块缺口

    for result in results:
        boxes = result.boxes.xyxy
        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                print(f"滑动距离: {x1 - 64}")
                page.wait(1)
                iframe.actions.move_to('x://*[@id="tcOperation"]/div[6]').hold().move(offset_x=x1 - 64, duration=1.5)
                page.wait(2)
                found = True
                break
        else:
            print(f'第{i+1}次未识别到滑块目标，刷新重试中...')

    if not found:
        iframe.actions.move_to('x://*[@id="reload"]/img').click()
        continue  # 直接跳过当前循环，重新开始
    else:
        page.wait(2)
        iframe.get_screenshot(path=f'img2/result_{i+1}.jpg')
        iframe.actions.move_to('x://*[@id="reload"]/img').click()