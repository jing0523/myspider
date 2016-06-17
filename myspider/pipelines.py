# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime, time
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter


class MyspiderPipeline(object):
    def __init__(self):
        # self.file = codecs.open("data.json", encoding="utf-8", mode="wb")
        pass
    def process_item(self, item, spider):
        pass

class CSVPipeline(object):

    def __init__(self):
        self.files = {}

    # Rules - switchers
    def from_spider_to_fields(self, spider):
        public_fields = ['STATUS', 'ID', 'COLLECTDATE', 'EVENTTYPE', 'ROADNAME'
            , 'DIRECTION', 'START_TIME', 'END_TIME', 'CONTENT', 'TITLE', 'REF', 'POSTDATE', 'POSTFROM'
                         ]
        switcher = {
            'sz1': ['POSTDATE', 'COLLECTDATE', 'TITLE', 'CONTENT', 'POSTFROM', 'REF'],
            'bj1': public_fields
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
        dt = datetime.datetime.today().strftime("%Y-%m-%d")
        file = open('%s.csv' % (spider.name + '_' + dt), 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)

        self.exporter.fields_to_export = self.from_spider_to_fields(spider)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        # todo: check export options

        from optionclass import DataParser
        from optionclass import ExportOptions
        parser = DataParser()
        parser.setRules(spider)
        item['START_TIME'] = parser.check_fill_st(item['CONTENT'])
        item['END_TIME'] = parser.check_fill_ed(item['CONTENT'])
        # item['STATUS'] =  None#self.check_status(item)


        self.exporter.export_item(item)
        return item
