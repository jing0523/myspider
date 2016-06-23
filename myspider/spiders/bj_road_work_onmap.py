# -*- coding: utf-8 -*-
from myspider.items import MyspiderItem
from scrapy.http import Request
import scrapy
import json, codecs, os, sys
import datetime, time


class bjRoadWorkOnMap(scrapy.spiders.Spider):
    name = 'bjevent'
    allowed_domains = ['glcx.bjlzj.gov.cn']
    start_urls = [
        'http://glcx.bjlzj.gov.cn/bjglwww/index.shtml'
    ]
    def parse(self, response):
        yield Request(
                url="http://glcx.bjlzj.gov.cn/bjglwww/ws/publish/publishEvent/publishEvents",
                method="POST",
            cookies={'JSESSIONID': 'AE0E5EE2F39355DE399BE9B9CB258E21',
                     '_gscu_813094265': '63640433yb4sh416'},
                callback=self.fill_in_items)

    def fill_in_items(self, response):
        # parse json and fill them into items

        item = MyspiderItem()
        data = json.loads(response.body)
        real_data = data[u'roadEvents'][u'roadEvents']
        strnow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for row in real_data:
            item['ID'] = row[u'eventId']
            item['ROADNAME'] = row[u'roadName'].encode('utf-8')
            item['COLLECTDATE'] = strnow
            item['EVENTTYPE'] = row[u'eventType']
            item['DIRECTION'] = row[u'dealCase'].encode('utf-8')
            item['EVENTTYPE'] = row[u'eventType']

            item['START_TIME'] = row[u'occurTime']
            item['END_TIME'] = row[u'endTime']

            item['CONTENT'] = row[u'description'].strip().replace('\n', ' ').replace('\r', '').encode('utf-8')
            item['TITLE'] = (row[u'roadName'] + u'-location at: ' + row[u'lonlatData']).encode('utf-8')
            item['POSTDATE'] = strnow
            item['POSTFROM'] = u'北京市路政局公路出行信息服务站'
            item['REF'] = 'http://glcx.bjlzj.gov.cn/bjglwww/index.shtml'
            yield item
