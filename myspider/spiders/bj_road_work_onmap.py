# -*- coding: utf-8 -*-
from myspider.items import MyspiderItem
from scrapy.spider import Spider
from scrapy.http import FormRequest
import scrapy
import json, codecs, os, sys
import datetime, time


class MyBaseSpider_BJOnMap(Spider):
    name = 'bjevent'
    allowed_domains = ['glcx.bjlzj.gov.cn']

    def parse(self, response):
        for i in range(0, 1):
            yield FormRequest(
                url="http://glcx.bjlzj.gov.cn/bjglwww/ws/publish/publishEvent/publishEvents",
                method="POST",
                formdata={},
                callback=self.fill_in_items)

    # def start_requests(self):
    #     return [scrapy.http.FormRequest(
    #         'http://glcx.bjlzj.gov.cn/bjglwww/ws/publish/publishEvent/publishEvents',
    #         formdata=None,
    #         callback=self.fill_in_items
    #     )]
    def fill_in_items(self, response):
        # parse json and fill them into items

        item = MyspiderItem()
        data = json.loads(response.body)
        real_data = data['roadEvents']
        strnow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for row in real_data:
            item['ID'] = row['eventId']
            item['ROADNAME'] = row['roadName']
            item['COLLECTDATE'] = datetime.datetime.today().strftime('%Y-%m-%d')
            item['EVENTTYPE'] = row['eventType']
            item['DIRECTION'] = row['dealCase']
            item['EVENTTYPE'] = row['eventType']

            item['START_TIME'] = row['occurTime']
            item['END_TIME'] = row['endTime']

            item['CONTENT'] = row['description']
            item['TITLE'] = row['roadName'] + u'-location at: ' + row['lonlatData']
            item['POSTDATE'] = strnow
            item['POSTFROM'] = u'北京市路政局公路出行信息服务站'
            item['REF'] = 'http://glcx.bjlzj.gov.cn/bjglwww/index.shtml'
            yield item
