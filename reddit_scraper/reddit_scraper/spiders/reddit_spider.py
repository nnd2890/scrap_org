from datetime import datetime as dt
import scrapy

class RedditSpider(scrapy.Spider):
    name='reddit'

    def start_requests(self):
        yield scrapy.Request('http://reddit.com')

    def parse(self, response):
        items = []
        for div in response.css('div.scrollerItem'):
            try:
                title = div.css('h2.s134yi85-0.bNKTNd::text').extract_first()
                votes = div.css('div._1rZYMD_4xY3gRcSS3p8ODO::text').extract_first()
                items.append({'title':title, 'votes':votes})
            except:
                pass

        if len(items)>0:
            return {'items':items}