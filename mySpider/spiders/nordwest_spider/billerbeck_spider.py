import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.utils.response import get_base_url

from mySpider.items import GrundstuckItem

class BillerbeckSpider(Spider):
    name = 'billerbeck_spider'
    allow_domains = ['www.billerbeck.de']
    start_urls = ['http://www.billerbeck.de/staticsite/staticsite2.php?menuid=565']

    bundesland = 'NW'
    gemeinde = 'Billerbeck'
    base_url = 'http://www.billerbeck.de'

    def parse(self,response):
        grund_bezeichungs = response.xpath("//div[@class='content-text']//div/u/strong//text()").extract_first()
        grund_urls = get_base_url(response)

        grund_item = GrundstuckItem()  # 实例化
        next_url = grund_urls
        grund_item['bundesland'] = self.bundesland
        grund_item['gemeinde'] = self.gemeinde
        grund_item['link'] = next_url
        grund_item['bezeichnung'] = grund_bezeichungs
        content = response.xpath("//div[@class='staticsite-content']//text()").extract()
        tags = ' '.join(content)
        grund_item['content'] = tags

        yield grund_item
        #yield scrapy.Request(next_url, meta={'item': grund_item}, callback=self.detail_page)
        #yield scrapy.Request(next_url, callback=self.grund_list_page)

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
