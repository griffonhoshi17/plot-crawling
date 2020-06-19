import os

import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

class DattelnSpider(Spider):
    name = "datteln_spider"
    allow_domains = ['www.datteln.de']
    start_urls = ['https://www.datteln.de/09_Bauen_Wohnen/Grundstuecke_und_Immobilien.asp']
    pass
