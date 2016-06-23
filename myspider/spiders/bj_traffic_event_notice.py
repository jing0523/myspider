# -*- coding: utf-8 -*-

import scrapy
import urllib2
import BeautifulSoup
import datetime
from myspider.items import MyspiderItem
from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector

domain_bj = "http://bjjtgl.gov.cn"
basic_url = 'http://www.bjjtgl.gov.cn/jgj/jttg/7711-'


class MyBaseSpider_BJ(BaseSpider):
    name = 'bj1'
    allowed_domains = [domain_bj]
    start_urls = [
        'http://www.bjjtgl.gov.cn/jgj/jttg/7711-1.html',

    ]

    def __init__(self):
        # private variables for parsing HTML page
        self.flurls = []


    def timefilter(self, rptime):

        crtime = datetime.date.today().strftime('%Y-%m-%d')
        if crtime == rptime:  # .replace('_',''):
            return True
        else:
            return False

    def parse(self, response):
        selector = HtmlXPathSelector(response)
        sels = selector.select('//*[@id="wuhang"]/ul/li')
        for sel in sels:
            item = MyspiderItem()

            partial_url = ''.join(sel.xpath('a/@href').extract())
            partial_time = ''.join(sel.xpath('span/text()').extract())

            if partial_time:
                partial_time = partial_time[1:-1]
            if partial_url:
                _url = domain_bj
                _url += partial_url

            # parse following urls content
            rp = urllib2.urlopen(_url)
            content = rp.read()
            lstcontent = []
            if content:
                rp = BeautifulSoup.BeautifulSoup(content)
                text =  rp.findAll("p")
                for t in text:
                    lstcontent.append(t.getText())

            ecode_ctnt = (''.join(lstcontent)).strip().replace('&nbsp;','')
            ecode_title = ''.join(sel.xpath('a/@title').extract())
            # ['STATUS', 'ID', 'COLLECTDATE', 'EVENTTYPE', 'ROADNAME'
            #     , 'DIRECTION', 'START_TIME', 'END_TIME', 'CONTENT', 'TITLE', 'REF', 'POSTDATE', 'POSTFROM'
            #  ]
            # item['NOTICE_CONTENT'] = ecode_ctnt.encode('utf-8')
            # item['NOTICE_TITLE'] = ecode_title.encode('utf-8')
            # item['NOTICE_REF'] = _url
            # item['NOTICE_DATETIME'] = partial_time
            item['CONTENT'] = ecode_ctnt.encode('utf-8')
            item['TITLE'] = ecode_title.encode('utf-8')
            item['REF'] = _url
            item['POSTDATE'] = partial_time
            item['COLLECTDATE'] = datetime.datetime.now()
            item['POSTFROM'] = u'北京市公安局公安交通管理局通告'

            yield item
