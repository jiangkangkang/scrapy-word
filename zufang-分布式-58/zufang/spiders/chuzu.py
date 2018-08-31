# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zufang.items import ZufangItem
from scrapy_redis.spiders import RedisCrawlSpider
class ChuzuSpider(RedisCrawlSpider):
    name = 'chuzu'
    allowed_domains = ['bj.58.com']
    # start_urls = ['http://bj.58.com/chuzu/pn1/']
    redis_key = 'chuzu:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'http://bj.58.com/chuzu/pn\d/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        home_list=response.xpath("//div[@class='content']//li")
        for home in home_list:
            item=ZufangItem()
            item['title']=home.xpath(".//h2/a/text()").extract_first()
            net_url='http:'+home.xpath(".//div[@class='des']/h2/a/@href").extract_first()
            yield scrapy.Request(url=net_url,callback=self.parse_next,meta={'item':item})

        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
    def parse_next(self,response):
        item=response.meta['item']
        item['img']=response.xpath("//div[@id='bigImg']/img/@src").extract_first()
        item['jiage']=response.xpath("//span[contains(@class,'c_ff552e')]//text()").extract_first()
        item['info']=response.xpath("//ul[contains(@class,'f14')]/li[position() < 7]").extract_first()
        yield item
