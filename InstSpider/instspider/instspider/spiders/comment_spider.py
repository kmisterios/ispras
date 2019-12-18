import scrapy
from scrapy.selector import Selector
from scrapy import Spider
from instspider.items import Comment
import json

class QuotesSpider(scrapy.Spider):
    name = "comment"

    def start_requests(self):
        link = (str)(getattr(self, 'link'))
        urls = [link]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = Comment()
        link = response.css('meta')[17]
        idstr = link.css('::attr(content)').get()
        item['idstr'] = idstr
        return item

