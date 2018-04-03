# -*- coding: utf-8 -*-
import scrapy

from scrapy.contrib.spiders import Rule,CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor 
from ..items import Assignment7ScrappyItem

def staticNum():
    staticNum.x += 1
    return staticNum.x
staticNum.x = 0

def staticPage():
    staticPage.x += 1
    return staticPage.x
staticPage.x = 0

class TshirtsspiderSpider(scrapy.Spider):
    name = 'TshirtsSpider'
    #allowed_domains = ['https://www.amazon.in/s/ref=lp_1968120031_pg_2?rh=n%3A1571271031%2Cn%3A%211571272031%2Cn%3A1968024031%2Cn%3A1968120031']
    start_urls = ['https://www.amazon.in/T-Shirts-Polos-Men/s?ie=UTF8&page=1&rh=n%3A1968120031']
    #rules = [Rule(LinkExtractor(allow=['https://images-eu.ssl-images-amazon.com/images/*']),'parse')]
    def parse(self, response):
    	category = response.css('span.a-color-state.a-text-bold::text').extract_first()
    	for product in response.css('li.s-result-item'):
    		image_url = product.css('img.s-access-image.cfMarker::attr(src)').extract_first()
    		yield Assignment7ScrappyItem(image_urls=[image_url])
    		#cost = product.xpath('//div[@class="a-row a-spacing-none"]/div[@class="a-row a-spacing-none"]//a[@class="a-link-normal a-text-normal"]')
    		yield {
    			'Id': staticNum(),
    			'Name': product.css('h2.a-size-base.s-inline.s-access-title.a-text-normal::text').extract_first(),
    			'imageUrl': image_url,
    			'ProductUrl': product.css('a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal::attr(href)').extract_first(),
    			'Review': product.css('div.s-item-container div.a-spacing-none div.a-spacing-top-mini span span.a-declarative a.a-popover-trigger i.a-icon span.a-icon-alt::text').extract_first(),
    			'Cost': product.css('span.a-size-base.a-color-price.s-price.a-text-bold::text').extract_first(),
    			'Category': category,
    		}
    	next_page = response.css('span.pagnLink')[1]
    	next_page = next_page.css('a::attr(href)').extract_first()
    	pgNo= staticPage()
    	if pgNo<7:
    		if pgNo == 1:
    			next_page = response.css('span.pagnLink')[0]
    		elif pgNo == 2:
    			next_page = response.css('span.pagnLink')[1]
    		elif pgNo == 3:
    			next_page = response.css('span.pagnLink')[2]
    		elif pgNo == 4:
    			next_page = response.css('span.pagnLink')[3]
    		elif pgNo == 5:
    			next_page = response.css('span.pagnLink')[2]
    		elif pgNo == 6:
    			next_page = response.css('span.pagnLink')[2]
    		next_page = next_page.css('a::attr(href)').extract_first()
    		if next_page is not None:
    			yield response.follow(next_page, callback=self.parse)
