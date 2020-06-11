import os

import scrapy
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from mySpider.items import ArticleItem


class hoshiItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    info = scrapy.Field()

# Koeln
class KoelnSpider(scrapy.Spider):
    """
    crawl from koeln stadt website
    """
    name = "koeln_spider"
    allowed_domains = ["www.stadt-koeln.de"]
    start_urls = [
        "https://www.stadt-koeln.de/leben-in-koeln/planen-bauen/grundstueck-immobilien/vermarktung-von-unbebauten-gewerbegrundstuecken"
    ]

    def parse(self, response):
        first_titles = response.xpath("//ul[@class='textteaserliste']/li/a/h2/text()").extract()
        first_urls = response.xpath("//ul[@class='textteaserliste']/li/a/@href").extract()

        gemeinde_name = "Köln"
        land_name = "NW"

        for i in range(0, len(first_titles)):
            item = ArticleItem()
            # define the path and folder
            first_filename = "/Users/hoshiraku/Documents/gemeinde_data/data_crawling/" + land_name + '/' + gemeinde_name
            if (not os.path.exists(first_filename)):
                os.makedirs(first_filename)
            item['first_title'] = first_titles[i]
            item['first_url'] = first_urls[i]
            item['land_name'] = land_name
            item['gemeinde_name'] = gemeinde_name
            # request the content from full_url
            base_url = response.url
            base_url = "https://www.stadt-koeln.de"
            next_url = base_url + first_urls[i]
            #self.log(next_url)
            yield scrapy.Request(next_url, callback=self.detail_page)

    def detail_page(self, response): # pass ArtikleItem
        page_texture = response.xpath('//div[@id="rs_ganzeseite"]//text()').extract()
        self.log('内容: %s' % page_texture)

# Düsseldorf

# Dortmund

# Essen

# Duisburg

# Bochum

# Wuppertal

# Bielefeld

# Bonn

# Münster

# Gelsenkirchen

# Mönchengladbach

# Aachen

# Krefeld

# Oberhausen

# Hagen www.hagen.de

#Hamm
class HammSpider(scrapy.Spider):
    """
    crawl from Hamm stadt website
    """
    name = 'hamm_spider'
    allow_domains = ['www.hamm.de']
    start_urls = [
        "https://www.hamm.de/aktuelle-baugebiete"
    ]

    def parse(self, response):
        #first_titles = response.xpath("//div[@class='frame frame-border-custom frame-type-cqflex_pi7 frame-layout-110']//h3/text()").extract()
        first_urls = response.xpath("//div[@class='frame frame-border-custom frame-type-cqflex_pi7 frame-layout-110']//a/@href").extract()

        gemeinde_name = "Hamm"
        land_name = "NW"

        for i in range(0, len(first_urls)):
            base_url = response.url
            base_url = "https://www.hamm.de"
            next_url = base_url + first_urls[i]
            self.log(next_url)
            yield scrapy.Request(next_url, callback=self.detail_page)

    def detail_page(self, response):
        page_texture = response.xpath("//div[@class='container main-content']//text()").extract()
        self.log('内容: %s' % page_texture)


#Mülheim an der Ruhr
class MuelheimruhrSpider(scrapy.Spider):
    """
    crawling from Mülheim an der Ruhr websites
    """
    name = "muelheimruhr_spider"
    allow_domains = ['www.muelheim-ruhr.de']
    start_urls = [
        "https://www.muelheim-ruhr.de/cms/wohnbauflaechenpotenziale.html"
    ]
    def parse(self, response):
        #first_titles = response.xpath("//div[@class='frame frame-border-custom frame-type-cqflex_pi7 frame-layout-110']//h3/text()").extract()
        first_urls = response.xpath("//div[@class='d115:leistungsbeschreibung']//td/a/@href").extract()

        gemeinde_name = "Mülheim an der Ruhrk"
        land_name = "NW"

        for i in range(0, len(first_urls)):
            base_url = response.url
            next_url = first_urls[i]
            #self.log(next_url)
            yield scrapy.Request(next_url, callback=self.detail_page)

    def detail_page(self, response):
        page_texture = response.xpath("//div[@id='content-inside']//text()").extract()
        #self.log('内容: %s' % page_texture)
        contact_urls = response.xpath("//div[@class='field field-name-field-verantwortliche field-type-ldap-ac field-label-above']//a/@href").extract()
        for i in range(0, len(contact_urls)):
            contact_base_url = "https://geo.muelheim-ruhr.de"
            contact_next_url = contact_base_url + contact_urls[i]
            #self.log(contact_next_url)
            yield scrapy.Request(contact_next_url, callback=self.contact_detail_page)

    def contact_detail_page(self, response):
        contact_page_texture = response.xpath("//div[@id='main']//text()").extract()
        self.log(contact_page_texture)


#Leverkusen

#Solingen

#Herne

#Neuss

#Paderborn

#Bottrop

#Recklinghausen

#Bergisch Gladbach

#Remscheid

#Moers

#Siegen

#Gütersloh

#Wuppertal

#Arnsberg

#Bergheim

#Bocholt

#Castrop-Rauxel

#Detmold

#Dinslaken

#Dormagen

#Dorsten

#Düren

#Gladbeck

#Grevenbroich

#Herford

#Herten

#Iserlohn

class IserlohnSpider(scrapy.Spider):
    """
    crawling from Mülheim an der Ruhr websites
    """
    name = "iserlohn_spider"
    allow_domains = ['www.iserlohn.de']
    start_urls = [
        "https://www.iserlohn.de/wirtschaft-stadtentwicklung/grundstuecks-und-gebaeudeangebote/"
    ]
    def parse(self, response):
        first_titles = response.xpath("//ul[@class='nav']/li//a/text()").extract()
        first_urls = response.xpath("//ul[@class='nav']/li//a/@href").extract()

        gemeinde_name = "Iserlohn"
        land_name = "NW"

        for i in range(0, len(first_titles)):
            first_title = first_titles[i]
            base_url = "https://www.iserlohn.de/"
            next_url = base_url + first_urls[i]
            #self.log(next_url)
            yield scrapy.Request(next_url, callback=self.detail_page)

    def detail_page(self, response):
        page_texture = response.xpath("//div[@class='content-details']//text()").extract()
        self.log('内容: %s' % page_texture)

#Kerpen

#Lippstadt

#Lüdenscheid
class LuedenscheidSpider(scrapy.Spider):
    """
    crawling from Lüdenscheid website
    """
    name = "luedenscheid_spider"
    allow_domains =['www.luedenscheid.de']
    start_urls = ["https://www.luedenscheid.de/wirtschaft/grundstuecke/sp_auto_3155.php"]

    def parse(self, response):
        first_urls = response.xpath("//div[@class='headline']//a/@href").extract()
        first_contents = response.xpath("//div[@class='description']//text()").extract()
        for i in range(0, len(first_urls)):
            base_url = "https://www.luedenscheid.de/"
            next_url = base_url + first_urls[i]
            yield scrapy.Request(next_url, callback=self.detail_page)

    def detail_page(self, response):
        page_texture = response.xpath("//div[@class='container']//text()").extract()
        self.log('内容: %s' % page_texture)
        pass


#Lünen

#Marl

#Minden
class MindenSpider(scrapy.Spider):
    """
    crawling from Minden website
    """
    name = "minden_spider"
    allow_domains =['www.minden.de']
    start_urls = ["https://www.minden.de/stadt_minden/de/Arbeit,%20Wirtschaft,%20Standort/MEW/Grundst%C3%BCcke%20und%20Wohnimmobilien/"]

    def parse(self, response):
        first_contents = response.xpath("//div[@class='maincontent large-9 columns']/li//text()").extract()
        for i in range(0, len(first_contents)):
            pass

#Ratingen

#Rheine

#Troisdorf

#Unna pdf

#Velbert

#Viersen

#Wesel not found

#Witten

#Ahaus
class AhausSpider(scrapy.Spider):
    """
    crawling from Ahaus website
    """
    name = "ahaus_spider"
    allow_domains =['www.stadt-ahaus.de']
    start_urls = ["https://www.stadt-ahaus.de/wirtschaft/datenbankenboersen/wohnbauflaechen/"]

    def parse(self, response):
        first_urls = response.xpath("//div[@class='csc-textpic-text']//a/@href").extract()
        for i in range(first_urls):
            self.log('link: %s' % first_urls[i])

#Ahlen

#Alsdorf

#Altena

#Attendorn; nicht geöffnet

#Bad Honnef

#Bad Oeynhausen

#Bad Salzuflen

#Baesweiler; currently no info

#Beckum; only personal query

#Bedburg;













