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

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        dt = datetime.datetime.today().strftime("%Y-%m-%d")
        file = open('%s_products.csv' % (spider.name + '_' + dt), 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ['COLLECTDATE', 'TITLE', 'CONTENT', 'POSTFROM', 'REF', 'POSTDATE']

        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        # todo:re-parse item when exporting
        self.exporter.export_item(item)
        return item
