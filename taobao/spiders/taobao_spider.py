# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from taobao.items import ProductItem

class TaobaoSpider(scrapy.Spider):
    name = 'taobao_spider'
    allowed_domains = ['www.taobao.com']
    base_url = 'https://s.taobao.com/search?q='

    def start_requests(self):
        keyword = self.settings.get('KEYWORD')
        url = self.base_url + quote(keyword)
        for page in range(1, self.settings.get('MAX_PAGE')):
            yield scrapy.Request(url=url, callback=self.parse, cookies=list, meta={'page': page}, dont_filter=True)


    def parse(self, response):
        products = response.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"]//div[contains(@class, "item")]')
        print('************当前抓取页面：', response.meta.get('page'))
        for product in products:
            item = ProductItem()
            item['price'] = ''.join(product.xpath('.//div[contains(@class, "price")]//text()').extract()).strip()
            item['title'] = ''.join(product.xpath('.//div[contains(@class, "title")]//text()').extract()).strip()
            item['shop'] = ''.join(product.xpath('.//div[contains(@class, "shop")]//text()').extract()).strip()
            item['image'] = ''.join(
                product.xpath('.//div[@class="pic"]//img[contains(@class, "img")]/@data-src').extract()).strip()
            item['deal'] = product.xpath('.//div[contains(@class, "deal-cnt")]//text()').extract_first()
            item['location'] = product.xpath('.//div[contains(@class, "location")]//text()').extract_first()
            yield item