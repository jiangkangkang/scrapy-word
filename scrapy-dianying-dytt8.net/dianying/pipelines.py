# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class DianyingPipeline(object):
    def open_spider(self,spider):
        self.conn=pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='j51265126',
            db='videos',
            charset='utf8'
        )
        self.con=self.conn.cursor()

    def process_item(self, item, spider):
        sql="INSERT INTO dianying VALUES (NULL ,'%s','%s','%s','%s','%s')"%(item['title'],item['data'],item['img'],item['content'],item['url'])
        self.con.execute(sql)
        self.conn.commit()
        return item

    def close_spider(self,spider):

        self.con.close()
        self.conn.close()
