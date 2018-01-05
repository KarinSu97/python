# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qiushibaike.items import QiushibaikeItem
from scrapy.http import Request

class QiushibaikeAutoSpider(CrawlSpider):
    name = 'qiushibaike_auto'
    allowed_domains = ['qiushibaike.com']
    '''
    start_urls = ['http://www.qiushibaike.com/']
    '''
    def start_requests(self):
        headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
        yield Request('http://www.qiushibaike.com/',headers=headers)
    rules = (
        Rule(LinkExtractor(allow='article'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = QiushibaikeItem()
        i['content']=response.xpath('//div[@class="content"]/text()').extract()
        i['link'] = response.xpath('//link[@rel="canonical"]/@href').extract()
        print(i['content'])
        print(i['link'])
        print('')
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
