# -*- coding: utf-8 -*-
import scrapy
import urllib2
import BeautifulSoup
from myspider.items import MyspiderItem
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

import time, datetime
domain_bj = "http://www.btic.org.cn/xxzx/jtxxfw/cxts/"
basic_url = 'http://www.btic.org.cn/xxzx/jtxxfw/cxts/index'
lastpage = 5


# todo: wei.fm.1039代替
class MyBaseSpider_BJ_U1(BaseSpider):
    name = 'bj2'
    allowed_domains = [domain_bj]
    start_urls = [basic_url + '.htm']
    for p in range(1, lastpage + 1, 1):
        start_urls.append(basic_url + '_' + str(p) + '.htm')

    def __init__(self):
        # private variables for parsing HTML page
        self.flurls = []
        self.kwdictionary = {"InProcess": ["发生故障", "临时交通管制", "采取临时", "进行", "占道施工"],
                             "Completed": ["结束", "恢复", "恢复正常", "完毕", "处理完毕", "修复完毕", "故障车离开", "管制结束", "施工结束"],
                             "InPlanning": []
                             }
        self.displayUrgentEventonly = False
        """TIMEFILTER : URGENT INCIDENT_ROAD REPAIR EVENT ONLY"""

    def timefilter(self, rptime):
        crtime = datetime.date.today().strftime('%Y-%m-%d')
        if crtime == rptime:  # .replace('_',''):
            return True
        else:
            return False



    def classifyWord(self, title):
        d = self.kwdictionary
        cl = ''
        if d and len(title) > 0:
            for key in d:
                for v in d[key]:
                    if title.find(v) > -1:
                        cl = key
                        break
        return cl
    def parse(self, response):
        selector = HtmlXPathSelector(response)
        sels = selector.select('//div[@class="fzdt_con"]/dl')
        for sel in sels:

            item = MyspiderItem_NOTICE()
            partial_url = ''.join(sel.xpath('dd/a/@href').extract())
            partial_time = ''.join(sel.xpath('dt/text()').extract())

            if partial_time:
                partial_time = "2016-" + partial_time
                #     apply time filter
                displayUrgentEventonly = self.timefilter(partial_time)

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
            ecode_title = ''.join(sel.xpath('dd/a/@title').extract())

            # item['NOTICE_CONTENT'] = ecode_ctnt.encode('utf-8')
            # item['NOTICE_TITLE'] = ecode_title.encode('utf-8')
            # item['NOTICE_REF'] = _url
            # item['NOTICE_DATETIME'] = partial_time
            # item['NOTICE_STATUS'] = self.classifyWord(item['NOTICE_TITLE'])

            # if (displayUrgentEventonly):
            yield item
