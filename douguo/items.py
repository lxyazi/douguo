# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouguoItem(scrapy.Item):
    # 浏览综述
    peopleNumber = scrapy.Field()
    # 收藏人数
    collectionNumber = scrapy.Field()
    # 描述
    description = scrapy.Field()
    # 用料
    recipeIngredient = scrapy.Field()
    # 做法步骤
    step = scrapy.Field()
    # 小贴士
    tip = scrapy.Field()
    # URL
    href = scrapy.Field()
    # 菜名
    title = scrapy.Field()
    # 分类信息
    typeTitle = scrapy.Field()
    # 难度
    difficulty = scrapy.Field()
    # 时间
    timeAssume = scrapy.Field()
    # 用户名称
    author = scrapy.Field()

class DouguoTypeItem(scrapy.Item):
    # 一级分类
    catesListInfo = scrapy.Field()

    # 二级分类
    catesList = scrapy.Field()

    # 三级分类
    catesListHref = scrapy.Field()