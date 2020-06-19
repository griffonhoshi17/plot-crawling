import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class DuelmenSpider(Spider):
    name = 'duelmen_spider'
    allow_domains = ['www.duelmen.de']
    start_urls = ['https://www.duelmen.de/828.html']

    def parse(self,response):
        wohngrund_bezeichung = response.xpath("//li[contains(a/text(), 'Wohnbaugrundstücke')]/ul/li/a/text()").extract()
        wohngrund_urls = response.xpath("//li[contains(a/text(), 'Wohnbaugrundstücke')]/ul/li/a/@href").extract()

        gewerbgrund_bezeichung = response.xpath("//li[contains(a/text(), 'Gewerbegrundstücke')]/ul/li/a/text()").extract()
        gewerbgrund_urls = response.xpath("//li[contains(a/text(), 'Gewerbegrundstücke')]/ul/li/a/@href").extract()

        base_url = 'https://www.duelmen.de/'

        for i in range(0, len(wohngrund_urls)):
            grund_item = GrundstuckItem()  # 实例化
            next_url = base_url + wohngrund_urls[i]
            grund_item['bundesland'] = 'NW'
            grund_item['gemeinde'] = 'Duelmen'
            grund_item['bezeichnung'] = wohngrund_bezeichung[i]
            grund_item['link'] = next_url
            yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.detail_page)

        for i in range(0, len(gewerbgrund_urls)):
            grund_item = GrundstuckItem()  # 实例化
            next_url = base_url + gewerbgrund_urls[i]
            grund_item['bundesland'] = 'NW'
            grund_item['gemeinde'] = 'Duelmen'
            grund_item['bezeichnung'] = gewerbgrund_bezeichung[i]
            grund_item['link'] = next_url
            yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.detail_page)

    def detail_page(self, response):
        grund_item = response.meta['item']
        content = response.xpath("//div[@id='contentinhalt']//text()").extract()
        grund_item['content'] = content
        #save texture content
        yield grund_item