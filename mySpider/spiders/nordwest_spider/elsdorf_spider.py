import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class ElsdorfSpider(Spider):
    name = 'elsdorf_spider'
    allow_domains = ['www.elsdorf.de']
    start_urls = ['https://www.elsdorf.de/index.php?id=661']

    bundesland = 'NW'
    gemeinde = 'Elsdorf'

    def parse(self,response):
        wohngrund_bezeichung = response.xpath("//section[@class='contentelement']//div[@class='ce-bodytext']//b/text()").extract()
        wohngrund_urls = response.xpath("//section[@class='contentelement']//div[@class='ce-bodytext']//a/@href").extract()

        for i in range(0, len(wohngrund_urls)):
            grund_item = GrundstuckItem()  # 实例化
            next_url = wohngrund_urls[i]
            grund_item['bundesland'] = self.bundesland
            grund_item['gemeinde'] = self.gemeinde
            grund_item['bezeichnung'] = wohngrund_bezeichung[i]
            grund_item['link'] = next_url
            yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.detail_page)

    def detail_page(self, response):
        grund_item = response.meta['item']
        content = response.xpath("//blockquote[@id='entry-description']//text()").extract()
        grund_item['content'] = content
        #save texture content
        yield grund_item