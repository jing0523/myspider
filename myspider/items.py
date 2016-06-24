# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# add still active flag
class MyspiderItem_NOTICE(scrapy.Item):
    pass
class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    STATUS = scrapy.Field()
    ID = scrapy.Field()
    COLLECTDATE = scrapy.Field()
    EVENTTYPE = scrapy.Field()
    ROADNAME = scrapy.Field()
    DIRECTION = scrapy.Field()
    START_TIME = scrapy.Field()
    END_TIME = scrapy.Field()
    CONTENT = scrapy.Field()
    TITLE = scrapy.Field()
    REF = scrapy.Field()
    POSTDATE = scrapy.Field()
    POSTFROM = scrapy.Field()
