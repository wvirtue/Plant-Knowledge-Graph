# -*- coding: utf-8 -*-
import scrapy
from plantScrapy.items import PlantItem

class plantDataSpider(scrapy.Spider):
    name = 'nameSpider'
    allowed_domains = ['https://www.zhiwuwang.com/baike/']
    start_urls = []
    # user_agent="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
    # header={'User-Agent':user_agent}
    # proxies={"http":"http://125.120.11.219:6666"}
    for id in range(1711,1732):
        start_urls = 'https://www.zhiwuwang.com/baike/list.php?catid=' + str(id)
    def parse(self, response):
        items = []
        item = PlantItem()
        plantNameSelector = response.xpath('//div[@class="bk-list-title"]')
        for plant in plantNameSelector:
            temps = ''
            for temp in plant.xpath('./a//text()').extract():
                temps += temp
            item['plantName'] = temps
            # temps = ''
            # for temp in sub.xpath('./ul/li[2]//text()').extract():
            #     temps += temp
            # item['temperature'] = temps
            # item['weather'] = sub.xpath('./ul/li[3]//text()').extract()[0]
            # item['wind'] = sub.xpath('./ul//li[4]//text()').extract()[0]
            items.append(item)
        return items