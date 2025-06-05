import os.path
from DrissionPage import Chromium
from DrissionPage.common import ChromiumOptions

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
if not os.path.exists('img'):
    os.makedirs('img')
# 循环抓取300张验证码
for i in range(1, 301):
    i += 2
    page.wait.load_start()
    iframe_ele = page.ele('x://*[@id="tcaptcha_iframe_dy"]')
    iframe_page = page.get_frame(iframe_ele)
    iframe_page.wait.load_start()
    img_data = iframe_page.get_screenshot(path=f'img/{i}.png')
    iframe_page.wait.ele_displayed('x://*[@id="tcStatus"]/div[1]/div[3]')
    iframe_page.ele('x://*[@id="tcStatus"]/div[1]/div[3]').click()
