import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class HeinsbergSpider(Spider):
    name = 'heinsberg_spider'
    allow_domains = ['www.heinsberg.de']
    start_urls = ['https://www.heinsberg.de/wirtschaft-leistung/grundstuecke-in-den-gewerbe-und-industriegebieten']

    bundesland = 'NW'
    gemeinde = 'Heinsberg'

    def parse(self,response):
        wohngrund_bezeichungs = response.xpath("//div[@class='image-with-text__headline id-headline']/text()").extract()
        wohngrund_urls = response.xpath("//div[@class='textblock']/h3/a/@href").extract()
        grund_list = response.xpath("//div[@class='textblock']/h3/a")

        for i_item in grund_list:
            grund_item = GrundstuckItem()  # 实例化
            base_url = 'https://www.heinsberg.de'
            next_url = base_url + i_item.xpath("@href").extract_first()
            grund_item['bundesland'] = self.bundesland
            grund_item['gemeinde'] = self.gemeinde
            grund_item['bezeichnung'] = i_item.xpath("text()").extract_first()
            grund_item['link'] = next_url
            yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.detail_page)

    def detail_page(self, response):
        grund_item = response.meta['item']
        content = response.xpath("//div[@id='col1_content']/div[@class='pimcore_area_layout2 pimcore_area_content']//text()").extract()
        tags = ' '.join(content)
        grund_item['content'] = tags
        #save texture content
        yield grund_item