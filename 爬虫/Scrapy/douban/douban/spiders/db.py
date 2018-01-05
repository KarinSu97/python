# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
import urllib.request

class DbSpider(scrapy.Spider):
    name = 'db'
    header={"User-Agent":
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    allowed_domains = ['douban.com']
    '''
    start_urls = ['http://douban.com/']
    '''
    def start_requests(self):
        return [Request('https://accounts.douban.com/login',callback=self.parse,meta={'cookiejar':1},headers=self.header)]   #开启cookie
    def parse(self, response):
        url='https://accounts.douban.com/login'
        captcha=response.xpath('//img[@class="captcha_image"]/@src').extract()
        if len(captcha)==0:
            print("没有验证码")
            data={
                "form_email":"1173229840@qq.com",
                "form_password":"2012050355lch",
                "redir":"https://www.douban.com/people/145935277/"
            }
        else:
            print("有验证码,请前往查看验证码，并输入：")
            file='C:/Users/T/Desktop/Scrapy/douban/captcha.png'
            urllib.request.urlretrieve(captcha[0],filename=file)
            captcha_value=input()
            data = {
                "form_email": "1173229840@qq.com",
                "form_password": "2012050355lch",
                "captcha-solution":captcha_value,
                "redir": "https://www.douban.com/people/145935277/"
            }
        print("登陆中.......")
        return [FormRequest.from_response(response,
                                          meta={"cookiejar":response.meta['cookiejar']},
                                          formdata=data,
                                          headers=self.header,
                                          callback=self.next
                                          )]
    def next(self,response):
        title=response.xpath("/html/head/title/text()").extract()
        content=response.xpath('//div[@class="note-header pl2"]/a[@class="ll"]/text()').extract()
        print(title[0])
        print(content[0])


