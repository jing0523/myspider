# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from myspider.items import MyspiderItem

import scrapy
import json, codecs, os, sys
import datetime, time


class zjfHWApp(Spider):
    name = "zjHWApp"
    allowed_domains = ['app.zjzhgs.com']
    start_urls = [
        'http://app.zjzhgs.com/MQTTWechatAPIServer/businessserver/getTrafficByRoad',
        'http://app.zjzhgs.com/MQTTWechatAPIServer/businessserver/loadAllroad'
    ]
    map = {}

    # '''
    #     Method：-
    #     parse                        -Request        show all road list and id
    #     get_road_mapping             -json/dict      road name and id mapping dict
    #     dataparse                    -Item/dict      return Items can be exported through out pipelinetool

    # '''
    def parse(self, response):
        yield Request(
            url='http://app.zjzhgs.com/MQTTWechatAPIServer/businessserver/loadAllroad',
            method="POST",
            dont_filter=True,
            callback=self.get_road_mapping)

    def get_road_mapping(self, response):
        item = MyspiderItem()
        data = json.loads(response.body)
        for r in data["data"]:
            rdname = r[u'shortname']
            rdid = int(r[u'roadoldid'])
            self.map.update({rdid: rdname})
        for i in self.map.keys():
            item['ID'] = int(i)
            item['ROADNAME'] = self.map[int(i)]
            # yield FormRequest(
            #     url="http://app.zjzhgs.com/MQTTWechatAPIServer/businessserver/getTrafficByRoad",
            #     method="POST",
            #     formdata={'roadoldid': str(i)}, dont_filter=True,

            yield item



            # def data_parse(self,response):
            #     print json.loads(response.body_as_unicode)
