from myspider.items import MyspiderItem
from scrapy.spider import BaseSpider
import scrapy
import json, codecs, os, sys
import datetime, time


class MyBaseSpider_BJ(BaseSpider):
    name = 'bjevent'
    allowed_domains = ['glcx.bjlzj.gov.cn']
    start_urls = [
        'http://glcx.bjlzj.gov.cn/bjglwww/ws/publish/publishEvent/publishEvents'
    ]

    def __init__(self):
        # private variables for parsing HTML page
        self.name = ''

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={},
            callback=self.fill_in_items
        )

    def fill_in_items(self, response):
        # parse json and fill them into items
        item = MyspiderItem()
        data = json.loads(response.body)
        real_data = data['roadEvents']

        for row in real_data:
            yield item
