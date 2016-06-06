import scrapy
import urllib2
import BeautifulSoup
from myspider.items import MyspiderItem
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

domain_bj = "http://www.btic.org.cn/xxzx/jtxxfw/cxts/"
basic_url = 'http://www.btic.org.cn/xxzx/jtxxfw/cxts/index'
lastpage = 10

class MyBaseSpider(BaseSpider):
    name = 'bj2'
    allowed_domains = [domain_bj]
    start_urls = [basic_url + '.htm']
    for p in range(1, lastpage + 1, 1):
        start_urls.append(basic_url + '_' + str(p) + '.htm')

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
        sels = selector.select('//div[@class="fzdt_con"]/dl')
        for sel in sels:
            item = MyspiderItem()

            partial_url = ''.join(sel.select('dd/a/@href').extract())
            partial_time = ''.join(sel.select('dt/text()').extract())

            if partial_time:
                partial_time = "2016_" + partial_time.replace("-","_")

            #     time filter
            if partial_url:
                partial_url = partial_url[9:-4]
                _url = domain_bj
                _url += partial_url
                _url += '.htm'
            # parse following urls content
            rp = urllib2.urlopen(_url)
            content = rp.read()
            lstcontent = []
            if content:
                rp = BeautifulSoup.BeautifulSoup(content)
                text =  rp.findAll("div",{"class":"article"})
                for t in text:
                    lstcontent.append(t.getText())

            ecode_ctnt = (''.join(lstcontent)).strip().replace('&nbsp;','')
            ecode_title = ''.join(sel.select('dd/a/@title').extract())

            item['NOTICE_CONTENT'] = ecode_ctnt.encode('utf-8')
            item['NOTICE_TITLE'] = ecode_title.encode('utf-8')
            item['NOTICE_REF'] = _url
            item['NOTICE_DATETIME'] = partial_time

            yield item
