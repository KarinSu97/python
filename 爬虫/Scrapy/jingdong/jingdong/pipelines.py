# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JingdongPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host='localhost', user='root', password='123456', db='spiders', port=3306,
                               charset='utf8mb4')
        title=item['title'][0]
        shop = item['shop'][0]
        shop_link = item['shop_link'][0]
        price = item['price'][0]
        good_rate = item['good_rate'][0]
        sql="insert into jingdong(title,shop,shop_link,price,good_rate) values('"+title+"','"+shop+"','"+shop_link+"','"+price+"','"+good_rate+"')"
        conn.query(sql)
        conn.commit()
        conn.close()
        return item
