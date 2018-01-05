# -*- coding: utf-8 -*-
import scrapy
from tianshan.items import TianshanItem
from scrapy.http import Request

class LessonSpider(scrapy.Spider):
    name = 'lesson'
    allowed_domains = ['hellobi.com']
    start_urls = ['https://edu.hellobi.com/course/1']

    def parse(self, response):
        item=TianshanItem()
        item['title']=response.xpath('//div[@class="course-info"]/h1/text()').extract()
        item['link'] = response.xpath('//ul[@class="nav nav-tabs"]/li[@class="active"]/a/@href').extract()[0]\
            .replace('overview','')
        item['stu_num'] = response.xpath('//span[@class="course-view"]/text()').extract()[0].replace("人学习",'')
        yield item
        for i in range(2,239):
            url='https://edu.hellobi.com/course/'+str(i)
            yield Request(url,callback=self.parse)
