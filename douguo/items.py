# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouguoItem(scrapy.Item):
    # 浏览综述 1
    peopleNumber = scrapy.Field()
    # 收藏人数 1
    collectionNumber = scrapy.Field()
    # 描述 1
    description = scrapy.Field()
    # 用料 1
    recipeIngredient = scrapy.Field()
    # 做法步骤
    step = scrapy.Field()
    # 小贴士 1
    tip = scrapy.Field()
    # URL 1
    href = scrapy.Field()
    # 菜名 1
    title = scrapy.Field()
    # 分类信息 1
    typeTitle = scrapy.Field()
    # 难度 1
    difficulty = scrapy.Field()
    # 时间 1
    timeAssume = scrapy.Field()
    # 用户名称 1
    author = scrapy.Field()
    # # 评论数量
    # numOfComments = scrapy.Field()
    # # 评论作者列表
    # authorOfComments = scrapy.Field()



class DouguoTypeItem(scrapy.Item):
    # 一级分类
    catesListInfo = scrapy.Field()

    # 二级分类
    catesList = scrapy.Field()

    # 三级分类
    catesListHref = scrapy.Field()

class DouguoAuthorItem(scrapy.Item):
    # 作者ID
    authorName = scrapy.Field()
    # 作者url
    authorUrl = scrapy.Field()
    # 作者地理位置
    authorLocation = scrapy.Field()
    # 作者收集的菜的数量
    authorCollectionNumber = scrapy.Field()
    # 作者收藏的菜
    authorCollection = scrapy.Field()

    # # 作者关注的人数
    # numOfFollow = scrapy.Field()
    # # 作者被关注的人数
    # numOfFollowed = scrapy.Field()
    # # 作者发布的菜谱
    # numOfRecipes = scrapy.Field()
