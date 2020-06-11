import os

import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector

from mySpider.items import DetailedInfoItem

class BedburgSpider(scrapy.Spider):
    name = "bedburg_spider"
    allow_domains = ['www.bedburg.de']

    start_urls = ['https://www.bedburg.de/Stadtentwicklung-Bauen-und-Wirtschaft/Bauen/Bauen-in-Bedburg.htm?']

    """
    def start_requests(self):
        base_url = "http://www.courtsofnz.govt.nz/the-courts/supreme-court/case-summaries/case-information-"
        for i in range(2004, 2020):
            url = base_url + str(i)
            yield scrapy.Request(url=url, callback=self.parse)
    """
    def parse(self, response):
        item = DetailedInfoItem()
        tables = response.xpath("//table[@summary='Verkauf einzelner Baugrundstücke']").extract()
        for table in tables:
            self.log('内容: %s' % table)
            pass