import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class MeschedeSpider(Spider):
    name = 'meschede_spider'
    allow_domains = ['www.meschede.de']
    start_urls = ['https://www.meschede.de/wirtschaft-karriere-bildung/gewerbeflaechen-und-immobilien/']

    bundesland = 'NW'
    gemeinde = 'Meschede'
    base_url = 'https://www.meschede.de'

    def parse(self,response):
        wohngrund_urls = response.xpath("//li[@class='active current sub']/ul/li/a/@href").extract()
        wohngrund_bezeichungs = response.xpath("//li[@class='active current sub']/ul/li/a//text()").extract()

        for i in range(0, len(wohngrund_urls)):
            grund_item = GrundstuckItem()
            base_url = self.base_url
            next_url = base_url + wohngrund_urls[i]
            grund_item['bundesland'] = self.bundesland
            grund_item['gemeinde'] = self.gemeinde
            grund_item['bezeichnung'] = wohngrund_bezeichungs[i]
            grund_item['link'] = next_url
            yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.detail_page)

    def detail_page(self, response):
        grund_item = response.meta['item']
        content = response.xpath("//div[@id='maincontent']//div[@class='frame frame-default frame-type-textmedia frame-layout-0']//text()").extract()
        tags = ' '.join(content)
        grund_item['content'] = tags
        yield grund_item