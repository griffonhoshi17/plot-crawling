# -*- coding: utf-8 -*-
import scrapy


class SimpleurlSpider(scrapy.Spider):
    name = 'simpleUrl'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/']

    def parse(self, response):
        pass
