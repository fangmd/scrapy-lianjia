# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class LianjiaItem(Item):
    # define the fields for your item here like:
    name = Field()


class HouseItem(Item):
    id = Field()  # id: 从 详细页 中提取
    h_name = Field()  # Name
    detail_url = Field()  # 详细页 URL
    community_name = Field()  # 小区名字
    area = Field()  # 面积
    pattern = Field()  # 户型
    latitude = Field()  # 经度
    longitude = Field()  # 纬度
    remark = Field()  # 备注
