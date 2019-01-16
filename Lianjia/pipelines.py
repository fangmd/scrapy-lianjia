# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

import pymysql as pymysql
from scrapy import log

from Lianjia import settings
from Lianjia.items import LianjiaItem, HouseItem


class LianjiaPipeline(object):
    def process_item(self, item, spider):
        # print('LianjiaPipeline' + str(item))
        return item


class LianjiaSaveToMysqlPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        if item.__class__ == HouseItem:
            try:
                self.cursor.execute("""select * from house where id = %s""", item["id"])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update house set h_name = %s,detail_url = %s,community_name = %s,
                            area = %s,pattern = %s,latitude = %s,longitude = %s,remark = %s
                            where id = %s""",
                        (item['h_name'],
                         item['detail_url'],
                         item['community_name'],
                         item['area'],
                         item['pattern'],
                         item['latitude'],
                         item['longitude'],
                         item['remark'],
                         item['id']))
                    self.insert_or_update_house_daily(mode=2)
                else:
                    self.cursor.execute(
                        """insert into house(id,h_name,detail_url,community_name,area,
                          pattern,latitude,longitude, remark)
                          value (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (item['id'],
                         item['h_name'],
                         item['detail_url'],
                         item['community_name'],
                         item['area'],
                         item['pattern'],
                         item['latitude'],
                         item['longitude'],
                         item['remark']))
                    self.insert_or_update_house_daily(mode=3)
                self.connect.commit()
            except Exception as error:
                log.err(error)
                print(error)
            return item
        else:
            pass

    def insert_or_update_house_daily(self, mode):
        cur_day = time.strftime("%Y-%m-%d", time.localtime())

        querySQl = "select * from `house_daily` WHERE `update_time_day`=%s"
        self.cursor.execute(querySQl, cur_day)
        ret = self.cursor.fetchone()
        if not ret:
            updateSQL = """insert into house_daily(update_time_day,update_house_cnt,dul_house_cnt,new_house_cnt)
                  value (%s,%s,%s,%s)"""
            self.cursor.execute(updateSQL, (cur_day, 0, 0, 0))

        if mode == 1:
            # update_house_cnt ++
            uhcSQL = """update `house_daily` set update_house_cnt=update_house_cnt+1 where update_time_day=%s"""
            self.cursor.execute(uhcSQL, cur_day)
        elif mode == 2:
            # dul_house_cnt ++ 重复的房子
            dhcSQL = """update `house_daily` set dul_house_cnt=dul_house_cnt+1 where update_time_day=%s"""
            self.cursor.execute(dhcSQL, cur_day)
        elif mode == 3:
            # new_house_cnt ++ 新加的房子
            nhcSQl = """update `house_daily` set new_house_cnt=new_house_cnt+1 where update_time_day=%s"""
            self.cursor.execute(nhcSQl, cur_day)
