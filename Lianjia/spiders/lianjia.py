# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request, Selector
from scrapy.loader import ItemLoader

from Lianjia.items import LianjiaItem, HouseItem
from utils.url_parse import get_id_from_url


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://hz.lianjia.com/ershoufang/']
    # https://hz.lianjia.com/ershoufang/pg2/

    def parse(self, response):
        print('Http URL: ' + str(response.url))
        # print('Http Body: ' + str(response.body))

        hSS = response.xpath('//li[@class="clear LOGCLICKDATA"]')
        for houseSelector in hSS:
            tempSe = Selector(text=houseSelector.extract())
            # print(tempSe.xpath(
            #     '//li[@class="clear LOGCLICKDATA"]/a[@class="noresultRecommend img "]/@href').extract())

            url = tempSe.xpath(
                '//li[@class="clear LOGCLICKDATA"]/a[@class="noresultRecommend img "]/@href').extract_first()

            houseItem = HouseItem()
            houseItem['detail_url'] = "".join(url)
            houseItem['h_name'] = "".join(tempSe.xpath(
                '//div[@class="info clear"]/div[@class="title"]/a/text()').extract_first())
            houseItem['id'] = "".join(get_id_from_url(url))
            houseItem['community_name'] = "".join(tempSe.xpath(
                '//div[@class="info clear"]/div[@class="address"]/div/a/text()').extract_first())
            houseItem['area'] = "".join("")
            houseItem['pattern'] = "".join("")
            houseItem['latitude'] = "".join("")
            houseItem['longitude'] = "".join("")
            houseItem['remark'] = "".join("")

            yield houseItem

        pageInfo = json.loads(response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract_first())
        maxPage = pageInfo['totalPage']
        if maxPage > 2:
            for i in range(2, maxPage):
                yield Request('https://hz.lianjia.com/ershoufang/pg{}/'.format(i), callback=self.parse)
