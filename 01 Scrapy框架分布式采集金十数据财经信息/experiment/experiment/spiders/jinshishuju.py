import json
import scrapy
from scrapy_redis.spiders import RedisSpider
from experiment.items import JinshishujuItem


class JinshishujuSpider(RedisSpider):
    name = "jinshishuju"
    redis_key = "jinshishuju:start_urls"

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
        'ROBOTSTXT_OBEY': False,
        'ITEM_PIPELINES': {
            'experiment.pipelines.MySQLPipeline': 300,
        },
        'SCHEDULER': 'scrapy_redis.scheduler.Scheduler',
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
        'SCHEDULER_PERSIST': True,
        'REDIS_HOST': '43.143.173.241',
        'REDIS_PORT': 6379,
        'REDIS_PARAMS': {
            'password': '123456',
            'db': 1,
            'decode_responses': False
        },
        'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.SpiderQueue',
        'DOWNLOAD_TIMEOUT': 15,  # 设置请求超时
        'RETRY_TIMES': 3,  # 重试次数
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "origin": "https://rili.jin10.com",
        "referer": "https://rili.jin10.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "x-app-id": "sKKYe29sFuJaeOCJ",
        "x-version": "2.0"
    }

    def start_requests(self):
        while True:
            url = self.server.lpop(self.redis_key)
            if not url:
                break
            if isinstance(url, bytes):
                url = url.decode('utf-8')
            self.logger.info(f"开始请求URL: {url}")
            print('-----------------------------------')
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response, **kwargs):
        self.logger.info(f"响应状态码: {response.status}，URL: {response.url}")
        if response.status != 200:
            self.logger.warning(f"非200响应，跳过: {response.status}")
            return
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {e}，内容片段: {response.text[:200]}")
            return
        data_dict = data.get('data', [])
        if not data_dict:
            self.logger.warning(f"接口未返回数据，URL: {response.url}")
            return

        for i in data_dict:
            item = JinshishujuItem()
            item['time'] = i.get('actual_time') or '时间数据为空'

            country = i.get('country') or ''
            time_period = i.get('time_period') or ''
            indicator_name = i.get('indicator_name') or ''
            item['data'] = country + time_period + indicator_name or '数据为空'

            star_map = {1: '很低', 2: '低', 3: '中', 4: '高', 5: '很高'}
            item['importance'] = star_map.get(i.get('star'), '重要性为空')

            item['previous'] = (i.get('previous') + '%') if i.get('previous') else '前值为空'
            item['consensus'] = (i.get('consensus') + '%') if i.get('consensus') else '预测值为空'
            item['actual'] = (i.get('actual') + '%') if i.get('actual') else '公布值为空'

            yield item