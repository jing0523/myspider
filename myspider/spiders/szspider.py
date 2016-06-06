import scrapy
import urllib2
import BeautifulSoup
from myspider.items import MyspiderItem
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

domain_sz = "http://www.stc.gov.cn/"
basic_url = 'http://www.stc.gov.cn/ZWGK/TZGG/GGJG/index'
lastpage = 3


class MyBaseSpider(BaseSpider):
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

    def parse(self, response):
        selector = HtmlXPathSelector(response)
        sels = selector.select('//*[@id="mytable"]/tr')
        for sel in sels:
            item = MyspiderItem()

            partial_url = ''.join(sel.select('td[2]/a/@href').extract())
            partial_time = ''.join(sel.select('td[3]/text()').extract())

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
                ecode_title = ''.join(sel.select('td[2]/a/@title').extract())

                item['NOTICE_CONTENT'] = ecode_ctnt.encode('utf-8')

                item['NOTICE_TITLE'] = ecode_title.encode('utf-8')
                item['NOTICE_REF'] = _url
                item['NOTICE_DATETIME'] = partial_time

            yield item
