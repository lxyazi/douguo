# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from douguo.items import DouguoTypeItem
from douguo.items import DouguoItem
from douguo.items import DouguoAuthorItem
import os
import pandas as pd
import csv
import re


class DouguoPipeline(object):
    def __init__(self):
        if os.path.exists("fileType.csv"):
            os.remove("fileType.csv")
        if os.path.exists("fileType.csv"):
            os.remove("fileAuthor.csv")
        if os.path.exists("fileType.csv"):
            os.remove("fileItem.csv")
        self.fileType = open("fileType.csv", "w", newline='')
        self.fileItem = open("fileItem.csv", "w", newline='')
        self.fileAuthor = open("fileAuthor.csv", "w", newline='')
        typeFieldNames = ['catesListInfo', 'catesList', 'catesListHref']
        itemFieldNames = ['peopleNumber', 'collectionNumber', 'description', 'recipeIngredient', 'step', 'tip', 'href',
                          'title', 'typeTitle', 'difficulty', 'timeAssume', 'author', 'numOfComments',
                          'authorOfComments']
        authorFieldNames = ['authorName', 'authorUrl', 'authorLocation', 'authorCollectionNumber', 'authorCollection']
        self.typeWriter = csv.DictWriter(self.fileType, fieldnames=typeFieldNames)
        self.itemWriter = csv.DictWriter(self.fileItem, fieldnames=itemFieldNames)
        self.authorWriter = csv.DictWriter(self.fileAuthor, fieldnames=authorFieldNames)
        self.typeWriter.writeheader()
        self.itemWriter.writeheader()
        self.authorWriter.writeheader()

    def process_item(self, item, spider):
        if type(item) == DouguoTypeItem:
            self.typeWriter.writerow(dict(item))

        if type(item) == DouguoItem:
            self.itemWriter.writerow(dict(item))


        if type(item) == DouguoAuthorItem:
            self.authorWriter.writerow(dict(item))

        return item

    def valueProcess(self, stirng):
        str = stirng.replace('，', '').replace('*', '').replace('。', '')
        regex = '（.*?）'
        result, number = re.subn(regex, '', str)
        return result

# class DouguoPipeline(object):
#     def __init__(self):
#         if os.path.exists("fileType.json"):
#             os.remove("fileType.json")
#         if os.path.exists("fileType.json"):
#             os.remove("fileAuthor.json")
#         if os.path.exists("fileType.json"):
#             os.remove("fileItem.json")
#         self.fileType = open("fileType.json", "w")
#         self.fileItem = open("fileItem.json", "w")
#         self.fileAuthor = open("fileAuthor.json", "w")
#         self.fileType.write('[')
#         self.fileItem.write('[')
#         self.fileAuthor.write('[')
#
#     def process_item(self, item, spider):
#         if type(item) == DouguoTypeItem:
#             if os.path.getsize("fileType.json"):
#                 content = "," + json.dumps(dict(item), ensure_ascii=False) + "\n"
#                 self.fileType.write(content)
#             else:
#                 content = json.dumps(dict(item), ensure_ascii=False) + "\n"
#                 self.fileType.write(content)
#
#         if type(item) == DouguoItem:
#             if os.path.getsize("fileItem.json")
#             content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
#             self.fileItem.write(content)
#
#         if type(item) == DouguoAuthorItem:
#             content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
#             self.fileAuthor.write(content)
#
#         return item
#
#     def closs_spidr(self, spider):
#         self.fileType.write(']')
#         self.fileItem.write(']')
#         self.fileAuthor.write(']')
#         self.fileType.close()
#         self.fileItem.close()
#         self.fileAuthor.close()
