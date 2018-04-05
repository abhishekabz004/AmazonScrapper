# -*- coding: utf-8 -*-
import scrapy
import hashlib

#from scrapy.contrib.spiders import Rule,CrawlSpider
#from scrapy.contrib.linkextractors import LinkExtractor
from ..items import Assignment7ScrappyItem

import csv

class csvWriter():
	def __init__(self):
		with open('result.csv', 'w') as csvfile:
			self.fieldname = ['Id', 'Name', 'ImageUrl', 'ProductUrl', 'Review', 'Cost', 'Category', 'SuperCategory', 'ImagePath']
			self.writer = csv.DictWriter(csvfile, fieldnames=self.fieldname)
			self.writer.writeheader()

	def write(self, pId, name, imgUrl, pUrl, review, cost, cat, supCat, imgPath):
		with open('result.csv', 'a') as csvfile:
			self.fieldname = ['Id', 'Name', 'ImageUrl', 'ProductUrl', 'Review', 'Cost', 'Category', 'SuperCategory', 'ImagePath']
			self.writer = csv.DictWriter(csvfile, fieldnames=self.fieldname)
			self.writer.writerow({'Id': pId, 'Name': name, 'ImageUrl': imgUrl, 'ProductUrl': pUrl, 'Review':review, 'Cost': cost, 'Category': cat, 'SuperCategory': supCat, 'ImagePath': imgPath})

def staticNum():
    staticNum.x += 1
    return staticNum.x
staticNum.x = 0

def staticPage():
    staticPage.x += 1
    return staticPage.x
staticPage.x = 0

csvObj = csvWriter()

class TshirtsspiderSpider(scrapy.Spider):
	name = 'TshirtsSpider'
	#allowed_domains = ['https://www.amazon.in/']
	start_urls = ['https://www.amazon.in/T-Shirts-Polos-Men/s?ie=UTF8&page=1&rh=n%3A1968120031']
	#rules = [Rule(LinkExtractor(allow=['https://images-eu.ssl-images-amazon.com/images/*']),'parse')] 	superCategory = response.css('span.srSprite.backArrow::text')extract_first()
	def parse(self, response):
		category = response.css('h4.a-size-small.a-color-base.a-text-bold::text').extract_first()
		category = category.replace("\n","")
		category = category.replace(" ","")
		superCat = ""

		for superCategory in response.css('li.s-ref-indent-neg-micro'):
			catName = superCategory.css('span.a-size-small.a-color-base::text').extract_first()
			superCat += catName+":"
		superCat = superCat.replace("\n","")
		superCat = superCat.replace(" ","")

		for product in response.css('li.s-result-item'):
			image_url = product.css('img.s-access-image.cfMarker::attr(src)').extract_first()
			prod_id = str(staticNum())
			hashObj = hashlib.sha1(image_url.encode('utf-8'))
			hashDig = hashObj.hexdigest()
			image_path = superCat.replace(":","/")+category+"/"+hashDig+".jpg"
			yield Assignment7ScrappyItem(image_urls=[image_url], image_paths=str(image_path))
			p_name = product.css('h2.a-size-base.s-inline.s-access-title.a-text-normal::text').extract_first()
			p_url = product.css('a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal::attr(href)').extract_first()
			p_review = product.css('div.s-item-container div.a-spacing-none div.a-spacing-top-mini span span.a-declarative a.a-popover-trigger i.a-icon span.a-icon-alt::text').extract_first()
			p_cost = product.css('span.a-size-base.a-color-price.s-price.a-text-bold::text').extract_first()
			csvObj.write(prod_id, p_name, image_url, p_url, p_review, p_cost, category, superCat, image_path )
			'''
			yield {
    			'Id': prod_id,
    			'Name': product.css('h2.a-size-base.s-inline.s-access-title.a-text-normal::text').extract_first(),
    			'imageUrl': image_url,
    			'ProductUrl': product.css('a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal::attr(href)').extract_first(),
    			'Review': product.css('div.s-item-container div.a-spacing-none div.a-spacing-top-mini span span.a-declarative a.a-popover-trigger i.a-icon span.a-icon-alt::text').extract_first(),
    			'Cost': product.css('span.a-size-base.a-color-price.s-price.a-text-bold::text').extract_first(),
    			'Category': category,
				'SuperCategory': superCat,
				'ImagePath' : image_path,
    		}'''
		next_page = response.css('span.pagnLink')[1]
		next_page = next_page.css('a::attr(href)').extract_first()
		pgNo= staticPage()
		if pgNo<1:
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