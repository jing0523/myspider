# -*- coding: utf-8 -*-
from myspider.items import MyspiderItem
from scrapy.selector import HtmlXPathSelector
import scrapy
import datetime


class bjHWNews(scrapy.spiders.BaseSpider):
    name = 'bjevent2'
    allowed_domains = ['www.bj96011.com']
    start_urls = [
        'http://www.bj96011.com/action.php?type=chuxingxinxi'  #referer
    ]

    def parse(self, response):
        selector = HtmlXPathSelector(response)
        sels = selector.select('//*[@class="road_one"]')
        for sel in sels:
            item = MyspiderItem()

            roadname = ''.join(sel.xpath('div[@class="road_one_title"]/span[1]/text()').extract())
            event_type = ''.join(sel.xpath('div[@class="road_one_title"]/span[2]/text()').extract())
            occtime = ''.join(sel.xpath('div[@class="road_one_title"]/span[3]/text()').extract())
            info = ''.join(sel.xpath('div[@class="road_info"]/p[1]/text()').extract())
            partial_url = ''.join(sel.xpath('div[@class="road_info"]/p[2]/a/@href').extract())

            encode_ctnt = info.strip().replace('\n', '').replace('\r', '').encode('utf-8')
            _url = self.allowed_domains[0] + '/' + partial_url
            roadname = roadname.encode('utf-8')
            event_type = event_type.encode('utf-8')
            _title = roadname + event_type

            item['CONTENT'] = encode_ctnt
            item['ROADNAME'] = roadname
            item['EVENTTYPE'] = event_type
            item['TITLE'] = _title
            item['REF'] = _url
            item['POSTDATE'] = occtime
            item['START_TIME'] = occtime
            item['COLLECTDATE'] = datetime.datetime.now()
            item['POSTFROM'] = u'首发高速出行网'

            yield item