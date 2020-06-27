import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class BadmuenstereifelSpider(Spider):
    name = 'badmuenstereifel_spider'
    allow_domains = ['www.bad-muenstereifel.de']
    start_urls = ['https://www.bad-muenstereifel.de/wirtschaft/immobilienangebote/']

    bundesland = 'NW'
    gemeinde = 'Bad Münstereifel'
    base_url = 'https://www.bad-muenstereifel.de'

    def parse(self,response):
        wohngrund_urls = response.xpath("//div[@id='content']//div[@style='display:inline']//h4/a/@href").extract()
        wohngrund_bezeichungs = response.xpath("//div[@id='content']//div[@style='display:inline']//h4/a//text()").extract()

        for i in range(0, len(wohngrund_urls)):
            # self.log('link: %s' % wohngrund_urls[i])
            # self.log('link: %s' % wohngrund_bezeichungs[i])
            grund_item = GrundstuckItem()
            base_url = self.base_url
            next_url = base_url + wohngrund_urls[i]
            grund_item['bundesland'] = self.bundesland
            grund_item['gemeinde'] = self.gemeinde
            grund_item['bezeichnung'] = wohngrund_bezeichungs[i]
            grund_item['link'] = next_url
            # yield grund_item
            yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.detail_page)

    def detail_page(self, response):
        grund_item = response.meta['item']
        content = response.xpath("//div[@id='content']//text()").extract()
        tags = ' '.join(content)
        grund_item['content'] = tags
        yield grund_item