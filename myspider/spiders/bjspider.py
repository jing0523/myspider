# -*- coding: utf-8 -*-

import scrapy
import urllib2
import BeautifulSoup
import datetime
from myspider.items import MyspiderItem_NOTICE
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

domain_bj = "http://bjjtgl.gov.cn"
basic_url = 'http://www.bjjtgl.gov.cn/jgj/jttg/7711-'


class MyBaseSpider_BJ(BaseSpider):
    name = 'bj1'
    allowed_domains = [domain_bj]
    start_urls = [
        'http://www.bjjtgl.gov.cn/jgj/jttg/7711-1.html',
        'http://www.bjjtgl.gov.cn/jgj/jttg/7711-2.html',
        'http://www.bjjtgl.gov.cn/jgj/jttg/7711-3.html'
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
            item = MyspiderItem_NOTICE()

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

            item['NOTICE_CONTENT'] = ecode_ctnt.encode('utf-8')
            item['NOTICE_TITLE'] = ecode_title.encode('utf-8')
            item['NOTICE_REF'] = _url
            item['NOTICE_DATETIME'] = partial_time

            yield item
