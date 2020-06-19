# -*- coding: utf-8 -*-
import scrapy


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['scrapyd.cn']
    start_urls = ['http://scrapyd.cn/']

    def parse(self, response):
        pass
