# -*- coding: utf-8 -*-
import scrapy
from plantScrapy.items import PlantItem

class plantDataSpider(scrapy.Spider):
    name = 'plantSpider'
    allowed_domains = ['https://www.zhiwuwang.com/baike/']
    start_urls = ['https://www.zhiwuwang.com/baike/list-1734.html']
    # user_agent="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
    # header={'User-Agent':user_agent}
    # proxies={"http":"http://125.120.11.219:6666"}
    for id in range(2,34):
        start_urls.append('https://www.zhiwuwang.com/baike/list-1732-' + str(id) + '.html')
    def parse(self, response):
        subSelector = response.xpath('//div[@class="bk-list-title"]/a')
        items = []
        item = PlantItem()
        item['plantCategory'] = response.xpath('//div[@class="nav"]/a//text()').extract()[2]
        temps = ''
        for temp in subSelector.xpath('./text()').extract():
            temps += temp + ' 0\n'
        item['plantName'] = temps
        items.append(item)
        return items