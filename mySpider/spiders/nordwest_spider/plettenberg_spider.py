import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class PlettenbergSpider(Spider):
    name = 'plettenberg_spider'
    allow_domains = ['www.plettenberg.de']
    start_urls = ['http://www.plettenberg.de/planen-bauen-umwelt-verkehr/bauen-und-wohnen/baugebiete-und-grundstuecke/']

    bundesland = 'NW'
    gemeinde = 'Plettenberg'
    base_url = 'http://www.plettenberg.de'

    def parse(self,response):
        wohngrund_urls = response.xpath("//li[@class='active']/ul/li/a/@href").extract()
        wohngrund_bezeichungs = response.xpath("//li[@class='active']/ul/li/a/text()").extract()

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
        content = response.xpath("//div[@id='content']//text()").extract()
        tags = ' '.join(content)
        grund_item['content'] = tags
        yield grund_item