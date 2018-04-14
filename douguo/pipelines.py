# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from douguo.items import DouguoTypeItem
from douguo.items import DouguoItem
from douguo.items import DouguoAuthorItem

class DouguoPipeline(object):
    def __init__(self):
        self.fileType = open("fileType.json", "w")
        self.fileItem = open("fileItem.json", "w")
        self.fileAuthor = open("fileAuthor.json", "w")

    def process_item(self, item, spider):
        if type(item) == DouguoTypeItem:
            content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.fileType.write(content)

        if type(item) == DouguoItem:
            content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.fileItem.write(content)

        if type(item) == DouguoAuthorItem:
            content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.fileAuthor.write(content)

        return item

    def closs_spidr(self, spider):
        self.fileType.close()
        self.fileItem.close()
        self.fileAuthor.close()