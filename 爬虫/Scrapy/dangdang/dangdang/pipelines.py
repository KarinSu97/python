# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DangdangPipeline(object):
    def process_item(self, item, spider):
        conn=pymysql.connect(host='localhost',user='root',password='123456',db='spiders',port=3306,charset='utf8mb4')
        for i in range(len(item['title'])):
            title=item['title'][i]
            link=item['link'][i]
            comment=item['comment'][i]
            try:
                sql="insert into dangdang(title,link,comment) values('"+title+"','"+link+"','"+comment+"')"
                conn.query(sql)
                conn.commit()
            except Exception as e:
                print(str(e))
        conn.close()
        return item
