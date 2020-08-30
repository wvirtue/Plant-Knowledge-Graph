# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import os.path
import urllib

class PlantPipeline(object):
    def process_item(self, item, spider):
        # today = time.strftime('%Y%m%d',time.localtime())
        fileName = item['plantCategory'] + '.txt'
        with open(fileName,'ab+') as fp:
            fp.write(item['plantName'].encode('utf8') + b'')
            # fp.write('0' + b'\n')
            time.sleep(1)
        return item
