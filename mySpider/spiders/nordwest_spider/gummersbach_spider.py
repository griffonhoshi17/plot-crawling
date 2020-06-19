import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class GummersbachSpider(Spider):
    name = 'gummersbach_spider'
    allow_domains = ['www.gummersbach.de']
    start_urls = ['https://www.gummersbach.de/de/rathaus/immobilien.html']

    bundesland = 'NW'
    gemeinde = 'Gummersbach'

    def parse(self,response):
        wohngrund_bezeichung = response.xpath("//div[@class='panel-group neos-contentcollection']//h4[@class='panel-title']//span/text()").extract_first()
        wohngrund_urls = self.start_urls
        # TODO
        for i in range(0, len(wohngrund_urls)):
            grund_item = GrundstuckItem()  # 实例化
            base_url = 'https://www.wtg-gronau.de'
            next_url = base_url + wohngrund_urls[i]
            grund_item['bundesland'] = self.bundesland
            grund_item['gemeinde'] = self.gemeinde
            grund_item['bezeichnung'] = wohngrund_bezeichung[i]
            grund_item['link'] = next_url
            #yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.detail_page)

    def detail_page(self, response):
        grund_item = response.meta['item']
        content = response.xpath("//div[@class='main-row ']//text()").extract()
        grund_item['content'] = content
        #save texture content
        yield grund_item