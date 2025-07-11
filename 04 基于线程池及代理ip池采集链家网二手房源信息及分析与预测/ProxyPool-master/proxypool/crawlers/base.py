from retrying import retry
import requests
from loguru import logger
from proxypool.setting import GET_TIMEOUT
from fake_headers import Headers
import time
class BaseCrawler(object):
    urls = []
    # stop_max_attempt_number
    # 在停止之前尝试的最大次数，最后一次如果还是有异常则会抛出异常，停止运行，默认为5次
    # retry_on_result
    # 指定一个函数，如果指定的函数返回True，则重试；否则退出
    # wait_fixed
    # 两次retry之间等待2秒
    # 参考https://blog.csdn.net/linzhjbtx/article/details/86581972
    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=10000)
    def fetch(self, url, **kwargs):
        try:
            # 随机生成header头信息
            headers = Headers(headers=True).generate()
            # 与get方法类似，获取key，如果没有获得到，则设置默认值
            kwargs.setdefault('timeout', GET_TIMEOUT)
            kwargs.setdefault('verify', False)
            kwargs.setdefault('headers', headers)
            response = requests.get(url ,**kwargs)
            if response.status_code == 200:
                # response.encoding = 'utf-8'
                return response.json()
        except requests.ConnectionError:
            return
    # 捕获异常到日志中，参考https://cuiqingcai.com/7776.html
    @logger.catch
    def crawl(self):
        """
        crawl main method
        """
        # for url in self.urls:
        # while True:
        #     # logger.info(f'fetching {url}')
        #     # url = 'https://api.xiaoxiangdaili.com/ip/get?appKey=916319498167275520&appSecret=H9yk8JNU&cnt=1&wt=json''https://api.xiaoxiangdaili.com/ip/get?appKey=916319498167275520&appSecret=H9yk8JNU&cnt=1&wt=json'
        #     url = 'https://api.xiaoxiangdaili.com/ip/get?appKey=1232964237073469440&appSecret=jA2gpzht&cnt=1&wt=json&method=https&city=&province='
        #     html = self.fetch(url)
        #     time.sleep(1)
        #     for proxy in self.parse(html):
        #         logger.info(f'fetched proxy {proxy.string()} from {url}')
        #         yield proxy
        #     break
        url = 'https://api.xiaoxiangdaili.com/ip/get?appKey=1227398998999322624&appSecret=XWWJtL5G&cnt=&wt=json&method=http&city=&province='
        for proxy in self.parse(self.fetch(url)):
            logger.info(f'fetched proxy {proxy.string()} from {url}')
            yield proxy