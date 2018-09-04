# -*- coding: utf-8 -*-
import scrapy
import pandas as pd 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

BASE_URL = 'https://pitchfork.com'

class ReviewItem(scrapy.Item):
	artists = scrapy.Field()
	album = scrapy.Field()
	url = scrapy.Field()
	text = scrapy.Field()

class PitchforkSpider(CrawlSpider):
    name = 'pitchfork'
    allowed_domains = ['pitchfork.com']
    start_urls = ['https://pitchfork.com/reviews/albums/',
    'https://pitchfork.com/reviews/albums/?page=2',
    'https://pitchfork.com/reviews/albums/?page=3',
    'https://pitchfork.com/reviews/albums/?page=4',
    'https://pitchfork.com/reviews/albums/?page=5']

    
    rules = [Rule(LinkExtractor(allow = ''), callback = 'parse', follow = True)]

    def parse(self, response):
    	artists = response.xpath('//ul/li[1]/text()').extract()
    	album = response.xpath('//h2/text()').extract()
    	urls = response.xpath('//div[@class = "review"]/a/@href').extract()
    	url = [BASE_URL + link for link in urls]
 		
    	for link in url:
    			request = scrapy.Request(link, callback = self.review_text,
    			dont_filter = True)
    			yield request
    	
    def review_text(self, response):
    		text = response.xpath('//p/text()').extract()
    		title = response.xpath('//h2/ul/li/a/text()').extract()
    		album = response.xpath('//h1/text()').extract()

    		yield ReviewItem(
    			artists= title,
    			album = album,
    			text = text)

