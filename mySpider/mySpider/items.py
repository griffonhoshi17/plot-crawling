# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    itemTitle = scrapy.Field()
    itemName = scrapy.Field()


class ArticleItem(scrapy.Item):
    # define the link of information
    first_title = scrapy.Field()
    first_content= scrapy.Field()
    first_url = scrapy.Field()

    # define the contents of detail information
    second_title = scrapy.Field()
    second_content = scrapy.Field()
    second_url = scrapy.Field()

    # detail of content
    head = scrapy.Field()
    content = scrapy.Field()

    # define the land and name of gemeind
    land_name = scrapy.Field()
    gemeinde_name = scrapy.Field()

# 
class DetailedInforItem(scrapy.Item):

    pass
