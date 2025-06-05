## Python中的自动化

### 实现自动化的方式

- `Selenium`
- `Pyppeteer`
- `Playwright`
- `DrissionPage`



### 四种自动化工具的对比

| 特性/工具          | **Selenium**                | **Pyppeteer**                | **Playwright**               | **DrissionPage**                      |
| ------------------ | --------------------------- | ---------------------------- | ---------------------------- | ------------------------------------- |
| 是否支持动态渲染   | ✅ 支持 JS 渲染              | ✅ 支持                       | ✅ 支持                       | ✅ 支持（集成浏览器驱动）              |
| 是否需要浏览器驱动 | ✅ 需要（手动下载/设置路径） | ❌ 自动下载 Chromium          | ❌ 自动下载 Chromium          | ❌ 内置驱动（也可选用 selenium）       |
| 支持无头浏览器     | ✅                           | ✅（默认无头）                | ✅（默认无头）                | ✅（用的 pyppeteer/selenium）          |
| 编程模式           | 同步（简单）                | 异步（需 asyncio）           | 异步（推荐 asyncio）         | 同步/异步模式都支持（封装好了）       |
| 多浏览器支持       | ✅（Chrome/Firefox/Edge）    | ❌（仅 Chromium）             | ✅（Chromium/Firefox/WebKit） | ✅（默认 Chromium，可扩展）            |
| 操作灵活性         | ⭐⭐⭐⭐                        | ⭐⭐⭐⭐                         | ⭐⭐⭐⭐⭐                        | ⭐⭐⭐（适合爬虫场景）                   |
| 文档/社区支持      | ⭐⭐⭐⭐⭐（经典项目）           | ⭐⭐（文档一般）               | ⭐⭐⭐⭐（文档好）               | ⭐⭐（中文文档友好，GitHub 社区小众）   |
| 安装易用性         | ⭐⭐（需配驱动）              | ⭐⭐⭐（首次运行下载 Chromium） | ⭐⭐⭐⭐                         | ⭐⭐⭐⭐⭐（pip 一键装）                   |
| 支持截图/PDF       | 有（截图），PDF 需额外库    | ✅ 原生支持                   | ✅ 原生支持                   | ✅（封装 pyppeteer 功能）              |
| 抓取静态网页速度   | ❌ 慢（全浏览器）            | ⭐⭐⭐⭐                         | ⭐⭐⭐⭐                         | ⭐⭐⭐⭐⭐（requests 静态爬 + 浏览器动爬） |
| 适合做爬虫         | ⭐⭐（反爬多）                | ⭐⭐⭐⭐（可改 UA 等）           | ⭐⭐⭐⭐（可模拟设备环境）       | ⭐⭐⭐⭐⭐（集成代理、反爬处理简单）       |
| 适合做自动化测试   | ⭐⭐⭐⭐⭐                       | ⭐⭐（偏爬虫）                 | ⭐⭐⭐⭐（官方主推测试）         | ⭐（不推荐）                           |



如何选择这四种自动化工具

| 你要做的事                     | 推荐工具                     | 原因说明                                        |
| ------------------------------ | ---------------------------- | ----------------------------------------------- |
| 快速爬虫开发（静+动一体）      | ✅ **DrissionPage**           | 写法简单，自动选 requests 或 selenium，无痛切换 |
| 页面内容复杂、强 JS 动态渲染   | ✅ **Playwright** / Pyppeteer | 强 JS 渲染能力、异步高性能                      |
| 自己写爬虫但懒得装驱动         | ✅ Pyppeteer / DrissionPage   | 自动下载 Chromium，无需手动搞浏览器驱动         |
| 学习自动化测试（测试业务流程） | ✅ Selenium / Playwright      | 多浏览器支持、自动化测试生态成熟                |
| 模拟登录、自动验证码识别       | ✅ DrissionPage + 三方库      | 易集成验证码打码平台，封装好                    |



### Selenium

- 安装：pip install selenium

- 需要安装各个浏览器驱动，并指定浏览器驱动位置（或在系统path中配置），注意在Selenium4.6及后续版本不需要自己安装浏览器驱动了

- 代码示例

  ```python
  import time
  # 浏览器驱动
  from selenium import webdriver
  # 查找元素
  from selenium.webdriver.common.by import By
  # 启动设置
  from selenium.webdriver.chrome.options import Options
  # 用于模拟键盘按键输入（如回车、删除、Tab 等）
  """
      Keys.ENTER：回车
      Keys.TAB：跳到下一个输入框
      Keys.BACKSPACE：删除
      Keys.ESCAPE：ESC
      Keys.CONTROL + 'a'：Ctrl+A 全选
  """
  from selenium.webdriver.common.keys import Keys
  # 显式等待工具，用来等待某个页面元素加载出来
  from selenium.webdriver.support.ui import WebDriverWait
  # 定义等待的“条件”
  from selenium.webdriver.support import expected_conditions as EC
  
  
  # 启动设置
  op = Options()
  # 设置无头浏览器（不显示浏览器界面）
  op.add_argument('--headless')
  # 模拟浏览器普通UA
  op.add_argument("user-agent=你的UserAgent")
  # 进制被检测自动化程序
  op.add_experimental_option("excludeSwitches", ["enable-automation"])
  op.add_experimental_option("useAutomationExtension", False)
  
  # 以启动设置打开浏览器
  driver = webdriver.Chrome(options=op)
  browser = webdriver.Chrome()
  
  # 打开网页
  browser.get('http://www.python.org')
  
  # 查找元素--常见查找方式
  driver.find_element(By.ID, "kw")               # 通过 id
  driver.find_element(By.NAME, "wd")             # 通过 name
  driver.find_element(By.CLASS_NAME, "xxx")      # 通过 class
  driver.find_element(By.XPATH, "//div[@id='xx']")  # 通过 XPath
  
  # 输入文字 + 回车
  search_box = driver.find_element(By.ID, "kw")
  search_box.send_keys("Python")
  search_box.send_keys(Keys.ENTER)
  
  # 点击按钮
  button = driver.find_element(By.ID, "submit")
  button.click()
  
  # 等待页面加载
  # 简单等待
  time.sleep(2)
  # 更优方法：显式等待
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "result")))
  
  # 网页截图
  driver.save_screenshot("screenshot.png")
  
  # 执行JavaScript
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  
  # 操作iframe（子页面）
  driver.switch_to.frame("iframe_id")     # 进入 iframe
  driver.switch_to.default_content()      # 回到主页面
  
  # 上传文件
  upload = driver.find_element(By.ID, "file_input")
  upload.send_keys("D:/path/to/file.jpg")
  ```

  

### Pyppeteer

- 安装：pip install pyppeteer

- 代码示例

  ```python
  # 启动浏览器并打开页面
  import asyncio
  from pyppeteer import launch
  
  async def main():
      # 启动浏览器
      browser = await launch(headless=True)  # headless=True 表示无头浏览器，不会显示 UI
      page = await browser.newPage()  # 创建一个新的标签页
      await page.goto('https://www.baidu.com')  # 打开指定网址
      # 等待页面加载完成
      await page.waitForSelector('#kw')  # 等待 id 为 'kw' 的输入框加载完成
      # 截图保存
      await page.screenshot({'path': 'baidu.png'})  # 截图并保存
      # 关闭浏览器
      await browser.close()
  # 运行主函数
  asyncio.get_event_loop().run_until_complete(main())
  
  # 模拟输入和点击
  async def main():
      browser = await launch(headless=True)
      page = await browser.newPage()
      await page.goto('https://www.baidu.com')
      # 输入搜索内容
      await page.type('#kw', 'Python')
      # 点击搜索按钮
      await page.click('#su')
      # 等待搜索结果加载
      await page.waitForSelector('#content_left')
      # 截图保存
      await page.screenshot({'path': 'baidu_search_result.png'})
      await browser.close()
  asyncio.get_event_loop().run_until_complete(main())
  
  # 获取页面内容
  async def main():
      browser = await launch(headless=True)
      page = await browser.newPage()
      await page.goto('https://www.baidu.com')
      # 获取页面的 HTML 内容
      html_content = await page.content()
      print(html_content)  # 打印页面 HTML
      # 获取页面的标题
      title = await page.title()
      print(title)  # 打印页面标题
      await browser.close()
  asyncio.get_event_loop().run_until_complete(main())
  
  # 生成网页截图
  async def main():
      browser = await launch(headless=True)
      page = await browser.newPage()
      await page.goto('https://www.baidu.com')
      # 截图并保存为 baidu.png
      await page.screenshot({'path': 'baidu.png'})
      await browser.close()
  asyncio.get_event_loop().run_until_complete(main())
  
  # 保存网页为 PDF
  async def main():
      browser = await launch(headless=True)
      page = await browser.newPage()
      await page.goto('https://www.baidu.com')
      # 将网页保存为 PDF
      await page.pdf({'path': 'baidu.pdf'})
      await browser.close()
  asyncio.get_event_loop().run_until_complete(main())
  
  # 查找元素的方法querySelector和querySelectorAll（通过css选择器查找）
  ```

- 常见问题

  ```python
  # 常见问题
  async def main():
      browser = await launch(headless=True)
      page = await browser.newPage()
      # Pyppeteer 报错 TimeoutError
      # 解决方法：可以增加 page.goto() 的超时时间，例如：
      await page.goto('https://www.example.com', {'timeout': 60000})  # 设置 60 秒超时
      # Pyppeteer 不支持 Windows 10 的 “沙盒” 模式
      # 解决方法：可以通过禁用沙盒来运行 Pyppeteer：
      browser = await launch({'headless': True, 'args': ['--no-sandbox', '--disable-setuid-sandbox']})
  ```

  

### Playwright

```python
# 安装：pip install playwright
# 初始化：playwright install

from playwright.sync_api import sync_playwright

def run():
    # 启动 Playwright
    with sync_playwright() as p:
        # 启动 Chromium 浏览器，可设置 headless=True 为无头模式
        browser = p.chromium.launch(headless=False)

        # 打开一个新标签页
        page = browser.new_page()

        # 访问目标网页
        page.goto('https://example.com')

        # 自动等待页面加载并获取标题
        title = page.title()
        print("页面标题:", title)

        # 获取第一个 h1 标签的文本内容
        h1_text = page.text_content('h1')
        print("主标题内容:", h1_text)

        # 填写表单示例（如果页面有输入框）
        # page.fill('input[name="username"]', 'my_username')
        # page.fill('input[name="password"]', 'my_password')

        # 模拟点击按钮（自动等待按钮加载）
        # page.click('button#login')

        # 截图当前页面保存为 PNG 文件
        page.screenshot(path='screenshot.png')

        # 生成 PDF（Chromium 才支持）
        page.pdf(path='page.pdf')

        # 提取多个链接文本
        links = page.locator('a')
        for i in range(links.count()):
            print("链接文本:", links.nth(i).text_content())

        # 文件上传示例（页面需要有 file input 元素）
        # page.set_input_files('input[type="file"]', 'test.txt')

        # 文件下载示例（页面需要有下载按钮）
        # with page.expect_download() as download_info:
        #     page.click('#download-btn')
        # download = download_info.value
        # download.save_as('downloaded_file.zip')

        # 关闭浏览器
        browser.close()

# 执行主函数
if __name__ == "__main__":
    run()
```



### DrissionPage

- DrissionPage官网：https://drissionpage.cn/

