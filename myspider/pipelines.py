# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime, time
from scrapy import signals
from scrapy.exporters import CsvItemExporter


class CSVPipeline(object):

    def __init__(self):
        self.files = {}

    # Rules - switchers
    def from_spider_to_fields(self, spider):
        public_fields = ['STATUS', 'ID', 'COLLECTDATE', 'EVENTTYPE', 'ROADNAME'
            , 'DIRECTION', 'START_TIME', 'END_TIME', 'CONTENT', 'TITLE', 'REF', 'POSTDATE', 'POSTFROM'
                         ]

        light_public_fields = []
        switcher = {
            'sz1': public_fields,
            'bj1': public_fields,
            'nj1': public_fields,
            'bjevent': public_fields,
            'bjevent2': public_fields,
            'zjHWApp': public_fields,
            'jsHWApp': public_fields,
            'fjHWApp': public_fields,

        }

        return switcher.get(spider.name, 'NONE')

    def check_status(self, item):
        from datetime import datetime
        td = datetime.today()
        sdate = min(item['START_TIME'], item['POSTDATE'])
        enddate = item['END_TIME']
        dt2 = datetime.strptime(sdate, '%Y-%m-%d %H:%M')
        dt3 = datetime.strptime(enddate, '%Y-%m-%d %H:%M')

        if (dt2 < td and dt3 > td):
            return 'ACTIVE'
        return 'OVERDUE'

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        # for all spiders
        dt = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        file = open('%s.csv' % (spider.name + '_' + dt), 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)

        self.exporter.fields_to_export = self.from_spider_to_fields(spider)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        # for all spiders
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):

        from optionclass import DataParser
        from optionclass import ExportOptions

        parser = DataParser()
        parser.setRules(spider)
        # add menu selections for either use spider setting or pipeline tools for generating date
        if spider.name in ['sz1',
                           'bj1',
                           'nj1',
                           'bjevent',
                           'bjevent',
                           'zjHWApp',
                           ]:
            item['START_TIME'] = parser.check_fill_st(item['CONTENT'])
            item['END_TIME'] = parser.check_fill_ed(item['CONTENT'])
            item['STATUS'] = None  # self.check_status(item)
        self.exporter.export_item(item)
        return item


        # todo: use duplicates filter
        # from scrapy.exceptions import DropItem
        #
        # class DuplicatesPipeline(object):
        #
        #     def __init__(self):
        #         self.ids_seen = set()
        #
        #     def process_item(self, item, spider):
        #         if item['id'] in self.ids_seen:
        #             raise DropItem("Duplicate item found: %s" % item)
        #         else:
        #             self.ids_seen.add(item['id'])
        #             return item
