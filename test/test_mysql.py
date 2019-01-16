import time

import pymysql as pymysql
from scrapy import log

from Lianjia import settings
from Lianjia.items import LianjiaItem, HouseItem


class TestMySQL(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def insert_or_update_house_daily(self):
        cur_day = time.strftime("%Y-%m-%d", time.localtime())

        querySQl = "select * from `house_daily` WHERE `update_time_day`=%s"
        self.cursor.execute(querySQl, cur_day)
        ret = self.cursor.fetchone()
        if ret:
            updateSQL = """update house_daily 
                            set update_house_cnt=%s, dul_house_cnt=%s, new_house_cnt=%s 
                            WHERE update_time_day=%s""",
            self.cursor.execute(updateSQL, (20, 20, 20, cur_day))
        else:
            insertSQL = """insert into house_daily(update_time_day, update_house_cnt, dul_house_cnt, new_house_cnt)
                          VALUE (%s,%d,%d,%d)""",
            self.cursor.execute(insertSQL, (cur_day, 20, 20, 20))

        self.connect.commit()

    def test_query(self):
        cur_day = '1980-06-19'
        querySQl = "select * from `house_daily` WHERE `update_time_day`=%s"
        self.cursor.execute(querySQl, cur_day)
        ret = self.cursor.fetchone()
        print(ret)

    def test_insert_house_daily(self):
        cur_day = '2020-10-10'

        self.cursor.execute(
            """insert into house_daily(update_time_day,update_house_cnt,dul_house_cnt,new_house_cnt)
              value (%s,%s,%s,%s)""",
            ('2020-10-11',
             0,
             0,
             0))

        self.connect.commit()

    def test_update_house_daily(self):
        cur_day = '2020-10-10'

        updateSQL = """update house_daily 
                        set update_house_cnt=%s, dul_house_cnt=%s, new_house_cnt=%s
                        WHERE update_time_day=%s"""
        self.cursor.execute(updateSQL, (20, 20, 20, cur_day))

        self.connect.commit()

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

        # self.connect.commit()


if __name__ == '__main__':
    test = TestMySQL()
    # test.test_insert_house_daily()
    # test.test_update_house_daily()
    test.insert_or_update_house_daily(1)
    # test.test_query()
