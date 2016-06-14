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
        public_fields = ['ID', 'COLLECTDATE', 'EVENTTYPE', 'ROADNAME'
            , 'DIRECTION', 'START_TIME', 'END_TIME', 'CONTENT', 'TITLE', 'REF', 'POSTDATE', 'POSTFROM'
            , '_STATUS']
        switcher = {
            'sz1': ['POSTDATE', 'COLLECTDATE', 'TITLE', 'CONTENT', 'POSTFROM', 'REF'],
            'bj1': ['NOTICE_DATETIME', 'NOTICE_TITLE', 'NOTICE_REF', 'NOTICE_CONTENT'],
        }
        return switcher.get(spider.name, 'NONE')

    # todo:spider - based - filtering options
    def item_filtering_options(self, spider):
        # todo:filter all events still active, add flag
        # define funciton returns group of arguments/  parser.add_option("-c", action="store_true", default=False, help='Produce a context format diff (default)')
        pass



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

        # todo:re-parse item when exporting
        # todo:filter all events still active, add flag
        # todo:def function to set categories -move to pipeline.py - bjurgent
        self.exporter.export_item(item)
        return item
