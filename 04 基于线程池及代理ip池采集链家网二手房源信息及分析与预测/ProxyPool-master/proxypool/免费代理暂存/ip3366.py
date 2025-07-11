from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler


BASE_URL = 'https://proxy.ip3366.net/free/?action=china&page={}'
MAX_PAGE = 50


class Ip3366Crawler(BaseCrawler):
    """
    daili66 crawler, http://www.66ip.cn/1.html
    """
    urls = [BASE_URL.format(page) for page in range(1, MAX_PAGE + 1)]

    
    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        # 取的是下标大于1的tr，从第1行开始，这个玩意是从1开始
        # 具体语法可以参考https://www.jianshu.com/p/7eb136bbe317
        trs = doc('.container table tr:gt(0)').items()
        for tr in trs:
            # 取下面第一个元素
            host = tr.find('td:nth-child(1)').text()
            port = int(tr.find('td:nth-child(2)').text())
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = Ip3366Crawler()
    for proxy in crawler.crawl():
        print(proxy)
