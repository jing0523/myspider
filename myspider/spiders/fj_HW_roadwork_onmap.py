# -*- coding: utf-8 -*-
from scrapy.http import FormRequest
from myspider.items import MyspiderItem

import scrapy
import json, codecs, os, sys
import datetime, time


class fjHWApp(scrapy.spiders.Spider):
    name = "fjHWApp"
    allowed_domains = ['appserver.fjgsgl.cn']
    start_urls = [
        'http://appserver.fjgsgl.cn/NewFJGSWechatAPIServer/index.php/userautoserver/showtrafficinfo?tab=1',  #
        # 路名-非必要

    ]

    response_id_map = {}
    page = -1

    def parse(self, response):
        yield FormRequest(
            url='http://appserver.fjgsgl.cn/NewFJGSWechatAPIServer/index.php/userautoserver/c007',
            method='POST',
            formdata={'roadlineid': '0', 'eventtype': '1006001', 'pageid': '0'}, dont_filter=True,
            callback=self.event_data_parse

        )

        yield FormRequest(
            url='http://appserver.fjgsgl.cn/NewFJGSWechatAPIServer/index.php/userautoserver/c007',
            method='POST',
            formdata={'roadlineid': '0', 'eventtype': '1006002', 'pageid': '0'}, dont_filter=True,
            callback=self.roadwork_data_parse

        )

    def event_data_parse(self, response):

        jdata = json.loads(response.body)
        events = jdata[u'data']

        for event in events:
            item = MyspiderItem()
            enc_event_text = event[u'remark'].strip().replace('\n', ' ').replace('\r', '').encode('utf-8')

            X = event[u'coor_x']
            Y = event[u'coor_y']

            if len(event) < 1:  # null-checking
                continue

            item['ID'] = event[u'eventid']
            item['POSTFROM'] = u'福建高速公路'
            item['CONTENT'] = enc_event_text
            item['TITLE'] = u'LOCATION AT {' + str(Y) + u' ,' + str(X) + u'}'
            item['DIRECTION'] = (event[u'occplace'] + event[u'startnodename'] + u'-' + event[u'endnodename']).encode(
                'utf-8')
            item['POSTDATE'] = (event[u'intime']).encode('utf-8')
            item['EVENTTYPE'] = u'交通事件'
            item['START_TIME'] = (event[u'occtime']).encode('utf-8')
            item['END_TIME'] = (event[u'planovertime'])
            item['COLLECTDATE'] = datetime.datetime.today().strftime('%Y-%m-%d')
            item['REF'] = self.start_urls[0]
            yield item

    def roadwork_data_parse(self, response):
        jdata = json.loads(response.body)
        events = jdata[u'data']

        for event in events:
            item = MyspiderItem()
            enc_event_text = event[u'remark'].strip().replace('\n', ' ').replace('\r', '').encode('utf-8')

            X = event[u'coor_x']
            Y = event[u'coor_y']

            if len(event) < 1:  # null-checking
                continue

            item['ID'] = event[u'eventid']
            item['POSTFROM'] = u'福建高速公路'
            item['CONTENT'] = enc_event_text
            item['TITLE'] = u'LOCATION AT {' + str(Y) + u' ,' + str(X) + u'}'
            item['DIRECTION'] = (event[u'occplace'] + event[u'startnodename'] + u'-' + event[u'endnodename']).encode(
                'utf-8')
            item['POSTDATE'] = (event[u'intime']).encode('utf-8')
            item['EVENTTYPE'] = u'路况施工'
            item['START_TIME'] = (event[u'occtime']).encode('utf-8')
            item['END_TIME'] = (event[u'planovertime'])
            item['COLLECTDATE'] = datetime.datetime.today().strftime('%Y-%m-%d')
            item['REF'] = self.start_urls[0][-1:] + '4'
            yield item
