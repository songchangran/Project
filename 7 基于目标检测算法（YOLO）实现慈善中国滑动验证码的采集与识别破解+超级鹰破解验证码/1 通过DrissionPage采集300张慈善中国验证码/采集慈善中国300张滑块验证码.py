import os.path
from DrissionPage import Chromium
from DrissionPage.common import ChromiumOptions

co = ChromiumOptions().auto_port()
co.set_argument('--start-maximized')
browser = Chromium(co)
page = browser.get_tab()
page.get('https://cszg.mca.gov.cn/platform/login.html')
page.ele('.content1_search_button').click()
page.wait(2)

if not os.path.exists('images'):
    os.makedirs('images')

for i in range(1, 301):
    page.wait.ele_displayed('x://*[@id="cutImg"]')
    page.ele('.captchaContainer').get_screenshot(path=f'images/image{i}.jpg')
    page.ele('x://*[@id="captchadiv"]/div[1]/img').click()