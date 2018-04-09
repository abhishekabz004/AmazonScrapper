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
				self.fieldname = ['Id', 'Name', 'ProductId', 'ImageUrl', 'ProductUrl', 'Review', 'Cost', 'Category', 'SuperCategory', 'ImagePath']
				self.writer = csv.DictWriter(csvfile, fieldnames=self.fieldname)
				self.writer.writeheader()

	def write(self, pId, name, p_id, imgUrl, pUrl, review, cost, cat, supCat, imgPath):
		filePath = "dataSet/amazon_"+supCat.replace(":","_").lower()+cat.lower()+".csv"
		with open(filePath , 'a') as csvfile:
			self.fieldname = ['Id', 'Name', 'ProductId', 'ImageUrl', 'ProductUrl', 'Review', 'Cost', 'Category', 'SuperCategory', 'ImagePath']
			self.writer = csv.DictWriter(csvfile, fieldnames=self.fieldname)
			self.writer.writerow({'Id': pId, 'Name': name, 'ProductId': p_id, 'ImageUrl': imgUrl, 'ProductUrl': pUrl, 'Review':review, 'Cost': cost, 'Category': cat, 'SuperCategory': supCat, 'ImagePath': imgPath})

csvObj = csvWriter()

class TshirtsspiderSpider(scrapy.Spider):
    name = 'TshirtsSpider'

    def findBetween(self, s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    start_urls = ['https://www.amazon.in/gp/search/ref=sr_hi_4?rh=n%3A1571271031%2Cn%3A%211571272031%2Cn%3A1968024031%2Cn%3A1968093031%2Cn%3A1968096031&bbn=1968096031&ie=UTF8&qid=1523269086', 'https://www.amazon.in/s/gp/search/ref=sr_nr_p_98_0?fst=as%3Aoff&rh=n%3A1571271031%2Cn%3A%211571272031%2Cn%3A1968024031%2Cn%3A1968248031%2Cn%3A1968250031&bbn=1968248031&hidden-keywords=-shirts&ie=UTF8&qid=1523266541', 'https://www.amazon.in/s/ref=sr_hi_4?rh=n%3A1571271031%2Cn%3A%211571272031%2Cn%3A1968024031%2Cn%3A1968093031%2Cn%3A1968094031&bbn=1968094031&ie=UTF8&qid=1523256981', 'https://www.amazon.in/s/ref=lp_1968024031_nr_n_4?fst=as%3Aoff&rh=n%3A1571271031%2Cn%3A%211571272031%2Cn%3A1968024031%2Cn%3A11960414031&bbn=1968024031&ie=UTF8&qid=1523266444&rnid=1968024031', 'https://www.amazon.in/s/ref=lp_1968024031_nr_n_6?fst=as%3Aoff&rh=n%3A1571271031%2Cn%3A%211571272031%2Cn%3A1968024031%2Cn%3A1968107031&bbn=1968024031&ie=UTF8&qid=1523266444&rnid=1968024031', 'https://www.amazon.in/s/ref=sr_pg_1?rh=n%3A1571271031%2Cn%3A%211571272031%2Cn%3A1968024031%2Cn%3A1968120031&ie=UTF8&qid=1523260539&ajr=2']
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
            hashObj = hashlib.sha1(image_url.encode('utf-8'))
            hashDig = hashObj.hexdigest()
            image_path = superCat.replace(":","/")+category+"/"+hashDig+".jpg"
            if image_url:
                yield Assignment7ScrappyItem(image_urls=[image_url], image_paths=str(image_path))
            id = product.css('li::attr(id)').extract_first()
            if id:
                id = int(id.replace("result_",""))+1
            p_id = product.css('li::attr(data-asin)').extract_first()
            p_name = product.css('h2.a-size-base.s-inline.s-access-title.a-text-normal::text').extract_first()
            p_url = product.css('a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal::attr(href)').extract_first()
            p_review = product.css('div.s-item-container div.a-spacing-none div.a-spacing-top-mini span span.a-declarative a.a-popover-trigger i.a-icon span.a-icon-alt::text').extract_first()
            p_cost = product.css('span.a-size-base.a-color-price.s-price.a-text-bold::text').extract_first()
            if p_cost:
                p_cost = p_cost.replace("-","")
                p_cost = p_cost.replace(" ","")
            csvObj.write(id, p_name, p_id, image_url, p_url, p_review, p_cost, category, superCat, image_path )
            image_url = product.css('div.s-hidden a.a-link-normal.a-text-normal div::attr(data-search-image-source)').extract_first()
            if image_url:
                hashObj = hashlib.sha1(image_url.encode('utf-8'))
                hashDig = hashObj.hexdigest()
                image_path = superCat.replace(":", "/") + category + "/" + hashDig + ".jpg"
                yield Assignment7ScrappyItem(image_urls=[image_url], image_paths=str(image_path))
                csvObj.write(id, p_name, p_id, image_url, p_url, p_review, p_cost, category, superCat, image_path)

        next_page = response.css('a.pagnNext::attr(href)').extract_first()
        curPg = int(self.findBetween(next_page, "page=", "&rh="))
        if curPg<=100:
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)