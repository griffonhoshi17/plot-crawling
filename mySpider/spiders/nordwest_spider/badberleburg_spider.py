import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class BadberleburgSpider(Spider):
    name = 'badberleburg_spider'
    allow_domains = ['www.bad-berleburg.de']
    start_urls = ['https://www.bad-berleburg.de/index.phtml?sNavID=1746.121&mNavID=1746.15&La=1']

    bundesland = 'NW'
    gemeinde = 'Bad Berleburg'
    base_url = 'https://www.bad-berleburg.de'

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