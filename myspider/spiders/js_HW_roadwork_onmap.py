# -*- coding: utf-8 -*-
import sys

reload(sys)

from myspider.items import MyspiderItem
from scrapy.http import TextResponse

import scrapy
import json, os, sys
import datetime, time


class jsHWApp(scrapy.spiders.Spider):
    name = "jsHWApp"
    allowed_domains = ['218.2.208.140:8091']
    start_urls = [
        'http://218.2.208.140:8091/JSWeb/servlet/custService?key=getLUWSJSSB&traffictype='
    ]

    def event_type_switcher(self, eventTypeID):
        if type(eventTypeID) is unicode:
            _event_type_id = int(eventTypeID)
            switcher = {
                151: u'养护施工',
                115: u'通告',
                131: u'天气受阻-雨',
                134: u'天气受阻-雾',
                121: u'交通事故',
                173: u'紧急事故',
                144: u'断路',
                141: u'断路',
            }

            return switcher.get(_event_type_id, 'NONE')

        return u'无类型'

    def parse(self, response):
        data = json.loads(response.body.decode('gb18030').encode('utf8'))

        strn = datetime.datetime.today().strftime('%Y-%m-%d')
        for case in data[u'LUWSJSSB']:
            item = MyspiderItem()

            item['COLLECTDATE'] = strn

            item['ROADNAME'] = case[u'LUDMC']
            item['POSTFROM'] = u'江苏省交通运输厅'

            item['EVENTTYPE'] = self.event_type_switcher(case[u'SHIJLX'])
            item['DIRECTION'] = case[u'FANGX'] + u"-" + case[u'LUXBSM']
            item['START_TIME'] = case[u'SHIFSJ']
            item['POSTDATE'] = case[u'CHUANGJSJ']
            item['END_TIME'] = case[u'YUJHFSJ']

            item['CONTENT'] = case[u'SHIJNR'].strip().replace('\n', ' ').replace('\r', '')
            item['TITLE'] = (u'locate at x: ' + case[u'X'] + u' Y: ' + case[u'Y']).strip().replace('\n', ' ').replace(
                '\r', '')

            item['REF'] = self.start_urls[0]

            yield item
