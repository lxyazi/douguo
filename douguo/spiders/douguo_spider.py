# -*- coding: utf-8 -*-
import scrapy
from douguo.items import DouguoTypeItem
from douguo.items import DouguoItem
from douguo.items import DouguoAuthorItem


class DouguoSpiderSpider(scrapy.Spider):
    name = 'douguo_spider'
    start_urls = ['http://www.douguo.com/caipu/fenlei']

    def parse(self, response):
        nodeList = response.xpath(".//div[@class='fei3 mb20 libdm pbl']")
        for node in nodeList:
            catesListInfo = node.xpath("./h2/text()").extract()[0].strip()
            catesList = node.xpath(".//ul/li")
            for cates in catesList:
                item = DouguoTypeItem()
                item['catesListInfo'] = catesListInfo
                item['catesList'] = cates.xpath("./a/text()").extract()[0].strip()
                item['catesListHref'] = cates.xpath("./a/@href").extract()[0].strip()
                yield item
                yield scrapy.Request(item['catesListHref'], meta={"catesList": item['catesList']},
                                     callback=self.listParse)

    def listParse(self, response):
        catesList = response.meta['catesList']
        nodeList = response.xpath(".//div[@class='cp_box']")
        for node in nodeList:
            url = node.xpath("./a/@href").extract()[0].strip()
            yield scrapy.Request(url, meta={"catesList": catesList, "url": url}, callback=self.itemParse)
        if len(response.xpath(".//div[@class='pagination']/span/a[text()='下一页']/@href")) != 0:
            url = response.xpath(".//div[@class='pagination']/span/a[text()='下一页']/@href").extract()[0].strip()
            yield scrapy.Request(url, meta={'catesList': response.meta['catesList']}, callback=self.listParse)

    def itemParse(self, response):
        item = DouguoItem()
        item['typeTitle'] = response.meta['catesList']
        item['title'] = response.xpath(".//div[@class='recinfo']//h1/text()").extract()[0].strip()

        # 菜的描述
        if len(response.xpath(".//div[@class='xtip']")) != 0:
            item['description'] = response.xpath(".//div[@class='xtip']/text()").extract()[0].strip()
        else:
            item['description'] = "无"

        # 浏览次数
        if len(response.xpath(".//div[@class='falisc']/span[1]")) != 0:
            item['peopleNumber'] = response.xpath(".//div[@class='falisc']/span[1]/text()").extract()[0].strip()
        else:
            item['peopleNumber'] = "-1"

        # 收藏次数
        if len(response.xpath(".//div[@class='falisc']/span[2]")) != 0:
            item['collectionNumber'] = response.xpath(".//div[@class='falisc']/span[2]/text()").extract()[0].strip()
        else:
            item['collectionNumber'] = "-1"

        # 小贴士
        if len(response.xpath(".//div[@class='xtieshi']/p")) != 0:
            item['tip'] = response.xpath(".//div[@class='xtieshi']/p/text()").extract()[0].strip()
        else:
            item['tip'] = "无"

        # 该道菜的url

        item['href'] = response.meta['url'].split('/')[4][0:-5]

        # 用户站内ID的爬取
        item['author'] = response.xpath(".//div[@class='auth']/h4/a/text()").extract()[0].strip()

        # 用户主页的爬取及收藏页面的跳转
        authorUrl = response.xpath(".//div[@class='auth']/h4/a/@href").extract()[0].strip()
        authorUrlCollection = authorUrl.replace(".html", "/collect")
        yield scrapy.Request(authorUrl,
                             meta={'url': authorUrl, 'author': item['author'], 'urlCollection': authorUrlCollection},
                             callback=self.authorMainParse)

        # ----------------------爬取菜的用料--------------------------------------
        recipeIngredient = ""
        for pair in response.xpath(".//table//tr[not(@class='mtim')]/td"):
            if len(pair.xpath("./span")) != 0:
                if len(pair.xpath("./span[1]/a")) != 0:
                    ing1 = pair.xpath("./span[1]/a/text()").extract()[0].strip()
                else:
                    ing1 = pair.xpath("./span[1]/label/text()").extract()[0].strip()

                if len(pair.xpath("./span[2]/text()").extract()) != 0:
                    ing2 = pair.xpath("./span[2]/text()").extract()[0].strip()
                else:
                    ing2 = 'null'
                recipeIngredient += str(ing1) + "&:" + str(ing2) + "$"

        item['recipeIngredient'] = recipeIngredient

        # ------------------爬取难易程度和时间消耗这两个信息------------------------------------

        difficulty = "无"
        timeAssume = "无"
        diffAndTime = response.xpath(".//table//tr[1]/td/span/text()").extract()
        for value in diffAndTime:
            if value == '难度：':
                difficulty = response.xpath(".//table//tr[1]/td[1]/text()").extract()[0].strip()
            if value == '时间：':
                timeAssume = response.xpath(".//table//tr[1]/td[2]/text()").extract()[0].strip()
        if len(response.xpath(".//table//tr[1]/td/span")) == 2:
            difficulty = \
                response.xpath(".//table//tr[@class='mtim']/td/text()").extract()[0].strip()
            timeAssume = \
                response.xpath(".//table//tr[@class='mtim']/td/text()").extract()[2].strip()
        item['difficulty'] = difficulty
        item['timeAssume'] = timeAssume

        # 爬取菜的步骤
        steps = response.xpath(
            ".//div[@class='step clearfix']/div[@class='stepcont mll libdm pvl clearfix']/p/text()").extract()
        step = "*"
        for value in steps:
            step += value + "*"
        item['step'] = step

        # 爬取菜的评论数量和作者
        authorID = response.xpath(
            ".//div[@id='comment_container']/div[@class='coping ptb2010 clearfix libdm']/div[@class='coimg mrm']/a/@href")

        yield item

    def parseComments(self, authorID, response):
        for value in response.xpath(
                ".//div[@id='comment_container']/div[@class='coping ptb2010 clearfix libdm']/div[@class='coimg mrm']/a/@href"):
            value = value.strip()
            value = value.split('/')[2][0:-5]
            authorID.append(value)


        return authorID

    def authorMainParse(self, response):
        item = DouguoAuthorItem()
        item['authorUrl'] = response.meta['url'].split('/')[4][0:-5]
        item['authorName'] = response.meta['author']
        item['authorLocation'] = response.xpath(".//div[@class='clearfix']/span[@class='fcc']/text()").extract()[0]

        yield scrapy.Request(response.meta['urlCollection'],
                             meta={'item': item, 'urlCollection': response.meta['urlCollection']},
                             callback=self.authorIfCollectionParse)

    def authorIfCollectionParse(self, response):
        item = response.meta['item']

        item['authorCollectionNumber'] = \
            (response.xpath(".//div[@id='main']//li[1]/a/span/text()").extract()[0]).strip().split('（')[1][0:-1]

        # 爬取用户的收藏列表
        if item['authorCollectionNumber'] == "0":
            item['authorCollection'] = '无'
            yield item
        else:
            collections = ""
            # 为什么这条会被过滤
            yield scrapy.Request(response.meta['urlCollection'], meta={'item': item, 'collections': collections},
                                 callback=self.authorCollectionParse, dont_filter=True)

    def authorCollectionParse(self, response):
        collections = response.meta['collections']
        item = response.meta['item']

        for node in response.xpath(".//div[@id='main']//div[@class='faveone']"):
            # 菜名
            collection = node.xpath("./h3/a/text()").extract()[0]
            # 菜的唯一表示（url）
            collection += "**" + node.xpath("./h3/a/@href").extract()[0].strip().split('/')[-1].split('.')[0]
            # 菜的作者
            collection += "**" + node.xpath("./p[2]/text()").extract()[0].strip()[3:] + "&&"
            # 合并
            collections += collection
            # flag = 0
        for node in response.xpath(".//div[@class='pagination mt30 mb30']//span[@class='floblock']"):
            if node.xpath("./a/text()").extract()[0].strip() == "下一页":
                return scrapy.Request(node.xpath("./a/@href").extract()[0].strip(),
                                      meta={'item': item, 'collections': collections},
                                      callback=self.authorCollectionParse, dont_filter=True)

        item['authorCollection'] = collections
        yield item
