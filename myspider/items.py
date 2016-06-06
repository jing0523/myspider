# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NOTICE_TITLE = scrapy.Field()
    NOTICE_REF = scrapy.Field()
    NOTICE_DATETIME = scrapy.Field()
    NOTICE_CONTENT = scrapy.Field()
class MySubspiderItem(scrapy.Item):
    NOTICE_CONTENT = scrapy.Field()
    NOTICE_STIME = scrapy.Field()
    NOTICE_ETIME = scrapy.Field()
    NOTICE_ID = scrapy.Field()
    NOTICE_POSTTIME = scrapy.Field()
