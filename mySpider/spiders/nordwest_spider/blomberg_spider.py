import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class BlombergSpider(Spider):
    name = 'blomberg_spider'
    allow_domains = ['blomberg-immobilien.de', 'www.blomberg-lippe.net']
    start_urls = ['https://blomberg-immobilien.de/grundstuecke/']

    bundesland = 'NW'
    gemeinde = 'Blomberg'
    base_url = 'https://blomberg-immobilien.de/grundstuecke'

    def parse(self, response):
        grund_item_div_list = response.xpath("//div[@class='search-filter-results']/div[@class='search-result-entry']")

        for grund_item_div in grund_item_div_list:
            grund_item = GrundstuckItem()
            next_url = grund_item_div.xpath("./h2/a/@href").extract_first()
            grund_bezeichung = grund_item_div.xpath("./h2/a//text()").extract_first()
            grund_item['link'] = next_url
            grund_item['bundesland'] = self.bundesland
            grund_item['gemeinde'] = self.gemeinde
            grund_item['bezeichnung'] = grund_bezeichung
            yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.detail_page)

    def detail_page(self, response):
        grund_item = response.meta['item']
        content = response.xpath("//div[@id='content']//text()").extract()
        tags = ' '.join(content)
        grund_item['content'] = tags
        yield grund_item