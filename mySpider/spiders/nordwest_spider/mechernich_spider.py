import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class MechernichSpider(Spider):
    name = 'mechernich_spider'
    allow_domains = ['www.mechernich.de']
    start_urls = ['https://www.mechernich.de/wirtschaft-bauen/gewerbliche-baugebiete/']

    bundesland = 'NW'
    gemeinde = 'Mechernich'
    base_url = 'https://www.mechernich.de'

    def parse(self,response):
        wohngrund_urls = response.xpath("//div[contains(@class,'csc-header')]//h1/a/@href").extract()
        wohngrund_bezeichungs = response.xpath("//div[contains(@class,'csc-header')]//h1/a/text()").extract()

        for i in range(0, len(wohngrund_urls)):
            grund_item = GrundstuckItem()
            next_url = wohngrund_urls[i]
            grund_item['bundesland'] = self.bundesland
            grund_item['gemeinde'] = self.gemeinde
            grund_item['bezeichnung'] = wohngrund_bezeichungs[i]
            grund_item['link'] = next_url
            yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.detail_page)

    def detail_page(self, response):
        grund_item = response.meta['item']
        content = response.xpath("//div[@class='mainContentLeft_Section']//text()").extract()
        tags = ' '.join(content)
        grund_item['content'] = tags
        yield grund_item