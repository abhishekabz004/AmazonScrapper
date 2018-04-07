# -*- coding: utf-8 -*-
import scrapy
import hashlib

#from scrapy.contrib.spiders import Rule,CrawlSpider
#from scrapy.contrib.linkextractors import LinkExtractor
from ..items import Assignment7ScrappyItem

import csv
import os.path

class csvWriter():
	def initiate(self,path):
		filePath =  "dataSet/amazon_"+path.lower()+".csv"
		if not os.path.exists(os.path.dirname("dataSet/")):
			os.makedirs(os.path.dirname("dataSet/"))
		if not os.path.isfile(filePath):
			with open(filePath, 'w') as csvfile:
				self.fieldname = ['Id', 'Name', 'ImageUrl', 'ProductUrl', 'Review', 'Cost', 'Category', 'SuperCategory', 'ImagePath']
				self.writer = csv.DictWriter(csvfile, fieldnames=self.fieldname)
				self.writer.writeheader()

	def write(self, pId, name, imgUrl, pUrl, review, cost, cat, supCat, imgPath):
		filePath = "dataSet/amazon_"+supCat.replace(":","_").lower()+cat.lower()+".csv"
		with open(filePath , 'a') as csvfile:
			self.fieldname = ['Id', 'Name', 'ImageUrl', 'ProductUrl', 'Review', 'Cost', 'Category', 'SuperCategory', 'ImagePath']
			self.writer = csv.DictWriter(csvfile, fieldnames=self.fieldname)
			self.writer.writerow({'Id': pId, 'Name': name, 'ImageUrl': imgUrl, 'ProductUrl': pUrl, 'Review':review, 'Cost': cost, 'Category': cat, 'SuperCategory': supCat, 'ImagePath': imgPath})

csvObj = csvWriter()

class TshirtsspiderSpider(scrapy.Spider):
    name = 'TshirtsSpider'
    idNumber = 0
    pgNumber = 0

    def findBetween(self,s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    start_urls = ['https://www.amazon.in/s/ref=lp_1968120031_pg_2?rh=n%3A1571271031%2Cn%3A!1571272031%2Cn%3A1968024031%2Cn%3A1968120031&page=1&ie=UTF8&qid=1523098448']

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
        csvObj.initiate(superCat.replace(":","_")+category)

        for product in response.css('li.s-result-item'):
            image_url = product.css('img.s-access-image.cfMarker::attr(src)').extract_first()
            self.idNumber = self.idNumber +1
            prod_id = str(self.idNumber)
            hashObj = hashlib.sha1(image_url.encode('utf-8'))
            hashDig = hashObj.hexdigest()
            image_path = superCat.replace(":","/")+category+"/"+hashDig+".jpg"
            yield Assignment7ScrappyItem(image_urls=[image_url], image_paths=str(image_path))
            p_name = product.css('h2.a-size-base.s-inline.s-access-title.a-text-normal::text').extract_first()
            p_url = product.css('a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal::attr(href)').extract_first()
            p_review = product.css('div.s-item-container div.a-spacing-none div.a-spacing-top-mini span span.a-declarative a.a-popover-trigger i.a-icon span.a-icon-alt::text').extract_first()
            p_cost = product.css('span.a-size-base.a-color-price.s-price.a-text-bold::text').extract_first()
            csvObj.write(prod_id, p_name, image_url, p_url, p_review, p_cost, category, superCat, image_path )

        next_page = response.css('span.pagnLink')[1]
        next_page = next_page.css('a::attr(href)').extract_first()
        self.pgNumber = self.pgNumber+1
        pgNo= self.pgNumber
        if pgNo<50:
            curPg = self.findBetween(next_page,"page=","&rh=")
            curPg = "page="+curPg
            newPg = "page="+str(pgNo+1)
            nextRef = next_page.replace(curPg,newPg)
            if nextRef is not None:
                yield response.follow(nextRef, callback=self.parse)
