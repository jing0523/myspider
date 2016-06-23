# -*- coding: utf-8 -*-

import scrapy
import urllib2
import BeautifulSoup
from myspider.items import MyspiderItem
from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
import time, datetime
domain_sz = "http://www.stc.gov.cn/"
basic_url = 'http://www.stc.gov.cn/ZWGK/TZGG/GGJG/index'
lastpage = 1


class MyBaseSpider_SZ(BaseSpider):
    name = 'sz1'
    allowed_domains = [domain_sz]
    start_urls = [basic_url + '.htm']
    for p in range(1, lastpage + 1, 1):
        start_urls.append(basic_url + '_' +str(p) + '.htm')

    def __init__(self):
        # private variables for parsing HTML page
        self.flurls = []

    # def geturlContent(self, l):
    #
    #     rp = urllib2.urlopen(l)
    #     content = rp.read()
    #     if content:
    #         rp = BeautifulSoup.BeautifulSoup(content)
    #         return rp.getText()

    """TIMEFILTER : URGENT INCIDENT_ROAD REPAIR EVENT ONLY"""

    def timefilter(self, rptime):
        crtime = datetime.date.today().strftime('%Y_%m_%d')
        if crtime == rptime:  # .replace('_',''):
            return True
        else:
            return False

    def parse(self, response):
        selector = HtmlXPathSelector(response)
        sels = selector.select('//*[@id="mytable"]/tr')

        for sel in sels:
            item = MyspiderItem()
            partial_url = ''.join(sel.xpath('td[2]/a/@href').extract())
            partial_time = ''.join(sel.xpath('td[3]/text()').extract())
            self.displayUrgentEventonly = self.timefilter(partial_time)
            if partial_url:
                _url = basic_url.replace('/index','/')
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
                ecode_title = ''.join(sel.xpath('td[2]/a/@title').extract())

                item['COLLECTDATE'] = datetime.date.today().strftime("%Y-%m-%d")
                item['CONTENT'] = ecode_ctnt.encode('utf-8')
                item['TITLE'] = ecode_title.encode('utf-8')
                item['REF'] = _url
                item['POSTFROM'] = u'网上深圳交警'
                item['POSTDATE'] = partial_time

            if not (self.displayUrgentEventonly):
                yield item
            else:
                continue
