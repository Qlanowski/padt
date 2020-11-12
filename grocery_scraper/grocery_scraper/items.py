# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GroceryScrapperItem(scrapy.Item):
    price = scrapy.Field()
    photo_url = scrapy.Field()
    features = scrapy.Field()
    description = scrapy.Field()
    ean = scrapy.Field()
    title = scrapy.Field()
    price_before_discount = scrapy.Field()
    price_per_quantity = scrapy.Field()
    category = scrapy.Field()
    packaging = scrapy.Field()
    nutrition = scrapy.Field()
    features = scrapy.Field()
    ingredients = scrapy.Field()