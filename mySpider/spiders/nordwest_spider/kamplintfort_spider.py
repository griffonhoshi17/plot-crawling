import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider

from mySpider.items import GrundstuckItem

class KamplintfortSpider(Spider):
    name = 'kamplintfort_spider'
    allow_domains = ['www.kamp-lintfort.de']
    start_urls = ['https://www.kamp-lintfort.de/de/inhalt/staedtische-baugrundstuecke/']

    bundesland = 'NW'
    gemeinde = 'KampLintfort'
    base_url = 'https://www.kamp-lintfort.de'

    def parse(self,response):
        grund_urls = response.xpath("//div[@class='floatbox']/h4/a/@href").extract()

        for grund_url in grund_urls:
            #grund_item = GrundstuckItem()  # 实例化
            next_url = self.base_url + grund_url
            #grund_item['bundesland'] = self.bundesland
            #grund_item['gemeinde'] = self.gemeinde
            #grund_item['link'] = next_url
            #yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.detail_page)
            yield scrapy.Request(next_url, callback=self.grund_list_page)

    def grund_list_page(self, response):
        #grund_item = response.meta['item']
        grund_list = response.xpath("//table[@class='simple full']/tbody/tr")
        for i_item in grund_list:
            grund_item = GrundstuckItem()  # 实例化
            grund_item['bundesland'] = self.bundesland
            grund_item['gemeinde'] = self.gemeinde

            grund_link = i_item.xpath("./td")[0].xpath("./a/@href").extract_first() # link
            # self.log('link: %s' % grund_link)
            if grund_link is None:
                next_url = self.base_url
                grund_bezeichung = i_item.xpath("./td")[0].xpath("./text()").extract_first()
            else:
                next_url = self.base_url + grund_link
                grund_bezeichung = i_item.xpath("./td")[0].xpath("./a/text()").extract_first()
            grund_item['link'] = next_url
            grund_item['bezeichnung'] = grund_bezeichung

            grund_content = 'NAME: ' + grund_bezeichung + '; ' # content: name, flache, preis, status
            grund_size = i_item.xpath("./td")[1].xpath("./text()").extract_first()
            grund_content = grund_content + 'FLÄCHE: ' + grund_size + '; '
            grund_preis = i_item.xpath("./td")[2].xpath("./text()").extract_first()
            grund_content = grund_content + 'PREIS: ' + grund_preis + '; '
            grund_status = i_item.xpath("./td")[3].xpath("./text()").extract_first()
            grund_content = grund_content + 'STATUS: ' + grund_status
            grund_item['content'] = grund_content

            if grund_link is None:
                yield grund_item
            else:
                yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.grund_detail_page)

    def grund_detail_page(self, response):
        grund_item = response.meta['item']
        content = response.xpath("//div[@id='col3_content']//text()").extract()
        tags = ' '.join(content)
        grund_item['content'] = tags
        yield grund_item
