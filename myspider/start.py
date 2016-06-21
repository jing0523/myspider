# -*- coding: utf-8 -*-
'''Run Scrapy Spider in Cmdline todo: run scrapy in a script'''

# done:runs multiple spiders simultaneously

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.bj_traffic_event_notice import MyBaseSpider_BJ
from spiders.bj_road_work_onmap import MyBaseSpider_BJOnMap
from spiders.GooglePlaySpider import googleAppSpider
from spiders.sz_traffic_event_notice import MyBaseSpider_SZ
from spiders.zj_HW_roadwork_news import zjfHWApp
import sys

# add 2 mode : retrieve history - 保留过期数据 ACTIVE 进行上线， OVERDUE 筛选施工完毕信息
# add 2 mode : update new - random capture 不保留过期数据
# def main(m):
pip = get_project_settings()

process = CrawlerProcess(pip)
# process.crawl(MyBaseSpider_BJ())
# process.crawl(googleAppSpider())
# process.crawl(MyBaseSpider_BJOnMap())
# process.crawl(MyBaseSpider_SZ())
process.crawl(zjfHWApp())
process.start()


# if __name__ == "__main__":
#     mode = raw_input('PLEASE ENTR MODE -1 : REMAIN HISTORY DATA;-0 UPDATE NEW DATA ONLY')
#     sys.exit(main(mode))
