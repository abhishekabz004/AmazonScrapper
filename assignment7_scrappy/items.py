import scrapy
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Assignment7ScrappyItem(scrapy.Item):
    image_url = scrapy.Field()
    images = scrapy.Field()
    pass
