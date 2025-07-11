import asyncio
import aiohttp
from loguru import logger
from proxypool.schemas import Proxy
from proxypool.storages.redis import RedisClient
from proxypool.setting import TEST_TIMEOUT, TEST_BATCH, TEST_URL, TEST_VALID_STATUS, TEST_ANONYMOUS
from aiohttp import ClientProxyConnectionError, ServerDisconnectedError, ClientOSError, ClientHttpProxyError
from asyncio import TimeoutError
import re

EXCEPTIONS = (
    ClientProxyConnectionError,
    ConnectionRefusedError,
    TimeoutError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError,
    AssertionError
)


class Tester(object):
    """
    tester for testing proxies in queue
    """

    def __init__(self):
        """
        init redis
        """
        self.redis = RedisClient()
        self.loop = asyncio.get_event_loop()
        self.headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'
}

    async def test(self, proxy: Proxy):
        """
        test single proxy
        :param proxy: Proxy object
        :return:
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                logger.debug(f'testing {proxy.string()}')
                # if TEST_ANONYMOUS is True, make sure that
                # the proxy has the effect of hiding the real IP
                if TEST_ANONYMOUS:
                    # url = 'https://www.baidu.com/'
                    # url = 'http://2025.ip138.com'
                    url = 'http://httpbin.org/ip'
                    # 不加代理请求检测ip网站返回的ip和加代理请求检测ip比较
                    # 原始iP为origin_ip，加代理后为anonymous_ip
                    async with session.get(url, timeout=TEST_TIMEOUT,headers=self.headers) as response:
                        resp_json = await response.json()
                        origin_ip = resp_json['origin']
                        print(origin_ip)

                    # 你加代理去请求检测代理IP网站返回的IP和你加的IP进行比较
                    # proxy.host就是你加的代理IP的 host,
                    # anonymous_ip你加代理去访问返回的值
                    # proxy.string() ip:port
                    async with session.get(url, proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT) as response:
                        # resp_text = await response.text
                        # anonymous_ip = re.findall('(\d+\.\d+\.\d+\.\d+)', resp_text)[0]
                        resp_json = await response.json()
                        anonymous_ip = resp_json['origin']
                        print(anonymous_ip)
                        print(proxy.string())

                    assert origin_ip != anonymous_ip
                    assert proxy.host == anonymous_ip

                async with session.get(TEST_URL, proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT,
                                       allow_redirects=False) as response:
                    # 你请求目标网站返回的响应的状态码是否属于200 206 302，如果是，通过，给当前IP改为100分
                    # 就是self.redis.max(proxy)这步
                    if response.status in TEST_VALID_STATUS:
                        self.redis.max(proxy)
                        logger.debug(f'proxy {proxy.string()} is valid, set max score')
                    else:
                        # 如果请求失败了，则当前分数减一
                        self.redis.decrease(proxy)
                        logger.debug(f'proxy {proxy.string()} is invalid, decrease score')
            except EXCEPTIONS:
                self.redis.decrease(proxy)
                logger.debug(f'proxy {proxy.string()} is invalid, decrease score')
    # 'https://blog.csdn.net/bailang_zhizun/article/details/107863671'
    @logger.catch
    def run(self):
        """
        test main method
        :return:
        """
        # event loop of aiohttp
        logger.info('starting tester...')
        # 获取代理IP的数量
        count = self.redis.count()
        logger.debug(f'{count} proxies to test')
        cursor = 0
        while True:
            # 参考为https://www.cnblogs.com/Mike_Chang/p/9499625.html
            # 这里20个一组验证代理IP，直到游标返回为0，验证完毕
            logger.debug(f'testing proxies use cursor {cursor}, count {TEST_BATCH}')
            cursor, proxies = self.redis.batch(cursor, count=TEST_BATCH)
            if proxies:
                tasks =[asyncio.gather(self.test(proxy)) for proxy in proxies]
                self.loop.run_until_complete(asyncio.wait(tasks))
            if not cursor:
                break

def run_tester():
    host = '120.43.58.101'
    port = '36086'
    tasks = [asyncio.gather(tester.test(Proxy(host=host, port=port)))]
    tester.loop.run_until_complete(asyncio.wait(tasks))
if __name__ == '__main__':
    tester = Tester()
    # tester.run()
    run_tester()

