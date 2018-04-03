# -*- coding: utf-8 -*-
import scrapy

from scrapy.contrib.spiders import Rule,CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor 
from assignment7_scrappy.items import Assignment7ScrappyItem
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
    	category = response.css('div.searchUndoAUIHacks')[0]
    	category = response.css('div.a-row div.a-span8 div.s-first-column div.a-spacing-top-small span span span.a-color-state::text').extract_first()#xpath('//div[@id="search-main-wrapper"]//div[@class="nav_redesign s-left-nav-rib-redesign s-span-page"]//div[@class="searchTemplate imageLayout so_in_e"]');
    	for product in response.css('li.s-result-item'):
    		product = product.css('div.s-item-container')
    		cost = product.css('div.a-spacing-none')[2]
    		#cost = product.xpath('//div[@class="a-row a-spacing-none"]/div[@class="a-row a-spacing-none"]//a[@class="a-link-normal a-text-normal"]')
    		yield {
    			'Id': staticNum(),
    			'Name': product.css('div.a-spacing-none div.a-spacing-mini a.s-color-twister-title-link h2.s-access-title::text').extract_first(),
    			'image_urls': product.css('div.a-spacing-base div.a-span12 span.a-declarative div.a-gesture-horizontal div.s-active a.a-link-normal img.s-access-image::attr(src)').extract_first(),                
    			'ProductUrl': product.css('div.a-spacing-none div.a-spacing-mini a.s-color-twister-title-link::attr(href)').extract_first(),
    			'Cost': cost.css('a.a-link-normal span.s-price::text').extract_first(),
    			'Review': product.css('div.a-spacing-none div.a-spacing-top-mini span span.a-declarative a.a-popover-trigger i.a-icon span.a-icon-alt::text').extract_first(),
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