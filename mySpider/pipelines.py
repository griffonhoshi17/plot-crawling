# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import time
import os
from scrapy.exceptions import DropItem

class FileWriterPipeline(object):

    def process_item(self, item, spider):
        now = time.strftime('%Y%m%d', time.localtime())
        filename = 'Plot' + now + '.txt'
        dirpath = "/Users/hoshiraku/Documents/gemeinde_data/data_crawling/"
        bundesland = item['bundesland']
        gemeinde = item['gemeinde']
        filepath = dirpath + '/' + bundesland + '/' + gemeinde
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        return item
