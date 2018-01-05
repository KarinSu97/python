# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jingdong.items import JingdongItem
import re
import urllib.request

class JdSpider(CrawlSpider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['http://www.jd.com/']

    rules = (
        Rule(LinkExtractor(allow=''), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            item = JingdongItem()
            url=response.url
            pat='item.jd.com/(.*?).html'
            x=re.search(pat,url)
            if x:
                id=re.compile(pat).findall(url)[0]
                print(id)
                item['title']=response.xpath('/html/head/title/text()').extract()
                item['shop']=response.xpath('//div[@class="name"]/a/text()').extract()
                item['shop_link']=response.xpath('//div[@class="name"]/a/@href').extract()
                price_url='https://p.3.cn/prices/mgets?callback=jQuery2250842&type=1&area=1_72_2799_0&pdtk=&pduid=742497677&pdpin=&pin=null&pdbp=0&skuIds=J_'+str(id)+'&ext=11000000&source=item-pc'
                comment_url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3091&productId='+str(id)+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
                price_data=urllib.request.urlopen(price_url).read().decode('utf-8','ignore')
                comment_data=urllib.request.urlopen(comment_url).read().decode('utf-8','ignore')
                item['price']=re.compile('"p":"(.*?)"').findall(price_data)
                item['good_rate']=re.compile('"goodRateShow":(.*?),').findall(comment_data)
            else:
                pass
            return item
        except Exception as e:
            print(e)