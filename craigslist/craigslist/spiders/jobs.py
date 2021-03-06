# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')
 
        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first()
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            yield Request(absolute_url, callback=self.parse_page, meta={'URL':absolute_url,'Title':title,'Address':address})

    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        address = response.meta.get('Address')

        description = ''.join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())
        yield {'URL':url, 'Title':title, 'Address':address, 'Description':description}

