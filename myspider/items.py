# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem_NOTICE(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NOTICE_TITLE = scrapy.Field()
    NOTICE_REF = scrapy.Field()
    NOTICE_DATETIME = scrapy.Field()
    NOTICE_CONTENT = scrapy.Field()
    NOTICE_STATUS = scrapy.Field()


class MyspiderItem_NOTICE2(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()
    COLLECTDATE = scrapy.Field()
    EVENTTYPE = scrapy.Field()
    ROADNAME = scrapy.Field()
    DIRECTION = scrapy.Field()
    START_TIME = scrapy.Field()
    END_TIME = scrapy.Field()
    # regex \d{4}年\d+月\d+日

    CONTENT = scrapy.Field()

    TITLE = scrapy.Field()
    REF = scrapy.Field()
    POSTDATE = scrapy.Field()
    POSTFROM = scrapy.Field()
    STATUS = scrapy.Field()


class MyspiderItem_SH(scrapy.Item):
    NOTICE_ROADNAME = scrapy.Field()
    NOTICE_STOPREASON = scrapy.Field()
    NOTICE_PLANTIME = scrapy.Field()
    NOTICE_PLANTIMEDIS = scrapy.Field()
    NOTICE_DESCRIBE = scrapy.Field()
    showpage = scrapy.Field()
