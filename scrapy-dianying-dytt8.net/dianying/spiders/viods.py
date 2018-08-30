# -*- coding: utf-8 -*-
import scrapy
from dianying.items import DianyingItem
import ssl
class ViodsSpider(scrapy.Spider):
    # ssl._create_default_https_context = ssl._create_unverified_context
    name = 'viods'
    allowed_domains = ['dytt8.net']
    start_urls = ['http://www.dytt8.net/html/gndy/dyzz/list_23_2.html']

    def parse(self, response):

        # 从响应体中提取出所有的电影信息
        viod_list = response.xpath("//div[@class='co_content8']//table")
        for viod in viod_list:
            item=DianyingItem()
            item['title']=viod.xpath(".//a/text()").extract_first()
            item['data']=viod.xpath(".//font/text()").extract_first()
            url_next="http://www.dytt8.net" + viod.xpath(".//a/@href").extract_first()
            yield scrapy.Request(url=url_next,callback=self.parse_next,meta={'item':item})

    def parse_next(self,request):
        item=request.meta['item']
        item['img']=request.xpath("//div[@id='Zoom']//img[1]/@src").extract_first()
        item['content']=request.xpath("//div[@class='co_content8']//p/text()").extract()[0]
        item['url']=request.xpath("//div[@id='Zoom']//a/@href").extract_first()#font size="4"


        yield item
