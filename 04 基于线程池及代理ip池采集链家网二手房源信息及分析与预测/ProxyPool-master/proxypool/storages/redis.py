import redis
from proxypool.exceptions import PoolEmptyException
from proxypool.schemas.proxy import Proxy
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB, REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MIN, \
    PROXY_SCORE_INIT
from random import choice
from typing import List
from loguru import logger
from proxypool.utils.proxy import is_valid_proxy, convert_proxy_or_proxies


REDIS_CLIENT_VERSION = redis.__version__
IS_REDIS_VERSION_2 = REDIS_CLIENT_VERSION.startswith('2.')


class RedisClient(object):
    """
    redis connection client of proxypool
    """

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB, **kwargs):
        """
        init redis client
        :param host: redis host
        :param port: redis port
        :param password: redis password
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True, **kwargs)

    def add(self, proxy: Proxy, score=PROXY_SCORE_INIT) -> int:
        """
        add proxy and set it to init score
        :param proxy: proxy, ip:port, like 8.8.8.8:88
        :param score: int score
        :return: result
        """
        if not is_valid_proxy(f'{proxy.host}:{proxy.port}'):
            logger.info(f'invalid proxy {proxy}, throw it')
            return
        if not self.exists(proxy):
            if IS_REDIS_VERSION_2:
                return self.db.zadd(REDIS_KEY, score, proxy.string())
            return self.db.zadd(REDIS_KEY, {proxy.string(): score})

    def random(self) -> Proxy:
        """
        get random proxy
        firstly try to get proxy with max score
        if not exists, try to get proxy by rank
        if not exists, raise error
        :return: proxy, like 8.8.8.8:8
        """
        # try to get proxy with max score
        # 获取分数是100的IP
        proxies = self.db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MAX , PROXY_SCORE_MAX)
        if len(proxies):
            return convert_proxy_or_proxies(choice(proxies))
        # else get proxy by rank
        proxies = self.db.zrevrange(REDIS_KEY, PROXY_SCORE_MIN , PROXY_SCORE_MAX)
        if len(proxies):
            return convert_proxy_or_proxies(choice(proxies))
        # else raise error
        raise PoolEmptyException

    def decrease(self, proxy: Proxy) -> int:
        """
        decrease score of proxy, if small than PROXY_SCORE_MIN, delete it
        :param proxy: proxy
        :return: new score
        """
        if IS_REDIS_VERSION_2:
            self.db.zincrby(REDIS_KEY, proxy.string(), -1)
        else:
            # 对当前ip的分数减一分
            self.db.zincrby(REDIS_KEY, -1, proxy.string())
            # 获取当前ip的分数
        score = self.db.zscore(REDIS_KEY, proxy.string())
        logger.info(f'{proxy.string()} score decrease 1, current {score}')
        # 如果分数小于规定值，删除
        if score <= PROXY_SCORE_MIN:
            logger.info(f'{proxy.string()} current score {score}, remove')
            self.db.zrem(REDIS_KEY, proxy.string())

    def exists(self, proxy: Proxy) -> bool:
        """
        if proxy exists
        :param proxy: proxy
        :return: if exists, bool
        """
        # 如果能获取当前ip对应的分数，为True,否则为False
        return not self.db.zscore(REDIS_KEY, proxy.string()) is None

    def max(self, proxy: Proxy) -> int:
        """
        set proxy to max score
        :param proxy: proxy
        :return: new score
        """
        # 如果测试IP可用，则将该ip的值改为100，存入库中
        logger.info(f'{proxy.string()} is valid, set to {PROXY_SCORE_MAX}')
        if IS_REDIS_VERSION_2:
            return self.db.zadd(REDIS_KEY, PROXY_SCORE_MAX, proxy.string())
        return self.db.zadd(REDIS_KEY, {proxy.string(): PROXY_SCORE_MAX})

    def count(self) -> int:
        """
        get count of proxies
        :return: count, int
        """
        # proxies: universal
        # 判断当前数据库里的ip数量
        # 统计有序集合里元素数量的方法
        # {1,2,3}
        #  0 0 1

        return self.db.zcard(REDIS_KEY)

    def all(self) -> List[Proxy]:
        """
        get all proxies
        :return: list of proxies
        """
        # 获取全部代理IP
        return convert_proxy_or_proxies(self.db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX))

        # 遍历有序集合的元素
    def batch(self, cursor, count) -> List[Proxy]:
        """
        get batch of proxies
        :param cursor: scan cursor
        :param count: scan count
        :return: list of proxies
        """
        cursor, proxies = self.db.zscan(REDIS_KEY, cursor, count=count)
        return cursor, convert_proxy_or_proxies([i[0] for i in proxies])


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.random()
    print(result)

