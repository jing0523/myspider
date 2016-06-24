# -*- coding: utf-8 -*-

import scrapy
import urllib2
import datetime
from myspider.items import MyspiderItem
from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector

basic_url_tg = 'http://www.njjg.gov.cn/www/njjg/jgxx2'
basic_url_sg = 'http://www.njjg.gov.cn/www/njjg/jgxx4'


class MyBaseSpider_NJ(BaseSpider):
    name = 'nj1'
    allowed_domains = ["www.njjg.gov.cn"]
    start_urls = [
        basic_url_tg + '.htm',
        basic_url_sg + '.htm'
    ]

    for i in range(1, 4):
        start_urls.append(basic_url_tg + '_p' + str(i) + '.htm')
    for i in range(1, 2):
        start_urls.append(basic_url_sg + '_p' + str(i) + '.htm')

    def __init__(self):
        # private variables for parsing HTML page
        self.flurls = []

    def parse(self, response):
        selector = HtmlXPathSelector(response)
        sels = selector.xpath('//tr/td/div/a[@class="t6"]')
        for sel in sels:

            item = MyspiderItem()

            partial_url = ''.join(sel.xpath('@href').extract())
            _title = '.join('.join(sel.xpath('text()').extract())
            if len(_title) < 1:
                continue
            _url = 'http://www.njjg.gov.cn/www/njjg/'
            _url += partial_url
            # parse following urls content
            rp = urllib2.urlopen(_url)
            content = rp.read()
            lstcontent = []
            txtsource = ''
            if content:
                import BeautifulSoup
                rp = BeautifulSoup.BeautifulSoup(content)
                text = rp.findAll("p")
                source = rp.findAll("br")
                for t in text:
                    lstcontent.append(t.getText())
                txtsource = ''.join([t.getText() for t in source])

            ecode_ctnt = (''.join(lstcontent)).strip().replace('&nbsp;', '')

            item['CONTENT'] = ecode_ctnt.encode('utf-8')
            item['TITLE'] = _title.encode('utf-8')
            item['REF'] = _url
            item['COLLECTDATE'] = datetime.datetime.today().strftime('%Y-%m-%d')
            item['POSTFROM'] = u'南京交管在线'

            yield item
