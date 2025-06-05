import asyncio
import pandas as pd
from pyppeteer import launch
from pyquery import PyQuery as pq

def get_proxy_info():
    # 自己的隧道代理信息
    proxy_user = '1229248023675424768'
    proxy_pass = 'nW07aj7M'
    proxy_ip = 'http-dynamic.xiaoxiangdaili.com:10030'
    return proxy_ip, proxy_user, proxy_pass


async def main(proxy_ip, proxy_user, proxy_pass):
    browser = await launch(
        headless=False,
        executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        args=[
            '--no-sandbox',
            '--disable-gpu',
            '--disable-dev-tools',
            '--disable-infobars',
            '--start-maximized',
            f'--proxy-server=http://{proxy_ip}'
        ],
        defaultViewport=None
    )
    """
    ,
            f'--proxy-server=http://{proxy_ip}'
    """
    page = await browser.newPage()
    # 设置隧道代理的认证信息
    await page.authenticate({
        'username': proxy_user,
        'password': proxy_pass
    })
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    )
    await page.goto('https://www.lagou.com/wn/zhaopin?fromSearch=true&kd=python&city=%E5%85%A8%E5%9B%BD')
    await page.waitForSelector('[name="account"]')
    await page.type('[name="account"]', '15732471620')
    await page.waitForSelector('[name="password"]')
    await page.type('[name="password"]', '@SCRscr1')
    button = await page.xpath('//*[@id="lg-passport-box"]/div/div[2]/div/div[4]/div[2]/div')
    await button[0].click()
    login = await page.xpath('//*[@id="lg-passport-box"]/div/div[2]/div/div[3]/button')
    await login[0].click()
    # 由于验证码形式会更改，所以这里选择手动打码
    await asyncio.sleep(20)
    # x遮挡了了搜索按钮，手动处理一下
    # x1 = await page.xpath('//*[@id="lg_tbar"]/div[2]/ul/li[4]/div[2]/div/div/div[4]')
    # await x1[0].click()
    # await asyncio.sleep(1)
    # x2 = await page.xpath('//*[@id="lg_tbar"]/div[2]/ul/li[3]/div[2]/div/div/span')
    # await x2[0].click()
    # await asyncio.sleep(1)
    # 搜索岗位
    await page.waitForSelector('#search_input')
    await asyncio.sleep(3)
    await page.type('#search_input', 'python')
    await asyncio.sleep(10)
    await page.waitForSelector('#search_input')
    await page.click('#search_button')
    await asyncio.sleep(20)
    pages = await browser.pages()  # 返回所有打开的标签页
    target_page = pages[2]
    await target_page.bringToFront()
    job_title_list, region_list, salary_range_list, experience_list, education_list, company_list, business_list, finance_list, people_list, description_list = [[] for _ in range(10)]
    recruit_dict = {
        '岗位名': [],
        '岗位位置': [],
        '薪资范围': [],
        '经验要求': [],
        '学历要求': [],
        '公司名': [],
        '主要业务': [],
        '融资情况': [],
        '人员规模': [],
        '岗位描述': []
    }
    j = 0
    old_yz = ''
    while j < 30:
        j += 1
        await asyncio.sleep(3)
        html = await target_page.content()
        doc = pq(html)
        # 获取岗位名和岗位位置
        data1 = doc('#openWinPostion')
        for i in data1.items():
            new_yz = i.text()
            job_title = i.text().split('[')[0]
            region = i.text().split('[')[1].strip(']')
            job_title_list.append(job_title)
            region_list.append(region)
        if new_yz == old_yz:
            print('页面未刷新，重新采集第{}页数据'.format(j-1))
            await target_page.click('.lg-pagination-next')
            j -= 1
            continue
        else:
            print(f'开始采集第{j}页数据')
            old_yz = new_yz

        # 获取薪资范围，经验要求以及学历
        data2 = doc('[class*="p-bom"]')
        for i in data2.items():
            salary_range = i.text().split(' / ')[0].split('经验')[0]
            experience = '经验' + i.text().split(' / ')[0].split('经验')[1]
            education = i.text().split(' / ')[1]
            salary_range_list.append(salary_range)
            experience_list.append(experience)
            education_list.append(education)
        # 获取公司名
        data3 = doc('[class*="company-name"]')
        for i in data3.items():
            company = i.text()
            company_list.append(company)
        # 获取公司主要业务，融资情况以及人员规模
        data4 = doc('[class*="industry__"]')
        for i in data4.items():
            business = i.text().split(' / ')[0]
            financing = i.text().split(' / ')[1]
            people = i.text().split(' / ')[2]
            business_list.append(business)
            finance_list.append(financing)
            people_list.append(people)
        # 获取岗位描述
        data5 = doc('[class*="item-bom__"]')
        for _ in data5.items():
            data6 = _.children().eq(1)
            for i in data6.items():
                description = i.text()
                description_list.append(description)
        # 将每一条完整的数据加入到字典中，为 pandas 写入 csv 文件做准备
        for i in zip(job_title_list, region_list, salary_range_list, experience_list,education_list,company_list,business_list,finance_list,people_list,description_list):
            recruit_dict['岗位名'].append(i[0])
            recruit_dict['岗位位置'].append(i[1])
            recruit_dict['薪资范围'].append(i[2])
            recruit_dict['经验要求'].append(i[3])
            recruit_dict['学历要求'].append(i[4])
            recruit_dict['公司名'].append(i[5])
            recruit_dict['主要业务'].append(i[6])
            recruit_dict['融资情况'].append(i[7])
            recruit_dict['人员规模'].append(i[8])
            recruit_dict['岗位描述'].append(i[9])

        # 翻到下一页
        await target_page.click('.lg-pagination-next')

    await browser.close()
    return recruit_dict


def write_to_csv(recruit_dict):
    df = pd.DataFrame(recruit_dict)
    df.index = df.index + 1
    df.to_csv('招聘数据.csv', mode='a', index_label='编号')

if __name__ == '__main__':
    proxy_ip, proxy_user, proxy_pass = get_proxy_info()
    recruit_dict = asyncio.run(main(proxy_ip, proxy_user, proxy_pass))
    write_to_csv(recruit_dict)