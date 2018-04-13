# -*- coding: utf-8 -*-
import scrapy
from douguo.items import DouguoTypeItem
from douguo.items import DouguoItem


class DouguoSpiderSpider(scrapy.Spider):
    name = 'douguo_spider'
    allowed_domains = ['douguo.com']
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

        if len(response.xpath(".//div[@class='xtip']")) != 0:
            item['description'] = response.xpath(".//div[@class='xtip']/text()").extract()[0].strip()
        else:
            item['description'] = "无"

        if len(response.xpath(".//div[@class='falisc']/span[1]")) != 0:
            item['peopleNumber'] = response.xpath(".//div[@class='falisc']/span[1]/text()").extract()[0].strip()
        else:
            item['peopleNumber'] = "-1"

        if len(response.xpath(".//div[@class='falisc']/span[2]")) != 0:
            item['collectionNumber'] = response.xpath(".//div[@class='falisc']/span[2]/text()").extract()[0].strip()
        else:
            item['collectionNumber'] = "-1"

        if len(response.xpath(".//div[@class='xtieshi']/p")) != 0:
            item['tip'] = response.xpath(".//div[@class='xtieshi']/p/text()").extract()[0].strip()
        else:
            item['tip'] = "无"

        item['href'] = response.meta['url']

        item['author'] = response.xpath(".//div[@class='auth']/h4/a/text()").extract()[0].strip()

        recipeIngredient = ""
        for pair in response.xpath(".//table//tr[not(@class='mtim')]/td"):
            if len(pair.xpath("./span[1]/a")) != 0:
                ing1 = pair.xpath("./span[1]/a/text()").extract()[0].strip()
            else:
                ing1 = pair.xpath("./span[1]/label/text()").extract()[0].strip()
            if len(pair.xpath("./span[2]")) == 1:           # TODO
                ing2 = pair.xpath("./span[2]/text()").extract()[0].strip()
            else:
                ing2 = 'null'
            recipeIngredient += str(ing1) + " &: " + str(ing2) + "$"
        item['recipeIngredient'] = recipeIngredient


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

        steps = response.xpath(
            ".//div[@class='step clearfix']/div[@class='stepcont mll libdm pvl clearfix']/p/text()").extract()
        step = " * "
        for value in steps:
            step += value + " * "
        item['step'] = step

        yield item
