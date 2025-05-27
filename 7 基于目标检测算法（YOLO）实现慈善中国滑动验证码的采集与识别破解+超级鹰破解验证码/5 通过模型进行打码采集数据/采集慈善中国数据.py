import cv2
from ultralytics import YOLO
from pymongo import MongoClient
from DrissionPage import Chromium
from DrissionPage.common import ChromiumOptions

# 加载模型
model = YOLO('last.pt')

# 启动设置
co = ChromiumOptions()
".auto_port()"
co.set_argument('--start-maximized')
browser = Chromium(co)
page = browser.get_tab()

page.get('https://cszg.mca.gov.cn/platform/login.html')
page.ele('.content1_search_button').click()
page.wait(2)

max_retries = 10
for i in range(max_retries):
    page.wait.ele_displayed('x://*[@id="cutImg"]')
    page.ele('.captchaContainer').get_screenshot(path=f'images/image{i}.jpg')
    images = cv2.imread(f'images/image{i}.jpg')
    results = model(images)
    for result in results:
        boxes = result.boxes.xyxy
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            print(f"滑动距离: {x1 - 50}")
    page.actions.move_to('x://*[@id="slider"]').hold().move(offset_x=x1 - 50, duration=1.5).release()
    try:
        page.wait.ele_displayed('x://*[@id="content1_search_info_cszz"]/table/thead/tr/th[2]/div', timeout=5)
        print("验证成功")
        break
    except Exception:
        print("验证失败，刷新验证码重试")
        page.ele('x://*[@id="captchadiv"]/div[1]/img').click()
        page.wait(2)


def get_data():
    number_list, id_list, name_list, time_list, jiguan_list = [[] for i in range(5)]
    numbers = page.eles('x://*[@id="gsdiv"]/table/tbody/tr/td[1]')
    for i in numbers:
        number_list.append(i.text)
    id = page.eles('x://*[@id="gsdiv"]/table/tbody/tr/td[2]/a')
    for i in id:
        id_list.append(i.text)
    name = page.eles('x://*[@id="gsdiv"]/table/tbody/tr/td[3]/a')
    for i in name:
        name_list.append(i.text)
    time = page.eles('x://*[@id="gsdiv"]/table/tbody/tr/td[4]')
    for i in time:
        time_list.append(i.text)
    jiguan = page.eles('x://*[@id="gsdiv"]/table/tbody/tr/td[5]')
    for i in jiguan:
        jiguan_list.append(i.text)
    return number_list, id_list, name_list, time_list, jiguan_list

def init_mongodb():
    conn = MongoClient('localhost', 27017)
    db = conn['cishan']
    col = db['cishandata']
    return col

def write_to_mongodb(col, number_list, id_list, name_list, time_list, jiguan_list):
    docs = []
    for i in range(len(number_list)):
        doc = {
            "_id": number_list[i],
            "idd": id_list[i],
            "name": name_list[i],
            "time": time_list[i],
            "jiguan": jiguan_list[i]
        }
        docs.append(doc)

    if docs:
        col.insert_many(docs)

if __name__ == '__main__':
    for i in range(2):
        number_list, id_list, name_list, time_list, jiguan_list = get_data()
        col = init_mongodb()
        write_to_mongodb(col, number_list, id_list, name_list, time_list, jiguan_list)
        page.ele('x://*[@id="gsdiv"]/div/span[3]').click()
        page.wait(3)