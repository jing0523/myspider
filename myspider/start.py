# -*- coding: utf-8 -*-
'''Run Scrapy Spider in Cmdline todo: run scrapy in a script'''

# done:runs multiple spiders simultaneously

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.bjspider import MyBaseSpider_BJ
from spiders.bjspider_urgent import MyBaseSpider_BJ_U1
from spiders.szspider import MyBaseSpider_SZ

pip = get_project_settings()

process = CrawlerProcess(pip)
process.crawl(MyBaseSpider_BJ())

process.crawl(MyBaseSpider_SZ())

process.start()
