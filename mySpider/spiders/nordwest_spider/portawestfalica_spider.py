import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class PortawestfalicaSpider(Spider):
    name = 'portawestfalica_spider'
    allow_domains = ['www.portawestfalica.de']
    start_urls = ['https://www.portawestfalica.de/sv_porta_westfalica/Stadtleben/Bauen%20und%20Wohnen/Immobilienangebote/']

    bundesland = 'NW'
    gemeinde = 'Porta Westfalica'
    base_url = 'https://www.portawestfalica.de/sv_porta_westfalica/Stadtleben/Bauen%20und%20Wohnen/Immobilienangebote/'

    def parse(self,response):
        wohngrund_urls = response.xpath("//main[@id='standardPage-maincontent']//a/@href").extract()
        wohngrund_bezeichungs = response.xpath("//main[@id='standardPage-maincontent']//a//text()").extract()

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
        content = response.xpath("//main[@id='standardPage-maincontent']//text()").extract()
        tags = ' '.join(content)
        grund_item['content'] = tags
        yield grund_item