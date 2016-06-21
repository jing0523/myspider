from myspider.items import MyspiderItem
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector


class MyBaseSpider_BJ(BaseSpider):
    name = 'bjevent'
    allowed_domains = ['glcx.bjlzj.gov.cn']
    start_urls = [
        'http://glcx.bjlzj.gov.cn/bjglwww/ws/publish/publishEvent/publishEvents'
    ]

    def __init__(self):
        # private variables for parsing HTML page
        self.name = ''

    def parse(self, response):
        from scrapy.http import FormRequest
        form = {}
        url = 'http://glcx.bjlzj.gov.cn/bjglwww/ws/publish/publishEvent/publishEvents'
        r = FormRequest(url, form)
        yield r
        # selector = HtmlXPathSelector(response)
        # sels = selector.select('//*[@id="wuhang"]/ul/li')
        # for sel in sels:
        #     item = MyspiderItem()
        #
        #     partial_url = ''.join(sel.xpath('a/@href').extract())
        #     partial_time = ''.join(sel.xpath('span/text()').extract())
        #
        #     if partial_time:
        #         partial_time = partial_time[1:-1]
        #     if partial_url:
        #         _url = domain_bj
        #         _url += partial_url
        #
        #     # parse following urls content
        #     rp = urllib2.urlopen(_url)
        #     content = rp.read()
        #     lstcontent = []
        #     if content:
        #         rp = BeautifulSoup.BeautifulSoup(content)
        #         text =  rp.findAll("p")
        #         for t in text:
        #             lstcontent.append(t.getText())
        #
        #     ecode_ctnt = (''.join(lstcontent)).strip().replace('&nbsp;','')
        #     ecode_title = ''.join(sel.xpath('a/@title').extract())
        #
        #     item['CONTENT'] = ecode_ctnt.encode('utf-8')
        #     item['TITLE'] = ecode_title.encode('utf-8')
        #     item['REF'] = _url
        #     item['POSTDATE'] = partial_time

        # yield item
        #
