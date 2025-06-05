# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JinshishujuItem(scrapy.Item):
    time = scrapy.Field()
    data = scrapy.Field()
    importance = scrapy.Field()
    previous = scrapy.Field()
    consensus = scrapy.Field()
    actual = scrapy.Field()
